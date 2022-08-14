import atexit
from functools import partial
import sys
import os
import subprocess
import re
from threading import Timer

from methods import param_dict, colorcode, beforeexit, push, help, listenForKeys, customexit, setbranch

if "windows" in platform().lower():
        os.system('cls')


atexit.register(beforeexit)

""" 
The needed parameters are:
- folder -> default: _currentdir
- branch -> default: main
- commit message template -> format `message-{uuid}`
- interval
"""

args = sys.argv[1:]

""" Check if the any help is needed else parse the arguments """
if "--help" in args:
    help()
    customexit()
else:
    print('=============== AUTO-PUSH is starting ===============')
    print('Press q at any point in time to quit')
    params = param_dict(args)


""" Setting the DIRECTORY """
dir = os.getcwd() if "--dir" not in params.keys() else params["--dir"]

""" Check the branch """
cur_branch = "main"

try:
    cur_branch = subprocess.check_output(["git", "-C", dir, "branch"])
except Exception as e:
    print("{error}".format(error=colorcode(repr(e), "white", "bg-red")))
    customexit()

regCheck = re.search(r"(\*\s((.*){2,}))", cur_branch.decode())

cur_branch = regCheck.group(2)



branch = cur_branch if "--branch" not in params.keys() else params["--branch"]

""" Commit message template """
commit_template = "auto-commit-#num#" if "--commit" not in params.keys() else params["--commit"]

""" Interval """
interval = 5
try:
    interval = 5 if "--interval" not in params.keys() else float(params["--interval"])
except ValueError:
    print("{error}".format(error=colorcode("Given --interval is not a number", "white", "bg-red")))
    customexit()
except Exception as e:
    print(f'ERROR: {e}')
    customexit()


print('\n')

""" SET UP THE BRANCH """
setbranch(dir, branch)


""" Check if there is a module to run before the every push"""
module = None
beforemethod = None

if "--before-mod" and "--before-method" in params.keys():
    try:
        sys.path.append(os.getcwd())
        module = __import__(params["--before-mod"])
        beforemethod = getattr(module, params["--before-method"])
        print("[LOG]: Found before-method")
    except Exception as e:
        print(f'ERROR IMPORTING before-method\n ****** \n{e} \n******')


""" Push periodically """
Timer(5, partial(push, commit_template, dir, branch, interval, beforemethod)).start()

""" Wait for key presses """
while True:
    key = input()
    listenForKeys(key)




    
