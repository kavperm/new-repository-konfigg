import json
import sys

def assemble(input_file, output_file, test_mode=False):
    with open(input_file, 'r', encoding='utf-8') as f:
        program = json.load(f)

    ir = []  
    for cmd in program:
        op = cmd["op"]
        if op == "load_const":
            ir.append((6, cmd["const"]))
        elif op == "read_mem":
            ir.append((0, cmd["addr"]))
        elif op == "write_mem":
            ir.append((4, cmd["addr"]))
        elif op == "leq":
            ir.append((7, cmd["addr"]))
        else:
            raise ValueError(f"Неизвестная операция: {op}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(repr(ir))

    if test_mode:
        print("Промежуточное представление:")
        for i, (a, b) in enumerate(ir):
            print(f"Команда {i}: A={a}, B={b}")


input_file = sys.argv[1] if len(sys.argv) > 1 else "program.json"
output_file = sys.argv[2] if len(sys.argv) > 2 else "program.ir"
test_mode = len(sys.argv) > 3 and sys.argv[3] == "-test"

assemble(input_file, output_file, test_mode)