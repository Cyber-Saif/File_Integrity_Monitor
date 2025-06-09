import os, hashlib, json, logging, time

logging.basicConfig(level=logging.DEBUG, filename="integrity_logs.txt", format='%(asctime)s - [%(levelname)s] %(message)s',datefmt='%Y-%m-%d %H:%M:%S')


def hash_file(filepath):  
    # Open file, read bytes, generate SHA-256 hash  
        # Hashlib has a helper funtion for file like object
        #https://docs.python.org/3/library/hashlib.html
    with open(filepath,"rb") as read_file:
        digest = hashlib.file_digest(read_file, "sha256")
    
    return digest.hexdigest()


def create_baseline(directory):  
    baseline = {}  
    igonre = ["tmp/", "*.log"]
    #Adding each file into the baseline{} along with its hash value
    for file in os.listdir(directory): 
        
        if file in igonre:
            pass
        #concatenating the directory and file 
        else:
            file_location = os.path.join(directory, file)         
            baseline[file] = hash_file(file_location)  
    
    #Dumping the baseline{} into the JSON file to furthur transmit or store it
    with open("data.json", "w") as file:
        json.dump(baseline,file)

    return baseline

def integrity_check(directory):    
    
    if not os.path.exists("data.json"):  
        message = "[!] Baseline not found. Create one first!"
        logging.error(message)  
        print(message)
        
    if not os.path.exists(directory):  
        message = "[!] Target directory not found!"
        logging.error(message)
        print(message)
            
    with open("data.json", "r") as read:
        baseline_data = json.load(read)

    #Making a dictionary of current files
    current_files = {} 
    for c_file in os.listdir(directory):  
        check_file = os.path.join(directory, c_file)  
        current_files[c_file] = hash_file(check_file)
    
    for file_name in baseline_data:          
        if file_name not in current_files:  
            message = f"[-] File {file_name} was DELETED!"
            logging.warning(message)
            print(message)
            
    
    for file_name in current_files:
        if file_name not in baseline_data:  
            message = f"[-] NEW file detected: {file_name}!"
            logging.info(message)
            print(message)
        
        elif baseline_data[file_name] == current_files[file_name]:
            message = f"[+] Integrity of the file {file_name} is maintained!"
            logging.info(message)
            print(message)
        
        elif baseline_data[file_name] != current_files[file_name]:  
            message = f"[!] {file_name} was MODIFIED!"
            logging.critical(message)
            print(message)
   
    print()
    

def main():
    option = ""
    while option not in ['0','1','exit']:
        print("----------------------------------------------")
        print("Enter 0 if you want to create a new baseline \nEnter 1 to check file integrity \nOR type exit to quit the program")
        print("----------------------------------------------")

        option = input("\nEnter the option: ")

        if option == "0":
            integrity = create_baseline("D:\Code\GitCode\Integrity Monitor\To Monitor")
            messagex = f"[+] A new baseline has created\n"
            logging.info(messagex)
            print(f"\n{messagex}\n")
        
        elif option == "1":
            integrity_check("D:\Code\GitCode\Integrity Monitor\To Monitor")
        
        elif option == "exit":
            exit()

        else:
            pass

if __name__ == "__main__":
    try:
        main()
        run_program = input("Do you want to continue with this program (y/n): ")
        while True:
            if run_program == 'y':
                main()
            else:
                print("\n[-] Exiting the program........")
                exit()
    except KeyboardInterrupt:
        print(f"\n\n[!] Keyboard Interrup\n[-] Exiting the program........")
    except Exception as e:
        print(e)
        e = f"\nError occured while running the script 1\n {e}"
        logging.critical(e)
        
        
    