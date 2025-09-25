import os
import socket
import shlex

def main():
    while True:
        user = os.getenv('USER') or os.getenv('USERNAME')
        hostname = socket.gethostname()
        cwd = os.getcwd().replace(os.path.expanduser("~"), "~")
        prompt = f"{user}@{hostname}:{cwd}$ "
        
        # Читаем ввод
        try:
            input_line = input(prompt).strip()
        except EOFError:
            break  # В случае Ctrl+D
            
        if not input_line:
            continue  # Пустой ввод
            
        # Парсим аргументы
        try:
            args = shlex.split(input_line)
        except ValueError as e:
            print(f"Parser error: {e}")
            continue
            
        # Обрабатываем команды
        if args[0] == "exit":
            break
        elif args[0] == "ls":
            print(f"ls called with arguments: {args[1:]}")
        elif args[0] == "cd":
            print(f"cd called with arguments: {args[1:]}")
        else:
            print(f"Command not found: {args[0]}")

if __name__ == "__main__":
    main()