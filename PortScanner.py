import socket
import time
import ipaddress

# Define the TCP scanner function
def tcp_scanner(port, target):
    try:
        # Create a TCP socket using the socket module
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Try to connect to the target on the specified port
        tcp_sock.connect((target, port))

        # Close the socket
        tcp_sock.close()

        # If the connection is successful, return True
        return True
    except socket.error:
        # If the connection is unsuccessful (i.e., the port is not open), return False
        return False


# Define the UDP scanner function
def udp_scanner(target, port):
    try:
        # Create a UDP socket using the socket module
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Set a timeout for the socket
        udp_sock.settimeout(2.0)

        # Send a UDP packet to the target on the specified port
        udp_sock.sendto(bytes("NOTHING", "utf-8"), (target, port))

        # If a response is received, store it and the address in the response and addr variables
        response, addr = udp_sock.recvfrom(1024)

        # If the response is not None, return True (indicating that the port is open)
        if response != None:
            return True
        return False
    except:
        # If no response is received, print a message indicating that the port may be open but not responding
        print('no response from udp port {}. Port may be open but not responding.'.format(port))


# Define the main function
def main():
    # Prompt the user for the target network address range in CIDR notation and the waiting time in milliseconds
    target_network = input("[+] Enter Target Network in CIDR Notation (e.g. 192.168.1.0/24): ")
    wait_time = int(input("[+] Enter Waiting Time Between Scans in Milliseconds: "))

    # Parse the network address range
    target_network = ipaddress.ip_network(target_network)

    # Scan TCP and UDP ports in the target network address range
    for ip_address in target_network.hosts():
        ip_address_str = str(ip_address)
        for portNumber in range(1, 1024):
            # Use the tcp_scanner function to check if the port is open
            if tcp_scanner(portNumber, ip_address_str):
                # If the port is open, print a message indicating the IP address, port number, and the protocol (TCP)
                print('[*] IP', ip_address_str, 'Port', portNumber, 'tcp', 'is open')

            # Use the udp_scanner function to check if the port is open
            if udp_scanner(ip_address_str, portNumber):
                # If the port is open, print a message indicating the IP address, port number, and the protocol (UDP)
                print('[*] IP', ip_address_str, 'Port', portNumber, 'udp', 'is open')

            # Wait for the specified amount of time before scanning the next port on the same IP address
            time.sleep(wait_time / 1000.0)

# If the script is run as the main module, call the main function
if __name__ == "__main__":
    main()
