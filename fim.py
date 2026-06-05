import hashlib, time, json, pathlib, tempfile
#import logging, threading
from colorama import Fore, Style, Back

#logging.basicConfig(level=logging.DEBUG, filename="integrity_logs.txt",
#format='%(asctime)s - [%(levelname)s] %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

Exec_dump = True

temp_dir_path = pathlib.Path(tempfile.gettempdir())
temp_path = temp_dir_path.joinpath('.temp-baseline.json')


def create_hash(file):
    """Take files as an input and return the hash"""
    with open(file, "rb") as hs:
        hash_file = hashlib.file_digest(hs, "sha256")
    return hash_file.hexdigest()


def baseline_dump(data):
    """Dumps the file:hash dictionary to the JSON file"""
    global Exec_dump
    if Exec_dump:
        with open('baseline.json', "w") as d:
            json.dump(data, d, indent=4)

    with open(temp_path, "w") as td:
        json.dump(data,td, indent=4)

    Exec_dump = False
    return data


def directory_enumeration(directory_location, data_dump=None):
    """Enumerate the folders and sub-folders to find files &
    add key:values in the dictionary"""
    data_dump = {}
    directory_location = pathlib.Path(directory_location)
    # Modify directory_enumeration():
    for file in directory_location.rglob("*"):
        if file.is_file() and not file.is_symlink():
            try:
                resolved_path = file.resolve()  # Check for path traversal
                # Ensure file is within monitored dir
                if directory_location in resolved_path.parents:
                    data_dump[file.name] = create_hash(file)

            except Exception as e:
                print(e)
                continue
    return data_dump


def user_directory_options(to_write=False):
    """User menu to choose the directory to monitor"""
    usr_option = ''
    directory_location = 'none'

    directory_location = pathlib.Path(directory_location)
    current_directory = pathlib.Path.cwd()
    return_directory = None

    #### User Menu #####
    while usr_option not in ['0','1']:
        print(f"{Fore.RESET}{'-'*50}")
        usr_option = str(input(f"{Fore.BLACK}{Back.WHITE}[0]{Back.RESET+Fore.RESET}"
                               f" To run this program in the current directory\n{Fore.BLACK}"
                               f"{Back.WHITE}[1]{Back.RESET+Fore.RESET} To specify a path\n"
                               f"{'-'*50}\n{Fore.CYAN}Enter the number [0/1]:{Fore.RESET}"))

    # User Specified Path [Option 1]
    if usr_option == '1':
        while not directory_location.exists():
            directory_location = input(r"Enter a valid path: ")
            directory_location = pathlib.Path(directory_location)


        data_dump = directory_enumeration(directory_location)
        if to_write is True:
            baseline_dump(data_dump)

        return_directory = directory_location

    #Default option, current directory
    elif usr_option == '0':
        data_dump = directory_enumeration(current_directory)
        if to_write is True:
            baseline_dump(data_dump)

        return_directory = current_directory

    return return_directory


def integrity_check(location):
    baseline_location = pathlib.Path(location).joinpath('baseline.json')
    baseline_exists = False
    baseline_data = None

    real_time_list = directory_enumeration(location)

    if baseline_location.exists():
        baseline_exists = True

        with open(temp_path, "r") as dr:
            baseline_data = json.load(dr)

        for loaded_file, loaded_hash in baseline_data.items():
            if loaded_file not in real_time_list:
                print(f"{Fore.RED}[-] {loaded_file} was deleted !")

        for file, hashes in real_time_list.items():

            if file not in baseline_data.keys():
                if file in ['baseline.json', '.baseline.json']:
                    pass
                else:
                    print(f"{Fore.MAGENTA}[+] New file created '{file}'")

            elif real_time_list[file] == baseline_data[file]:
                pass

            elif real_time_list[file] != baseline_data[file]:
                if file in ['baseline.json', '.temp-baseline.json']:
                    pass
                else:
                    print(f"{Fore.LIGHTYELLOW_EX}[!] {file} was modified !")

    baseline_dump(real_time_list)

    return real_time_list, baseline_data, baseline_exists


def baseline_update_initial_startup():
    update_baseline = ''
    global Exec_dump
    tp_status = False
    #location, real_time_data, baseline_data, baseline_exist = integrity_check(forward_to_write=False)

    if temp_path.exists():
        tp_status = True

    while update_baseline not in ['yes','no']:
        update_baseline = str(input(f"{Fore.LIGHTGREEN_EX}"
                                    f"Do you want to update the baseline first?\n"
                                    f"[yes/no]:{Fore.LIGHTYELLOW_EX}"))

        if update_baseline in 'yes':
            ##### Will update the baseline
            Exec_dump = True
            user_selected_directory = user_directory_options(to_write=True)
            #real_time_data,baseline_data,baseline_exist=integrity_check(user_selected_directory)
            baseline_exist = integrity_check(user_selected_directory)

        elif update_baseline in 'no':
            ##### Will not update the baseline
            user_selected_directory = user_directory_options()
            #real_time_data,baseline_data,baseline_exist=integrity_check(user_selected_directory)
            baseline_exist = integrity_check(user_selected_directory)

            if baseline_exist is False:
                print(f"[-] Program did not find a baseline, one will be created")
                user_selected_directory = user_directory_options(to_write=True)
            else:
                pass

    return update_baseline, user_selected_directory # type: ignore


def exit_save(directory_location):
    global Exec_dump
    to_save = ''

    while to_save not in ['yes','y','no','n']:
        to_save = input("Do you want to update the baseline before quitting the program?: ")

    if to_save in ['yes','y']:
        Exec_dump = True
        print("[+] The baseline will be updated !")
        integrity_check(directory_location)

    if temp_path.exists():
        temp_path.unlink()  # Clean up temp file
    else:
        exit()


def main():
    global Exec_dump
    with open('baseline.json', "r") as br:
        read_d = json.load(br)
        Exec_dump = False
        baseline_dump(read_d)

    user_choice, dir_location = baseline_update_initial_startup()
    def monitor_loop():
        while True:
            integrity_check(dir_location)
            time.sleep(3)
    try:
        monitor_loop()

    except KeyboardInterrupt:
        exit_save(dir_location)
        print(f"\n\n{Fore.RED+Style.BRIGHT}"
              f"[!] Keyboard Interrup\n[-] Exiting the program........"
              f"{Fore.RESET+Back.RESET+Style.RESET_ALL}")


if __name__ == "__main__":
    main()
