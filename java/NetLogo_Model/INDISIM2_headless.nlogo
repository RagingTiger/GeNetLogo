;; ENTITIES AND VARIABLES

globals [ total_nutrient total_end_product total_biomass upt ava_upt
  bacteria_t-1 bacteria_t biomass_t-1 biomass_t rate_bacteria rate_biomass
  devr devu devv min_mass devmm]
turtles-own [ mass start_mass energy viab ]
patches-own [ local_nutrient local_end_product ]


;; INITIALIZATION

to setup
  clear-all
  random-seed 1111
  set devr 0.20 * mass_reproduction     ; Slider Button Value
  set devu 0.15 * uptake_k              ; Slider Button Value
  set devv 0.20 * viability_time        ; Slider Button Value
  set min_mass 0.50 * mass_reproduction
  set devmm 0.25 * min_mass             ; Slider Button Value

  setup-bacteria-1

  set total_nutrient 0
  set total_end_product 0

  setup-medium

  do-plotting
  reset-ticks
end

to setup-bacteria-1                         ; Function Definition: "setup-bacteria-1"
  set-default-shape turtles "dot"           ; NOTE: Function has two different types of bacteria
    create-turtles initial_bacteria_1
  [ setxy random-pxcor random-pycor
    let mass_ini mass_reproduction / 2
    set mass abs ( random-normal mass_ini devr )
    set start_mass abs ( random-normal mass_reproduction devr )
    set energy 0
    set viab 0
    set color pink
    set total_biomass total_biomass + mass]

  create-turtles initial_bacteria_2
  [ setxy random-pxcor random-pycor
    let mass_ini mass_reproduction / 2
    set mass abs ( random-normal mass_ini devr )
    set start_mass abs ( random-normal mass_reproduction devr )
    set energy 0
    set viab 0
    set color sky
    set total_biomass total_biomass + mass]
end

to setup-medium
 ask patches [ set local_nutrient initial_local_nutrient]
 set total_nutrient sum [local_nutrient] of patches
end


;; MAIN LOOP

to go

  set bacteria_t-1 count turtles
  set biomass_t-1 sum [mass] of turtles

  ask turtles [ move uptake viability reproduce ]

  set total_biomass sum [mass] of turtles
  set total_nutrient sum [local_nutrient] of patches
  set total_end_product sum [local_end_product] of patches

  update_system

  set bacteria_t count turtles
  set biomass_t sum [mass] of turtles
  if bacteria_t = 0 [ stop ]
  set rate_bacteria (bacteria_t - bacteria_t-1) / bacteria_t-1
  set rate_biomass (biomass_t - biomass_t-1) / biomass_t-1

  tick

  do-plotting

  ;  write-to-file    ; NOTE: uncomment to restore constant updating after "tick"

end


to move
  move-to one-of neighbors
end

to uptake

    let up abs ( random-normal uptake_k devu )
    set upt up * (mass ^ (2. / 3.))

    set ava_upt availability_k * [local_nutrient] of patch-here
    if upt > ava_upt [set upt ava_upt]
    set local_nutrient local_nutrient - upt

    set energy yield * upt
    set energy energy - maintenance_k * mass - inhibitory_k * local_end_product
    set local_end_product local_end_product + upt

    if energy < 0 [set energy 0 if mass > abs ( random-normal min_mass devmm ) [set mass (0.99 * mass)]]
    set mass mass + yield * energy ;; production of new biomass
end

to viability
    if energy = 0 [set viab viab + 1]
    let viab_death abs (random-normal viability_time devv)
    if viab > viab_death [ die]
end

to reproduce
   if mass > start_mass
   [set mass mass / 2 set start_mass abs ( random-normal mass_reproduction devr ) set energy energy / 2 set viab viab / 2
    hatch 1 [set mass mass set start_mass abs ( random-normal mass_reproduction devr ) set energy energy set viab viab]]
end

to update_system
 diffuse local_nutrient 0.50
 diffuse local_end_product 0.50

;;Protocol of the bioreactor

 if (bioreactor = "Fed-batch")
  [
    if ticks mod length_time_feed = 0
    [ ask patches [set local_nutrient local_nutrient + fed_nutrient]
     set total_nutrient sum [local_nutrient] of patches ]
  ]

 if (bioreactor = "Continuous")
  [
    set total_nutrient total_nutrient + in_out_percent * out_reservoir_nutrient
    set total_nutrient total_nutrient - in_out_percent * total_nutrient
    set total_end_product total_end_product - in_out_percent * total_end_product

    let temp1 total_nutrient / (world-width ^ 2)
    ask patches [ set local_nutrient temp1 ]

    let temp2 total_end_product / (world-width ^ 2)
    ask patches [ set local_end_product temp2 ]

    let  temp3 round (in_out_percent * count turtles)
    ask n-of temp3 turtles [ die ]

    set total_biomass sum [mass] of turtles
  ]
end

to do-plotting
  set-current-plot "Nutrient"
  set-current-plot-pen "total_nutrient"
  plot total_nutrient

  set-current-plot "End product"
  set-current-plot-pen "total_end_product"
  plot total_end_product

  set-current-plot "Viable bacteria"
  set-current-plot-pen "turtles"
  plot count turtles

  set-current-plot "Total viable biomass"
  set-current-plot-pen "total_biomass"
  plot total_biomass

  set-current-plot "Mass distribution"
  set-current-plot-pen "mass_distribution"
  histogram [mass] of turtles with [color = pink]

  set-current-plot "Mass"
  set-current-plot-pen "mass_distribution"
  histogram [mass] of turtles with [color = sky]
end

to write-to-file
  if ticks <= 2000 [file-print (word "  " count turtles word " " initial_bacteria_1 word " " initial_bacteria_2 word " " count turtles with [color = pink] word " " count turtles with [color = sky])]
  ;file-print
end
@#$#@#$#@
GRAPHICS-WINDOW
804
10
1062
289
-1
-1
8.0
1
10
1
1
1
0
0
0
1
0
30
0
30
1
1
1
ticks
30.0

BUTTON
199
15
260
48
setup
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
186
156
357
189
inhibitory_k
inhibitory_k
0
0.1
0
0.001
1
NIL
HORIZONTAL

SLIDER
7
80
179
113
initial_bacteria_1
initial_bacteria_1
0
50
13
1
1
NIL
HORIZONTAL

SLIDER
9
156
181
189
yield
yield
0.0
3
1.8
0.05
1
NIL
HORIZONTAL

PLOT
274
334
519
474
Nutrient
Time steps
NIL
0.0
10.0
0.0
100.0
true
false
"" ""
PENS
"total_nutrient" 1.0 0 -6459832 true "" ""

MONITOR
1080
11
1161
60
# Bacteria
count turtles
1
1
12

SLIDER
8
118
181
151
initial_local_nutrient
initial_local_nutrient
0
1000
500
1
1
NIL
HORIZONTAL

PLOT
11
192
273
330
Viable bacteria
Time steps
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"turtles" 1.0 0 -16777216 true "" ""

BUTTON
274
15
370
48
go one step
go
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
383
15
445
48
go
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
186
79
357
112
mass_reproduction
mass_reproduction
0
100
50
1
1
NIL
HORIZONTAL

MONITOR
1081
66
1163
115
Nutrient
total_nutrient
0
1
12

PLOT
524
335
767
472
End product
Time steps
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" ""
"total_end_product" 1.0 0 -16777216 true "" ""

MONITOR
1081
119
1166
168
End product
total_end_product
0
1
12

SLIDER
363
78
527
111
uptake_k
uptake_k
0
1
0.5
0.01
1
NIL
HORIZONTAL

SLIDER
363
156
528
189
viability_time
viability_time
0
300
200
5
1
NIL
HORIZONTAL

SLIDER
363
118
527
151
maintenance_k
maintenance_k
0
1
0.25
0.01
1
NIL
HORIZONTAL

CHOOSER
9
10
147
55
Bioreactor
Bioreactor
"Batch" "Fed-batch" "Continuous"
1

SLIDER
381
228
553
261
fed_nutrient
fed_nutrient
0
400
300
10
1
NIL
HORIZONTAL

SLIDER
558
228
730
261
length_time_feed
length_time_feed
1
50
10
1
1
NIL
HORIZONTAL

TEXTBOX
286
233
374
265
For Fed-batch:
13
0.0
0

PLOT
10
334
271
477
Total viable biomass
Time steps
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" ""
"total_biomass" 1.0 0 -16777216 true "" ""

TEXTBOX
288
288
445
318
For continuous culture:
12
0.0
0

SLIDER
425
277
602
310
out_reservoir_nutrient
out_reservoir_nutrient
0
1000000
901200
100
1
NIL
HORIZONTAL

SLIDER
607
277
783
310
in_out_percent
in_out_percent
0
0.10
0.04
0.001
1
NIL
HORIZONTAL

SLIDER
186
118
357
151
availability_k
availability_k
0
1
0.5
0.01
1
NIL
HORIZONTAL

MONITOR
1083
198
1181
243
Rate of biomass
rate_biomass
4
1
11

MONITOR
1083
245
1191
290
Rate of bacteria
rate_bacteria
4
1
11

PLOT
808
299
1061
471
Mass distribution
Mass
Count
0.0
100.0
0.0
10.0
true
false
"" ""
PENS
"mass_distribution" 2.0 1 -2064490 true "" ""

PLOT
1063
298
1295
471
Mass
Mass
Count
0.0
100.0
0.0
10.0
true
false
"" ""
PENS
"mass_distribution" 2.0 1 -13791810 true "" ""

SLIDER
11
482
183
515
initial_bacteria_2
initial_bacteria_2
0
50
12
1
1
NIL
HORIZONTAL

@#$#@#$#@
## WHAT IS IT?

The purpose of this model is to provide a virtual bacterial bioreactor with three possible operating protocols (batch, fed-batch, and continuous cultures) so that the resulting dynamics can be studied and compared.

The general concepts and basic principles of the bacterial model are taken from INDISIM (Ginovart et al., 2002).

At this moment it allows a qualitative study, but in the near future it will be parameterized in order to be used for quantitative purposes in an adaption to specific applications.

## HOW IT WORKS

Basic entities are bacteria and spatial cells.

Bacterial variables include for each microorganism, a location (i.e., the spatial cell where it is), a mass, the required energy for maintenance, the mass at which it will enter the reproduction cycle, and the viability.

Spatial cell variables include the nutrient content and end product content.

This is a non-parameterized version so there is not a real units correspondence yet.

At each time step of the simulation, bacterial cells act or perform a set of actions. The sets of rules governing the behaviour or actions of each bacterium are in the following categories or sub-models:

(i) motion (randomly),
(ii) uptake and maintenance (i.e., uptake of nutrient particles to achieve cellular maintenance first and then, if there is enough nutrient, increase bacterial biomass, with excretion of the end product to the spatial cell),
(iii) reproduction by bipartition (when certain conditions are satisfied) and
(iv) cell viability (and death as appropriate).

The damage that an excreted end product can produce in bacterial cells may be considered.

Sub-models regarding spatial cells include the culture stirring, the entrance of fresh medium, and output of medium and bacteria according to the corresponding operating protocol. These actions are performed once individuals have acted.

The global scheduling of the simulation model is made up of various elements:
(1) initialization of the system with the input data chosen by the user, where initial configuration of the bacterial population and the spatial environment are set up, as well as the parameters for the chosen operating protocol;
(2) the main loop (time step or tick), in which all the rules for each bacterium and the medium are implemented and repeated, and the external actions on the system are applied, until reaching the end of the simulation; and
(3) the output of results at the end of each time step.

## HOW TO USE IT

Initialization is explicitly done by the user by pressing the “setup” button at the interface. Then the simulator reads all the input data and builds the system in its initial state, generating the “virtual world” with spatial characteristics (a homogeneous distribution of nutrient) and a population with initial individual characteristics for each bacterium. Then, it is ready to start the simulation by pressing the button “go one step” or “go”.

The operating protocol and model options, as well as the input values for the parameters of the model are chosen by the user at the interface within the allowed range by using “sliders”. The current version is non-parameterized, so these data are in simulation units.

The inputs that have to be set up are: initial number of bacteria, initial amount of nutrient, mean mass to initiate the reproduction cycle, availability of the nutrient to be uptaken for the bacterium, mean time that a bacterium remains viable without its energetic requirements, and the constants to determine the maximum amount of nutrient that a bacterium can uptake, the energetic requirements for cellular maintenance, the metabolic efficiency that accounts for the synthesised biomass per metabolised nutrient (yield), and the extra energy necessary to compensate the damaging effect that the presence of the end product acting as an inhibitor has on a bacterium.

Possible operating protocols are a batch culture (no nutrient entrance), a fed-batch culture and a continuous culture. If fed-batch is chosen, the handling characteristics, amount and periodicity of nutrient input, must be fixed. If continuous protocol is chosen, the amount of the external nutrient reservoir and the percentage of medium renewal have to be fixed.

The model options are chosen by means of some the above-mentioned parameters: e.g., if the inhibitory constant is fixed to 0, inhibitory effects will not be taken into account.

## THINGS TO NOTICE

The chosen operating protocol of the bioreactor is decisive for the dynamics of the system and structure of the bacterial population. These features arise from the reproduction and viability of the individuals which are conditioned by local nutrient availability and inhibition of the end product (affected by the entrance or not of fresh medium, and/or the output of the growth medium). Therefore, the individual activity is highly affected by the operating protocol of the culture.

An adaptation for individuals is the consumption of their own biomass when there is a nutrient scarcity, but the bacterial biomass has a lower limit under which bacteria just die. Also, in the presence of an end product that has an inhibitory effect, the microorganism needs to spend more energy to compensate this effect.

Stochasticity is introduced into the model when setting some characteristics of individuals using a Gaussian distribution around an expected mean value. This distribution remains the most commonly encountered distribution in nature and statistics, and reflects range in the population. Randomness is also considered when the rules are applied to individuals and to spatial cells by using probabilistic distributions to deal with or manage individual events. This represents the uncertainty in these processes and reflects the high variety of mechanisms that underlie the irregularity observed in natural processes and biological materials.

Observation data can be divided into macroscopic and mesoscopic. The former includes the evolution of several population-level variables such as number of individuals, total biomass, amount of nutrient, end product concentration, and rates of change in the size of the bacterial population and its total biomass. The latter refers to variables that connect individuals to population; in this case the mesoscopic variable is the bacterial biomass distribution, which is a reflection of the population structure and its evolution.

Stirring the culture permits the exclusion of local diffusion limitations. A periodically very high diffusion of nutrient and end product is performed in the medium.

## THINGS TO TRY

1) Identify the four classical phases of a population growth curve - lag, exponential or logarithmic phase, stationary phase, and death phase - in a closed loop system.

In the batch culture (a closed system with no entry or exit of individual cells and/or substrate particles) bacteria usually grow and reproduce until one necessary growth factor becomes exhausted (nutrient) and it becomes growth limiting or the accumulation of an end product with inhibitory effect is excessive. If no additional nutrient is added or the inhibitors are removed, no further growth will take place. Growth in such a closed loop system shows these four phases.

2) Compare the evolutions of the number of viable bacteria and the total biomass of the population.

These two evolutions show different profiles in such phases where the growth conditions are not optimal. For instance, when the nutrient is exhausted and the culture enters the stationary phase, the energetic requirements are satisfied with the use of the bacterial own biomass.

3) Recognize the effect of the parameters for the fed-batch operating protocol.

A fed-batch operating protocol implies that there is a periodic renewal of part of the medium. The amount of input nutrient (fed_nutrient) and the frequency of this renewal (length_time_feed) affect the evolution of the bacterial population. The bacterial load tends to synchronize with the renewal characteristics: the population initially increase and/or decreases until it reaches a kind of stationary state with oscillations, where there is a kind of equilibrium between nutrient entrance and bacterial load. These oscillations are directly related with renewal frequency, and their size is related with the amount of nutrient that enters each time.

4) Keep viable bacteria over extended periods of time.

For many applications in industry it is desirable to have maintenance of viable bacteria over extended periods of time. In this case, the nutrient concentration and other conditions must remain constant, so that individual cells grow at a constant rate, fully acclimatised exponential rate. In practice, this is achieved by constant addition of fresh effluent to the growing bacteria and concomitant withdrawal of equal volumes of the growing bacterial culture. We achieve this with the continuous culture, a bioreactor with a continuous medium renewal, considering different percentages of culture removing (in_out_percent), and nutrient entrance from an external reservoir (out_reservoir_nutrient).

5) Choose a specific application in order to adapt this individual-based bacterial model to certain experimental conditions.

## EXTENDING THE MODEL

Many parts of the bacterial model could be sophisticated.

## NETLOGO FEATURES

## RELATED MODELS

## CREDITS AND REFERENCES

Ferrer, J., Prats, C., and López, D. (2008). Individual-based modelling: an essential tool for microbiology. Journal of Biological Physics, 34, 19-27.

Ginovart, M., López, D. and Valls, J. (2002) INDISIM, an individual based discrete simulation model to study bacterial cultures. Journal of Theoretical Biology, 214, 305-319.

## HOW TO CITE

GINOVART M., PRATS C. (2012)
“A Bacterial Individual-based Virtual Bioreactor to test Handling Protocols in a NetLogo Platform”.
In: I. Troch and F. Breitenecker (eds), Proceedings of the 7th Vienna International Conference on Mathematical Modelling - MATHMOD 2012 Vienna Full Papers CD Volume, ARGESIM Report no 35,ARGESIM-ASIM German Simulation Society, Wien, p 1495 – 1506. ISBN 978-3-901608-35-3. http://www.ifac-papersonline.net/Detailed/58745.html
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270

@#$#@#$#@
NetLogo 5.2.1
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180

@#$#@#$#@
0
@#$#@#$#@
