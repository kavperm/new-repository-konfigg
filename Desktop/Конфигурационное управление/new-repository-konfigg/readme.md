# Эмулятор командной оболочки ОС

## Общее описание
Эмулятор командной строки UNIX-подобной ОС с поддержкой интерактивного режима и выполнения скриптов. Реализует базовые команды и парсинг аргументов.

## Функции и настройки
### Основные команды:
- `ls` - вывод аргументов команды
- `cd` - вывод аргументов команды
- `exit` - завершение работы

### Параметры запуска:
- `--path` / `-p` - путь к физическому расположению VFS
- `--script` / `-s` - путь к стартовому скрипту

### Особенности:
- Автоматическое определение пользователя и hostname для промпта
- Поддержка аргументов в кавычках через shlex
- Выполнение скриптов с пропуском ошибок

### Сборка и запуск
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

### Пример использования
---------------------------
Путь VFS = None
Путь скрипт = test.script
---------------------------
ak@MacBook-Air-A.local:~$ ls -lp lo "mi mi mi"
ls: ['-lp', 'lo', 'mi mi mi']
ak@MacBook-Air-A.local:~$ cd /tmp "ne ne ne"
cd: ['/tmp', 'ne ne ne']
ak@MacBook-Air-A.local:~$ lalalalalalalala
lalalalalalalala: command not found
ak@MacBook-Air-A.local:~$ ls
ls: []
ak@MacBook-Air-A.local:~$ exit
ak@MacBook-Air-A new-repository-konfigg % 