import socket
import struct
import time
from threading import Thread


class Sniffer( Thread ):
    def __init__( self , first_con , lock ):
        super( ).__init__( )
        self.first_con       =  first_con
        self.lock            =  lock
        self.is_running      =  True


    
    def mac_format( mac ):
        mac = map( '{:02x}'.format , mac )
        return ''.join( mac ).upper( )


    def ipv4_format( address ):
        return '.'.join( map( str , address ) )


    def ethernet_dissect( ethernet_data ):
        dst_mac, scr_mac, protocol  =  struct.unpack( '!6s6sH' , ethernet_data[:14] )
        return Sniffer.mac_format( dst_mac ), Sniffer.mac_format( scr_mac ), socket.htons( protocol ), ethernet_data[14:]


    def ipv4_dissect( ip_data ):
        ip_protocol, scr_ip, tar_ip = struct.unpack( '!9x B 2x 4s 4s', ip_data[:20] )
        return ip_protocol, Sniffer.ipv4_format( scr_ip ), Sniffer.ipv4_format( tar_ip ), ip_data[20:]


    def tcp_dissect( transport_data ):
        scr_port, dst_port  =  struct.unpack( '!HH' , transport_data[:4] )
        return scr_port, dst_port


    def udp_dissect( transport_data ):
        scr_port, dst_port  =  struct.unpack( '!HH' , transport_data[:4] )
        return scr_port, dst_port


    def icmp_dissect( transport_data ):
        icmp_type, icmp_code  =  struct.unpack( '!BB' , transport_data[:2] )
        return icmp_type, icmp_code


    def run( self ):
        packets  =  socket.socket( socket.PF_PACKET , socket.SOCK_RAW , socket.htons( 0x0800 ) )
        packets.settimeout( 5 )
        
        while self.is_running:

            try:
                ethernet_data, address  =  packets.recvfrom( 65536 )

            except socket.timeout:
                continue

            dest_mac, src_mac, protocol, ip_data  =  Sniffer.ethernet_dissect( ethernet_data )

            if protocol == 8:

                ip_protocol, src_ip, dest_ip, transport_data = Sniffer.ipv4_dissect( ip_data )
                contact  =  False

                if ip_protocol == 6: 

                    src_port, dest_port  =  Sniffer.tcp_dissect( transport_data )
                    contact = True

                elif ip_protocol == 17:

                    src_port, dest_port  =  Sniffer.udp_dissect( transport_data )
                    contact  =  True

                if contact:
                    key  =  ( src_ip , dest_ip , dest_port )


                    with self.lock:
                        
                        self.first_contacts[key]  =  time.time( ) 
