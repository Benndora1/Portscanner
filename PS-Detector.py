from Sniffer  import Sniffer             # Import the Sniffer class from Sniffer module
from DictCleaner import DictCleaner      # Import the DictCleaner class from DictCleaner module
from FanOutRateCalculator import FanOutRateCalculator  # Import the FanOutRateCalculator class from FanOutRateCalculator module
import threading                        # Import threading module

def detect_ps( ):
    # Initialize a dictionary to keep track of the first contacts with the IP addresses
    first_contacts  =  dict( )
    # Initialize a lock object to provide synchronization when multiple threads access the dictionary
    lock            =  threading.Lock( )

    # Create instances of Sniffer, DictCleaner, and FanOutRateCalculator classes, passing in the first_contacts and lock objects
    sniffer                  =  Sniffer( first_contacts , lock )
    cleanup                  =  DictCleaner( first_contacts , lock )
    fan_out_rate_calculator  =  FanOutRateCalculator( first_contacts , lock )

    # Start the Sniffer, DictCleaner, and FanOutRateCalculator threads
    sniffer.start( )
    cleanup.start( )
    fan_out_rate_calculator.start( )

    # Prompt the user to enter 'x' to stop detecting
    print( '[+] Enter \'x\' to Stop Detecting' )
    while True:
        x  =  input( )
        if x in 'xX':
            # If the user enters 'x', terminate the threads
            print( '[*] Terminating Threads...' )
            break

    # Set the is_running flag of each thread to False to signal them to stop
    sniffer.is_running                  =  False
    cleanup.is_running                  =  False
    fan_out_rate_calculator.is_running  =  False

    # Wait for the threads to terminate
    sniffer.join( )
    cleanup.join( )
    fan_out_rate_calculator.join( )

    return

if __name__ == '__main__':
    detect_ps( )
