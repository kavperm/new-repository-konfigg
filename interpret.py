import sys
import json

class StackVM:
    def __init__(self, mem_size=1024):
        self.memory = [0] * mem_size  
        self.stack = []               
        
    def execute(self, program):
        for op, b in program:
            if op == 6:  # load_const
                self.stack.append(b)
                
            elif op == 0:  # read_mem
                if b < 0 or b >= len(self.memory):
                    raise IndexError(f"Адрес памяти {b} вне диапазона")
                self.stack.append(self.memory[b])
                
            elif op == 4:  # write_mem
                if not self.stack:
                    raise RuntimeError("Стек пуст при выполнении write_mem")
                value = self.stack.pop()
                if b < 0 or b >= len(self.memory):
                    raise IndexError(f"Адрес памяти {b} вне диапазона")
                self.memory[b] = value
                
            elif op == 7:  # leq (меньше или равно)
                if len(self.stack) < 1:
                    raise RuntimeError("Недостаточно операндов в стеке для leq")
                
                
                op2 = self.stack.pop()
                
                
                if b < 0 or b >= len(self.memory):
                    raise IndexError(f"Адрес памяти {b} вне диапазона")
                op1 = self.memory[b]
                
                
                result = 1 if op1 <= op2 else 0
                self.stack.append(result)
                
            else:
                raise ValueError(f"Неизвестный код операции: {op}")
    
    def dump_memory(self, start_addr=0, end_addr=None):
        if end_addr is None:
            end_addr = len(self.memory)
        
        return {str(addr): self.memory[addr] 
                for addr in range(start_addr, end_addr) 
                if self.memory[addr] != 0}


   
if len(sys.argv) < 2:
    print("Использование:")
    print("  python interpret.py <program.ir> [dump.json] [start] [end]")
    sys.exit(1)

ir_file = sys.argv[1]
with open(ir_file, 'r', encoding='utf-8') as f:
    program = eval(f.read())


vm = StackVM()
vm.execute(program)


print("Состояние памяти (ненулевые значения):")
for addr, value in enumerate(vm.memory):
    if value != 0:
        print(f"  M[{addr}]: {value}")

if len(sys.argv) >= 3:
    dump_file = sys.argv[2]
    
    start = int(sys.argv[3]) if len(sys.argv) >= 4 else 0
    end = int(sys.argv[4]) if len(sys.argv) >= 5 else len(vm.memory)
    
    mem_dump = vm.dump_memory(start, end)
    with open(dump_file, 'w', encoding='utf-8') as f:
        json.dump(mem_dump, f, indent=2)
    
    print(f"\nДамп памяти сохранен в {dump_file} (адреса {start}-{end-1})")

