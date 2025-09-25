import os
import socket
import shlex

def get_prompt():
    user = os.getenv('USER')
    hostname = socket.gethostname()
    return f"{user}@{hostname}:~$ "

while True:
        input_line = input(get_prompt())
        args = shlex.split(input_line)
        
        if not args:
            continue
            
        if args[0] == "exit":
            break
        elif args[0] == "ls":
            print(f"ls: {args[1:]}")
        elif args[0] == "cd":
            print(f"cd: {args[1:]}")
        else:
            print(f"{args[0]}: command not found")
