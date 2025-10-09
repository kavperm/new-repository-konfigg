import os
import socket
import shlex
import argparse

def get_prompt():
    user = os.getenv('USER')
    hostname = socket.gethostname()
    return f"{user}@{hostname}:~$ "

def act(command):
    args = shlex.split(command)
    
    if not args:
        return ""
        
    if args[0] == "exit":
        return "exit"
    elif args[0] == "ls":
        return f"ls: {args[1:]}"
    elif args[0] == "cd":
        return f"cd: {args[1:]}"
    else:
        return f"{args[0]}: command not found"


parser = argparse.ArgumentParser()
parser.add_argument("--path", "-p", help="Путь к физическому расположению VFS")
parser.add_argument("--script", "-s", help="Путь к стартовому скрипту")
args = parser.parse_args()

print("---------------------------")
print(f"Путь VFS = {args.path}")
print(f"Путь скрипт = {args.script}")
print("---------------------------")


if args.script:
    with open(args.script, "r", encoding="utf-8") as f:
        for i in f.readlines():
            i = i.strip()
            if not i or i.startswith("#"):
                continue
            print(get_prompt() + i)  
            result = act(i)
            if result == "exit":
                exit()
            print(result) 

while True:
    a = input(get_prompt())
    result = act(a)
    if result == "exit":
        break
    print(result)