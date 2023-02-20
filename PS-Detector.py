import threading
from Sniffer              import Sniffer
from DictCleaner          import DictCleaner
from FanOutRateCalculator import FanOutRateCalculator



def detect_ps( ):

    first_contacts  =  dict( )
    lock            =  threading.Lock( )

    sniffer                  =  Sniffer( first_contacts , lock )
    cleanup                  =  DictCleaner( first_contacts , lock )
    fan_out_rate_calculator  =  FanOutRateCalculator( first_contacts , lock )

    sniffer.start( )
    cleanup.start( )
    fan_out_rate_calculator.start( )

    print( '[+] Enter \'x\' to Stop Detecting' )
    while True:
        x  =  input( )
        if x in 'xX':
            print( '[*] Terminating Threads...' )
            break

    sniffer.is_running                  =  False
    cleanup.is_running                  =  False
    fan_out_rate_calculator.is_running  =  False

    sniffer.join( )
    cleanup.join( )
    fan_out_rate_calculator.join( )

    return


if __name__ == '__main__':
    detect_ps( )