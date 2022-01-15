import socket
import binascii
import csv
from deencoding import build_message, decode_message
from collections import OrderedDict

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONENCTED"
SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)

counter_dic = {}
cache_dic = {}

visited = []
queue = []

def send(msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    client.close()


def send_udp_message(message, address, port):
    message = message.replace(" ", "").replace("\n", "")
    server_address = (address, port)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(server_address)
    try:
        client.sendto(binascii.unhexlify(message), server_address)
        data, _ = client.recvfrom(4096)
    finally:
        client.close()
    return binascii.hexlify(data).decode("utf-8")


addresses = []
address_dict = {}
# file1 = open("cache.csv", "r+")
# writer = csv.writer(file1)
file2 = open("count.txt", "r+")
# tmp1 = file1.readlines()
tmp2 = file2.readlines()
for i in range(len(tmp2)):
    if tmp2[i].strip() == '':
        continue
    tmp2[i] = tmp2[i].split(maxsplit=1)
    counter_dic[tmp2[i][0]] = tmp2[i][1]


with open('cache.csv', "r+") as file1:
    reader = csv.reader(file1, delimiter=',')
    for row in reader:
        cache_dic[row[0]] = row[1]

with open('adresses.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # line_count = 0
    for row in csv_reader:
        addresses.append(row[0])

address = input("Enter an address :")
# type = input("Enter type record : ")


if address not in cache_dic:
    if address not in counter_dic:
        # cache_dic[address] = ''
        counter_dic[address] = 0
    # else:
    #     counter_dic[address] = str(int(counter_dic[address]) + 1)
    addresses.append(address)
    message = build_message(address=address)
    print(f"[Request] : {message}")
    response = send_udp_message(message, "1.1.1.1", 53)

    print(f"[RESPONSE] : {response}")
    decoded_message, ip, answers, visited, queue = decode_message(response, visited, queue)
    queue.remove(queue[0])
    # print(f"[DECODED RESPONSE] : {decoded_message}")
    print(ip)
    while answers == 0:
        print(ip)
        if ip == 0 :
            print("NOT FOUND")
            break
        decoded_message, ip, answers, visited, queue = decode_message(send_udp_message(message, ip, 53), visited, queue)
        queue.remove(queue[0])
    if answers > 0:
        counter_dic[address] = str(int(counter_dic[address]) + 1)
        decoded_message = ip
        print(f"[DECODED RESPONSE] : {decoded_message}")

    # print(ip)
    if int(counter_dic[address]) > 2:
        cache_dic[address] = decoded_message
        # file1.write(str(address + " " + str(cache_dic[address]) + "\n"))
        with open("cache.csv", 'r+', encoding="UTF8", newline='')as file1:
            writer = csv.writer(file1)
            writer.writerow([address , cache_dic[address]])
else:
    print(f"[DECODED RESPONSE FROM CACHE] : {cache_dic[address]}")

file2 = open('count.txt', "w")
for i in counter_dic:
    # if i in cache_dic :
    #     file1.write(str(i + " " + str(cache_dic[i])))
    file2.write(str(i + " " + str(counter_dic[i]) + "\n"))

#reading from csv file
# print(addresses)
# for addr in addresses :
#     print(f"For address {addr} : ")
#     message = build_message(address=addr)
#     print(f"[Request] : {message}")
#     response = send_udp_message(message, "a.root-servers.net", 53)
#     print(f"[RESPONSE] : {response}")
#     print(f"[DECODED RESPONSE] : {decode_message(response)}")
    # address_dict[addr[0]] = decode_message(response)
    # addr.append(decode_message(response))



# with open('adresses.csv') as csv_file:
#     csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     print(address_dict)
#     csv_writer.writerow(address_dict)
    # for row in address_dict:
    #     print(row)
    #     if row not in csv_reader :
    #         csv_writer.writerow(row)
