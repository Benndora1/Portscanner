# import socket  # Used for network connectivity
# import time  # Used for timing
# import argparse  # Used for command-line argument parsing
# import ipaddress  # Used for IP address manipulation


# def tcp_scanner(ip, port):
#     try:
#         tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         tcp_sock.connect((ip, port))
#         return True
#     except:
#         return False
#     finally:
#         tcp_sock.close()


# def port_scan(cidr, delay_per_scan, ports):

#     network = ipaddress.IPv4Network(cidr)

#     for ip in network.hosts():
#         for port in ports:
#             if tcp_scanner(str(ip), port):
#                 print('[*] Port {}/tcp is open on {}'.format(port, str(ip)))
#             time.sleep(delay_per_scan)


# parser = argparse.ArgumentParser(description='TCP port scanner')
# parser.add_argument('cidr', metavar='CIDR', type=str, help='network address range in CIDR notation')
# parser.add_argument('--ports', metavar='PORT', type=int, nargs='+', help='list of ports to scan (default is 1-1023)', default=list(range(1, 1024)))
# parser.add_argument('--delay', metavar='DELAY', type=float, help='time to wait (in milliseconds) between every two consecutive scans (default is 1000ms)', default=1000)
# args = parser.parse_args()

# port_scan(args.cidr, args.delay / 1000, args.ports)

# Imports
import socket # Used for network connectivity
import time   # Used for timing




def tcp_scanner( target , port ):
    try:
        tcp_sock  =  socket.socket( socket.AF_INET , socket.SOCK_STREAM )
        tcp_sock.connect( ( target , port ) )
        return True
    except:
        return False
    finally:
        tcp_sock.close( )




def port_scan( ):
    
    target = input('[+] Enter Target IP: ')
    delay_per_port = float(input('[+] Enter Delay Per-Port Scanned (Seconds): '))
    for portNumber in range( 1 , 2048 ):
        if tcp_scanner( target , portNumber ):
            print( '[*] Port {}/tcp is open'.format( portNumber ) )
        time.sleep( delay_per_port )



if __name__ == '__main__':
    port_scan( )