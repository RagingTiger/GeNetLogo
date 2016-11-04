#!/usr/bin/env python
'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Program: genetlogo
Description:
    This program searches a combination space of NetLogo simulation parameters
    in an effort to find the maximum/minimum value.
'''

# libraries
# import genalgo
import jvm

# banner for stdout
banner = '''
             _____      _   _      _   _
            |  __ \    | \ | |    | | | |
            | |  \/ ___|  \| | ___| |_| |     ___   __ _  ___
            | | __ / _ \ . ` |/ _ \ __| |    / _ \ / _` |/ _ \\
            | |_\ \  __/ |\  |  __/ |_| |___| (_) | (_| | (_) |
             \____/\___\_| \_/\___|\__\_____/\___/ \__, |\___/
                                                    __/ |
                                                   |___/
'''

# executable
if __name__ == '__main__':

    # print
    print '{0}'.format(banner)

    # start JVM
    print 'Starting Java Virtual Machine ...'
    with jvm.JVM(jvm.PRG) as jcode:

        # ready to rock n roll
        print 'Virtual Machine Started'

        # get results
        results = jcode.run_java_code(jvm.TST)
        print 'Results:'
        for val in results:
            print val

    # print 'Starting Genetic Algorithm ...'
