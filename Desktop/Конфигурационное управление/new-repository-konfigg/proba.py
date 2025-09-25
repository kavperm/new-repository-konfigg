import os
import socket
import shlex

def get_prompt():
    user = os.getenv('USER')
    hostname = socket.gethostname()
    current_dir = os.getcwd()
    home_dir = os.getenv('HOME')
    
    if current_dir.startswith(home_dir):
        current_dir = '~' + current_dir[len(home_dir):]
    return f"{user}@{hostname}:{current_dir}$ "

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
