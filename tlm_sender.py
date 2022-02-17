import socket
import struct
import time
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

packet_value = 0
packet_flag = True
identifier = 1
MAX_TEMP = 2 ** 4 - 1

while True:

    # random temperature
    temperature1 = random.randint(0, MAX_TEMP)
    temperature2 = random.randint(0, MAX_TEMP)
    # put the 4 bit temperature together into an 8 bit value
    t = (temperature1 << 4) & 0xFF | (temperature2 & 0xF)

    print(
        "id={0} value={1} flag={2} temp1={3} temp2={4}".format(
            identifier, packet_value, packet_flag, temperature1, temperature2
        )
    )

    # ! big endian
    # B unsigned char 1 byte 8 bits
    # H unsigned short 2 byte 16 bits
    # Q unsigned long long 8 bytes 64 bits

    data = struct.pack(
        "!BHBBQ",
        identifier,
        packet_value,
        packet_flag,
        t,
        283686952306183,  # 1,2,3,4,5,6,7 in bits
    )

    sock.sendto(data, ("127.0.0.1", 8081))  # send the packet

    # update some of the values for the next packet
    packet_flag = not packet_flag  # flip the bool
    packet_value += 1  # increase the packet value
    time.sleep(1)  # wait one second before sending the next packet

