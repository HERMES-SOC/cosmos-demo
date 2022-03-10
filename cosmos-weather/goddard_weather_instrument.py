###############################################################################
# Goddard Weather Instrument Emulator over UDP for COSMOS Training
#
# Notes:
#   TELEMETRY
#   1. Generates fake weather data for COSMOS training
#   2. Creates a packet dictionary required to structure a python packet
#   3. Iterates between unix timestamp between 1/1/2022 and 12/31/2022
#   4. Takes current iterative timestamp and applies formula to range weather by the current hour (0-24)
#   4a. range is low during "night" hours and high during "peak day" hours 62-77 *F
#   5. Also includes goddard longitude and latitude based on google maps coordinates
#
#   COMMAND
#   1. Opens port to listen for "TO_ENABLE" command
#   2. Matches "TO_ENABLE" bytes data against CCSDS Headers, 127.0.0.1, and 8005 as contents
#   2a. If match then reply back with CCSDS Headers and value of 1, otherwise 0
#
# License:
#   Written by Timothy Walker
#
###############################################################################

import socket
import struct
import time
import threading
import datetime
import math 

packet_args_list = {
    'GODDARD_WEATHER_TLM': {
        'app_id': 0x8005,
        'length': 128,
        'structure': "!HHHIH" + "fffI",
        'args': [               #PACKET fffI (128)
            38.99495,           #Latitude
            -76.852344,         #Longitude
            0,                  #Temperature
            0                   #Timestamp
        ]        
    },
}

def send_packet(packet_name, sequence_cnt):
    try:
        print(packet_name)
        # ! big endian
        # B unsigned char 1 byte 8 bits
        # H unsigned short 2 byte 16 bits
        # L unsigned long 4 byte 32 bits
        # I unsigned int 4 byte 32 bits
        # Q unsigned long long 8 bytes 64 bits        
        tlm_data = struct.pack(
            packet_args_list[packet_name]['structure'],
            #CCSDS HEADER HHHIH (3x 16 UINT, 1x 32 UINT, 1x 16 UINT)
            packet_args_list[packet_name]['app_id'],            #CCSDS_STREAMID 16
            sequence_cnt,                                       #CCSDS_SEQUENCE 16
            packet_args_list[packet_name]['length'],            #CCSDS_LENGTH 16
            0,                                                  #CCSDS_SECONDS (secondary) 32
            0,                                                  #CCSDS_SUBSECS (secondary) 16
            #PACKET
            *packet_args_list[packet_name]['args']
        )
        print(tlm_data)
        sock_tlm.sendto(tlm_data, (UDP_SEND_IP, UDP_PORT_SEND))  # send the packet 
        return 0
    except:
        return 1
       

def send_telemetry():
    packet_name = 'GODDARD_WEATHER_TLM'
    sequence_cnt = 1    
    while True:
        try:
            start = 1640995200      #1/1/2022 0:00:00
            end = 1672531199        #12/31/2022 12:59:59
            for time_i in range(start, end, 900):       #15 minute interval of 2022
                temp_val = 8 * math.sin(((datetime.datetime.fromtimestamp(time_i).hour)/(4)) + 4.8) + 70        #calculate range temp based on current hour
                packet_args_list[packet_name]['args'][3] = time_i                                               #update timestamp
                packet_args_list[packet_name]['args'][2] = temp_val                                             #update temperature
                r = send_packet(packet_name, sequence_cnt)
                if r:
                    print('There was an error sending the packet')
                time.sleep(1)  # wait one second before sending the next packet
                sequence_cnt = sequence_cnt + 1
        except:
            print('There is a fatal error with sending the Telemetry.')

def get_commands():
    try:
        while True:
            cmd_data, addr = sock_cmd.recvfrom(1024)
            print('Recieved Data: ')
            print(cmd_data)
            if cmd_data == b'\x80\x11\xc0\x00\x00\x11\x06\x9b127.0.0.1\x00\x00\x00\x00\x00\x00\x00\x1fE':
                cmd_resp = struct.pack(
                    "!HHHIH" + "B",
                    #CCSDS HEADER HHHIH (3x 16 UINT, 1x 32 UINT, 1x 16 UINT)
                    0x8010,                             #CCSDS_STREAMID 16
                    1,                                  #CCSDS_SEQUENCE 16
                    8,                                  #CCSDS_LENGTH 16
                    0,                                  #CCSDS_SECONDS (secondary) 32
                    0,                                  #CCSDS_SUBSECS (secondary) 16
                    #PACKET
                    1
                )
                print(cmd_resp)
                sock_tlm.sendto(cmd_resp, (UDP_SEND_IP, UDP_PORT_SEND))  # send the packet   
            else:       
                cmd_resp = struct.pack(
                    "!HHHIH" + "B",
                    #CCSDS HEADER HHHIH (3x 16 UINT, 1x 32 UINT, 1x 16 UINT)
                    0x8010,                             #CCSDS_STREAMID 16
                    1,                                  #CCSDS_SEQUENCE 16
                    8,                                  #CCSDS_LENGTH 16
                    0,                                  #CCSDS_SECONDS (secondary) 32
                    0,                                  #CCSDS_SUBSECS (secondary) 16
                    #PACKET
                    0                                   #Send invalid response
                )
                print(cmd_resp)
                sock_tlm.sendto(cmd_resp, (UDP_SEND_IP, UDP_PORT_SEND))  # send the packet                         
            time.sleep(1)
    except:
        print('There is a fatal error with the command section.')

if __name__ == '__main__':
    sock_cmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock_tlm = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    UDP_REC_IP = input("Enter IP Address of Machine: ")   #Assigned IP of machine
    UDP_SEND_IP = '127.0.0.1' #COSMOS: compose.yaml file opening port 8005 to localhost
    UDP_PORT_REC = 8006
    UDP_PORT_SEND = 8005
    sock_cmd.bind((UDP_REC_IP,UDP_PORT_REC))
    thread1 = threading.Thread(target=send_telemetry)
    thread1.start()
    print('Thread1 started')
    thread2 = threading.Thread(target=get_commands)
    thread2.start() 
    print('Thread2 started')
