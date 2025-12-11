import sys
import yaml
from lark import Lark, Transformer, v_args

GRAMMAR = """
start: (const_def | value)*

const_def: "def" NAME ":=" value
value: NUMBER | array | const_ref
array: "#(" [value+] ")"
const_ref: ".(" NAME ")."

NUMBER: /[0-9]+/
NAME: /[_A-Z][_a-zA-Z0-9]*/

%import common.WS
%ignore WS
"""

@v_args(inline=True)
class ConfigTransformer(Transformer):
    def NUMBER(self, n):
        return int(n)
    
    def NAME(self, n):
        return str(n)
    
    def array(self, *args):
        return list(args)
    
    def const_ref(self, name):
        return ("ref", name)
    
    def const_def(self, name, value):
        return ("def", name, value)
    
    def value(self, v):
        return v
    
    def start(self, *items):
        return list(items)

def interpret(tree):
    env = {}
    results = []
    
    def eval_value(val):
        if isinstance(val, int):
            return val
        elif isinstance(val, list):
            return [eval_value(v) for v in val]
        elif isinstance(val, tuple) and val[0] == "ref":
            name = val[1]
            if name in env:
                return env[name]
            raise NameError(f"Undefined constant: {name}")
        return val
    
    const_defs = []
    for item in tree:
        if isinstance(item, tuple) and item[0] == "def":
            const_defs.append(item)
        else:
            results.append(item)
    

    for _, name, value in const_defs:
        env[name] = eval_value(value)
    
    final_results = []
    for item in results:
        final_results.append(eval_value(item))
    
    return final_results if len(final_results) != 1 else final_results[0]


input_text = sys.stdin.read()
parser = Lark(GRAMMAR, parser='lalr')
tree = parser.parse(input_text)
transformer = ConfigTransformer()
transformed = transformer.transform(tree)
result = interpret(transformed)
yaml.dump(result, sys.stdout, default_flow_style=False)