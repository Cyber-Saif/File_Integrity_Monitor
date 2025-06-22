import hashlib, time, json, pathlib, tempfile, time
from colorama import Fore, Style, Back

#######  To Enable Logging & Export Logs
#import logging, threading
#logging.basicConfig(level=logging.DEBUG, filename="integrity_logs.txt",
#format='%(asctime)s - [%(levelname)s] %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

class IntegrityMonitor:
    def __init__(self):
        self.Exec_dump = True
        self.temp_dir_path = pathlib.Path(tempfile.gettempdir())
        self.temp_path = self.temp_dir_path / '.temp-baseline.json'
        

    def create_hash(self, file):
        """Take files as an input and return the hash"""
        try:
            with open(file, "rb") as f:
                return hashlib.file_digest(f, 'sha256').hexdigest()
        except AttributeError:
            sha256_hash = hashlib.sha256()
            with open(file, "rb") as f:
                while chunk := f.read(4096):  # Read in 4k chunks
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"An error occured while hashing the file\n{e}")


    def baseline_dump(self, data):
        """Dumps the file:hash dictionary to the JSON file"""
        if self.Exec_dump:
            with open('baseline.json', "w") as d:
                json.dump(data, d, indent=4)

        with open(self.temp_path, "w") as td:
            json.dump(data, td, indent=4)

        self.Exec_dump = False
        return data


    def directory_enumeration(self, directory_location, data_dump=None):
        """Enumerate the folders and sub-folders to find files &
        add key:values in the dictionary"""
        data_dump = {}
        directory_location = pathlib.Path(directory_location)
        for file in directory_location.rglob("*"):
            if file.is_file() and not file.is_symlink():
                try:
                    resolved_path = file.resolve()  # Check for path traversal
                    # Ensure file is within monitored dir
                    if directory_location in resolved_path.parents:
                        data_dump[file.name] = self.create_hash(file)

                except Exception as e:
                    print(e)
                    continue
        return data_dump


    def user_directory_options(self, to_write=False):
        """User menu to choose the directory to monitor"""
        usr_option = ''
        directory_location = 'none'

        directory_location = pathlib.Path(directory_location)
        current_directory = pathlib.Path.cwd()
        return_directory = None

        #### User Menu #####
        while usr_option not in ['0', '1']:
            print(f"{Fore.RESET}{'-'*50}")
            usr_option = str(input(f"{Fore.BLACK}{Back.WHITE}[0]{Back.RESET+Fore.RESET}"
                                   f" To run this program in the current directory\n{Fore.BLACK}"
                                   f"{Back.WHITE}[1]{Back.RESET+Fore.RESET} To specify a path\n"
                                   f"{'-'*50}\n{Fore.CYAN}Enter the number [0/1]:{Fore.RESET}"))

        # User Specified Path [Option 1]
        if usr_option == '1':
            print("[+] Monitoring...")
            while not directory_location.exists():
                directory_location = input(r"Enter a valid path: ")
                directory_location = pathlib.Path(directory_location)

            data_dump = self.directory_enumeration(directory_location)
            if to_write is True:
                self.baseline_dump(data_dump)

            return_directory = directory_location

        # Default option, current directory
        elif usr_option == '0':
            print("[+] Monitoring...")
            data_dump = self.directory_enumeration(current_directory)
            if to_write is True:
                self.baseline_dump(data_dump)

            return_directory = current_directory

        return return_directory


    def integrity_check(self, location):
        baseline_location = location / 'baseline.json'
        baseline_exists = False
        baseline_data = None
        local_time = time.ctime()

        real_time_list = self.directory_enumeration(location)

        if baseline_location.exists():
            baseline_exists = True

            with open(self.temp_path, "r") as dr:
                baseline_data = json.load(dr)

            for loaded_file, loaded_hash in baseline_data.items():
                if loaded_file not in real_time_list:
                    print(f"{Fore.RED}[-] {loaded_file} was deleted ! [{local_time}]")

            for file, hashes in real_time_list.items():
                if file not in baseline_data.keys():
                    if file in ['baseline.json', '.baseline.json']:
                        pass
                    else:
                        print(f"{Fore.MAGENTA}[+] New file created '{file}' [{local_time}]")

                elif real_time_list[file] == baseline_data[file]:
                    pass

                elif real_time_list[file] != baseline_data[file]:
                    if file in ['baseline.json', '.temp-baseline.json']:
                        pass
                    else:
                        print(f"{Fore.LIGHTYELLOW_EX}[!] {file} was modified ! [{local_time}]")

        self.baseline_dump(real_time_list)

        return real_time_list, baseline_data, baseline_exists


    def baseline_update_initial_startup(self):
        update_baseline = ''
        tp_status = False

        #location,real_time_data,baseline_data,baseline_exist=integrity_check(forward_to_write=False)

        if self.temp_path.exists():
            tp_status = True

        while update_baseline not in ['yes', 'no']:
            update_baseline = str(input(f"{Fore.LIGHTGREEN_EX}"
                                        f"Do you want to update the baseline first?\n"
                                        f"[yes/no]:{Fore.LIGHTYELLOW_EX}"))

            if update_baseline in 'yes':
                ##### Will update the baseline
                self.Exec_dump = True
                user_selected_directory = self.user_directory_options(to_write=True)
                baseline_exist = self.integrity_check(user_selected_directory)

            elif update_baseline in 'no':
                ##### Will not update the baseline
                user_selected_directory = self.user_directory_options()
                baseline_exist = self.integrity_check(user_selected_directory)

                if not baseline_exist:
                    print(f"[-] Program did not find a baseline, one will be created")
                    user_selected_directory = self.user_directory_options(to_write=True)
                else:
                    pass

        return update_baseline, user_selected_directory

    def exit_save(self, directory_location):
        to_save = ''

        while to_save not in ['yes', 'y', 'no', 'n']:
            to_save = input("Do you want to update the baseline before quitting the program?: ")

        if to_save in ['yes', 'y']:
            self.Exec_dump = True
            print("[+] Baseline updated !")
            self.integrity_check(directory_location)

        if self.temp_path.exists():
            self.temp_path.unlink()  # Clean up temp file
        else:
            exit()

    def monitor_loop(self, dir_location):
        while True:
            self.integrity_check(dir_location)
            time.sleep(3)


    def main(self):
        try:
            with open('baseline.json', "r") as br:
                read_d = json.load(br)
                self.Exec_dump = False
                self.baseline_dump(read_d)

            user_choice, dir_location = self.baseline_update_initial_startup()
            self.monitor_loop(dir_location)

        except KeyboardInterrupt:            
            print(f"\n\n{Fore.RED+Style.BRIGHT}"
                  f"[!] Keyboard Interrup\n[-] Exiting the program........"
                  f"{Fore.RESET+Back.RESET+Style.RESET_ALL}\n")
        
        finally:
            self.exit_save(dir_location)


if __name__ == "__main__":
    monitor = IntegrityMonitor()
    monitor.main()
    