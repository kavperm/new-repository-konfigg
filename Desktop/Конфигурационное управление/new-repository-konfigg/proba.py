import os
import argparse
import socket

def expand(a: str):
    for k in os.environ:
        a = a.replace("$" + k, os.environ[k])
    return a

def get_prompt():
    username = os.getlogin() # имя пользователя
    hostname = socket.gethostname() # имя хоста
    return f"{username}@{hostname}:~$ "

def act(a):
    a = expand(a)
    b = a.split()
    if a == "exit":
        exit()
    if len(b) == 0:
        return ""
    if b[0] == "ls":
        return b
    elif b[0] == "cd":
        return b
    else:
        return f"{b[0]}: command not found"

parser = argparse.ArgumentParser()
parser.add_argument("--path", "-p", help="Путь к физическому расположению VFS")
parser.add_argument("--script", "-s", help="Путь к стартовому скрипту")
args = parser.parse_args()

print("=== Параметры запуска ===")
print(f"VFS путь: {args.path}")
print(f"Скрипт: {args.script}")
print("========================")

if args.script:
    print(f"\nВыполнение скрипта {args.script}:")
    try:
        with open(args.script, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                print(get_prompt() + line)
                result = act(line)
                if result:
                    print(result)
    except FileNotFoundError:
        print(f"Ошибка: скрипт {args.script} не найден")
    except Exception as e:
        print(f"Ошибка выполнения скрипта: {e}")
    
    print("\nСкрипт выполнен. Переход в интерактивный режим.\n")

while True:
    a = input(get_prompt())
    result = act(a)
    if result:
        print(result)

