import socket
import struct

# server = socket.gethostbyname(socket.gethostname())
# ADDR = (server, 16011)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# client.connect(ADDR)

def checksock() -> bool:
    try:
        client.send(bytes('SOMETHING', 'utf-8'))
        r = client.recv(256)
        return True
    except socket.error as e:
        print("Connection failed: ", e)
        client.close()
        exit(0)
    # return True


while True:
    print("============Initialize socket============")
    ip = input("input IP address: ")
    port = int(input("input port number: "))
    if port != 16011:
        print("Error: connection is not built, try again")
        continue
    ADDR = (ip, port)
    try:
        client.connect(ADDR)
    except:
        print("Error: connection is not built, try again")
        continue
    break

while True:
    command = input("Input Command: ")
    try:
        client.send(bytes(command, 'utf-8'))
    except socket.error as e:
        print("Connection failed: ", e)
        client.close()
        exit(0)
    if command == "POST_STRING":
        n = 0
        print("============== Content (Type a lone '&' to end message) ==============")
        while command != "&":
            command = input("client: ")
            client.send(bytes(command, 'utf-8'))
            n += 1
        response = client.recv(256)
        print(response.decode('utf-8'))
        print("---")
        print("Sent " + str(n) + " messages to (IP address:" + socket.gethostbyname(
            socket.gethostname()) + ", port number:" + "16011" + ")")
        if checksock():
            print("Connect status: OK")
        print("Send status: OK")
        print("---")
        print("===========================next command===============================")
    elif command == "POST_FILE":
        response = client.recv(256)
        print(response.decode('utf-8'))
        command = input("client: ")
        try:
            with open(command, "rb") as f:
                print("Transfer file absolute path: " + command)
                size = len(f.read())
                f.seek(0)
                if size > 256:
                    print("The file is too large")
                    continue
                send = struct.pack('128sl', command.encode('utf-8'), size)
                client.send(send)

                while True:
                    data = f.read(10)
                    client.send(data)
                    if not data:
                        break

                response = client.recv(256)
                print(response.decode('utf-8'))
        except:
            print("Cannot find the file")
            client.send(bytes("close", 'utf-8'))
            response = client.recv(256)
            print(response.decode('utf-8'))
        print("===========================next command===============================")
    elif command == "GET":
        print("---Received Messages---")
        response = client.recv(256)
        while response.decode('utf-8') != 'server: &':
            print("client: " + response.decode('utf-8'))
            response = client.recv(256)
        print("client: " + response.decode('utf-8'))
        print("---")
        print("(IP address:" + socket.gethostbyname(socket.gethostname()) + ", port number:" + "16011" + ")")
        if checksock():
            print("Connect status: OK")
        print("Send status: OK")
        print("---")
        print("===========================next command===============================")
    elif command == "EXIT":
        response = client.recv(256)
        print(response.decode('utf-8'))
        client.close()
        break
    else:
        response = client.recv(256)
        print(response.decode('utf-8'))
