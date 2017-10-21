import os
import sys

from storages import appdata_storage

BASE_DIR = "C:\\Users"


def set_username():

    if len(sys.argv) > 1:
        if os.path.isdir(os.path.join(BASE_DIR, sys.argv[1])):
            return sys.argv[1]

        else:
            print("[-] User %s not exists, using os name..." % sys.argv[1])

    user = os.getlogin()
    if os.path.isdir(os.path.join(BASE_DIR, user)):
        return user

    print("ERROR: User %s not exists" % user)
    exit(-1)


def check_file(dir, file):

    found = []

    if '*/' in file:
        path = os.path.join(dir, file[:file.index('*/')])
        filename = file[file.index('*/')+2:]

        if os.path.isdir(path):
            for f in os.listdir(path):
                dir_path = os.path.join(path, f)

                # only count directories
                if not os.path.isdir(dir_path):
                    continue

                full_path = os.path.join(dir_path, filename)
                if os.path.exists(full_path):
                    print("[+] Found - %s" % full_path)
                    found.append(full_path)

    elif file[-1] == '*':
        path = os.path.join(dir, file[:-1])
        if os.path.isdir(path):
            for f in os.listdir(path):
                full_path = os.path.join(path, f)

                # not count directories
                if os.path.isdir(full_path):
                    continue

                print("[+] Found - %s" % full_path)
                found.append(full_path)
        pass
    else:
        path = os.path.join(dir, file)
        if os.path.exists(path):
            print("[+] Found - %s" % path)
            found.append(path)

    return found


def run():
    username = set_username()
    base_dir = os.path.join(BASE_DIR, username)

    for storage in appdata_storage:
        name = storage["name"]
        dir = os.path.join(base_dir, "Appdata")
        dir = os.path.join(dir, storage["dir"])
        files = storage["files"]

        print("[*] Searching for - %s" % name)

        if not os.path.isdir(dir):
            continue

        for file in files:
            check_file(dir, file)

if __name__ == '__main__':
    run()