import sys
import os
import re
from random import randint



def randomname():
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    rname = ""
    for i in range(12):
        rname += charset[randint(1, len(charset))]
    return rname


def errno(msg):
    usage()
    print("Error: "+msg+"! Exiting...")
    exit(-1)


def usage():
    print(
        "Usage: python ce-antidetect.py --CE-dir <ce-dir> [--new-name <new-name>] [--backup]")
    print("     Whereas:")
    print("          <ce-dir> is the folder that you installed Cheat Engine to")
    print("          <new-name> is the new name to replace with 'Cheat Engine', 'cheatengine'..etc")
    print("                         (Leave out this to get a random name)")
    print("          --backup: make a Cheat Engine backup (eg: cheatengine.exe.bak)\n")


if len(sys.argv) < 3:
    errno("not enough arguments")


ce_dir = ""
newname = ""
backup = False


for i in range(len(sys.argv[1:-1])):
    if(sys.argv[i] == "--CE-dir" and os.path.isdir(sys.argv[i+1])):
        ce_dir = sys.argv[i+1]
    if(sys.argv[i] == "--new-name" and len(sys.argv[i+1]) == 12):  # and len(sys.argv[i+1])==12
        newname = sys.argv[i+1]
if("--backup" in sys.argv):
    backup = True


if(ce_dir == ""):
    errno("invalid Cheat Engine directory")
print("#DEBUG" + newname)
if not newname:
    opt = input("New name length not match!\nDo you want to set a random name?(Y/n)")
    if opt == "Y":
        newname = randomname()
    else:
        errno("invalid new name")

print("Patching CE at %s with new name = %s " %
      (ce_dir, newname)+" and with backup"*backup)
CEregex1 = re.compile("^(Cheat Engine)(.*)(exe)$")
CEregex2 = re.compile("^(cheatengine)(.*)(exe)$")

toPatch = []
for file in os.listdir(ce_dir):
    if CEregex1.search(file) != None and CEregex2.search(file) != None:
        print("Found file: %s" % file)
        toPatch.append(file)
        if backup:
            print("Making backup of "+ file)
            os.system('copy "%s" "%s"' % (os.path.join(ce_dir, file), os.path.join(ce_dir, file)+".bak"))
        #modify binary
        original_bin = open(file,"rb").read()
