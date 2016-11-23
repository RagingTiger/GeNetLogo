// INDISIM3Controller.java
// Author: John D. Anderson
// Email: jander43@vols.utk.edu

// original args:
// double init_bact1,
// double init_bact2, double init_loc_nutr,
// double yield_1, double mass_repr, double avail_k,
// double inhib_k, double uptake_k, double maint,
// double viabil, double fed_nutr,
// double out_res_nutr, double len_time_fed,
// double in_out_percnt, double yield_2,
// int ticks

// libraries
import java.util.*;
import py4j.GatewayServer;
import org.nlogo.headless.HeadlessWorkspace;

// class defs
public class INDISIM3Controller {

    // test function
    public int test_func(int first, int second) {
        return first + second;
    }

    // fitness function for use in genetic algorithm
    public static double[] fitness_function(HashMap<String, Float> pydict) {

      // setting up new workspace for "headless" NetLogo simulation
      HeadlessWorkspace workspace = HeadlessWorkspace.newInstance() ;

      // beginning actual API interface
      try {
        // open NetLogo model
        workspace.open("NetLogo_Model/" + "INDISIM3.nlogo");

        // strings to be passed to NetLogo
        String set_initial_bact1 = String.format("set initial_bacteria_1 %3f",
                                                  pydict.get("init_bact1"));

        String set_initial_bact2 = String.format("set initial_bacteria_2 %3f",
                                                  pydict.get("init_bact2"));

        String set_initial_local_nutrient = String.format(
                                            "set initial_local_nutrient %3f",
                                            pydict.get("init_loc_nutr"));

        String set_yield = String.format("set yield %3f",
                                         pydict.get("yield_1"));

        String set_mass_reproduction = String.format(
                                       "set mass_reproduction %3f",
                                       pydict.get("mass_repr"));

        String set_availability_k = String.format("set availability_k %3f",
                                                  pydict.get("avail_k"));

        String set_inhibitory_k = String.format("set inhibitory_k %3f",
                                                pydict.get("inhib_k"));

        String set_uptake_k = String.format("set uptake_k %3f",
                                            pydict.get("uptake_k"));

        String set_maintenance_k = String.format("set maintenance_k %3f",
                                                 pydict.get("maint"));

        String set_viability_time = String.format("set viability_time %3f",
                                                  pydict.get("viabil"));

        String set_fed_nutrient = String.format("set fed_nutrient %3f",
                                                pydict.get("fed_nutr"));

        String set_out_reservoir_nutrient = String.format(
                                            "set out_reservoir_nutrient %3f",
                                            pydict.get("out_res_nutr"));

        String set_length_time_feed = String.format("set length_time_feed %3f",
                                                    pydict.get("len_time_fed"));

        String set_in_out_percent = String.format("set in_out_percent %3f",
                                                  pydict.get("in_out_percnt"));

        String set_yield_2 = String.format("set yield-2 %3f",
                                           pydict.get("yield_2"));

        String repeatgo = repeatgo = String.format("repeat %f [ go ]",
                                                   pydict.get("ticks"));

        // setting up initial values for parameters
        workspace.command("setup");
        workspace.command(set_initial_bact1);
        workspace.command(set_initial_bact2);
        workspace.command(set_initial_local_nutrient);
        workspace.command(set_yield);
        workspace.command(set_mass_reproduction);
        workspace.command(set_availability_k);
        workspace.command(set_inhibitory_k);
        workspace.command(set_uptake_k);
        workspace.command(set_maintenance_k);
        workspace.command(set_viability_time);
        workspace.command(set_fed_nutrient);
        workspace.command(set_out_reservoir_nutrient);
        workspace.command(set_length_time_feed);
        workspace.command(set_in_out_percent);
        workspace.command(set_yield_2);
        workspace.command("setup");


        // run simulation
        workspace.command(repeatgo);

        // int array to store values
        double[] fitval = new double[3];

        // getting sim values
        fitval[0] = (double)workspace.report("count turtles");
        fitval[1] = (double)workspace.report("count turtles with [color = pink]");
        fitval[2] = (double)workspace.report("count turtles with [color = sky]");

        // quiting NetLogo Application after simulation(s) end
        workspace.dispose();

        // exit
        return fitval;

      } catch(Exception ex) {
          ex.printStackTrace();
          double[] errval = new double[1];
          errval[0] = 1.0;
          return errval;
      }
    }

    // main function
    public static void main(String[] args) {
        // check CLA
        if (args.length > 0) {
            // strcomp
            String flag = "-m";
            int comp = flag.compareTo(args[0]);

            // execute if "-m" flag present
            if (comp == 0) {
              // get new hashmap
              HashMap<String, Float> dict = new HashMap<String, Float>();

              // fill hashmap
              dict.put("init_bact1", new Float(1.0));
              dict.put("init_bact2", new Float(25.0));
              dict.put("init_loc_nutr", new Float(500.0));
              dict.put("yield_1", new Float(1.80));
              dict.put("mass_repr", new Float(50.0));
              dict.put("avail_k", new Float(0.5));
              dict.put("inhib_k", new Float(0.0));
              dict.put("uptake_k", new Float(0.50));
              dict.put("maint", new Float(0.25));
              dict.put("viabil", new Float(200.0));
              dict.put("fed_nutr", new Float(300.0));
              dict.put("out_res_nutr", new Float(901200.0));
              dict.put("len_time_fed", new Float(10.0));
              dict.put("in_out_percnt", new Float(0.040));
              dict.put("yield_2", new Float(3.00));
              dict.put("ticks", new Float(200));

              // call fitness function
              double[] values = fitness_function(dict);
              // check to see if an error occured
              if (values.length == 1) {
                System.exit(-1);
              }

              // print out results otherwise
              System.out.println(values[0]);
              System.out.println(values[1]);
              System.out.println(values[2]);

              // exit
              System.exit(0);
            }
        }

        // run gatweay servers
        INDISIM3Controller app = new INDISIM3Controller();
        GatewayServer server = new GatewayServer(app);
        server.start();
    }
}
