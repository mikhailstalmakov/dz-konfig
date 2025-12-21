import re

class ParseError(Exception):
    def __init__(self, message, line=None):
        if line is not None:
            super().__init__(f"Line {line}: {message}")
        else:
            super().__init__(message)


class Number:
    def __init__(self, value):
        self.value = value

class Array:
    def __init__(self, items):
        self.items = items

class ConstRef:
    def __init__(self, name):
        self.name = name

class GlobalDecl:
    def __init__(self, name, value):
        self.name = name
        self.value = value


def _remove_comments(text):
   
    text = re.sub(r"%[^\n]*", "", text)
   
    def _repl(m):
        s = m.group(0)
        return "\n" * s.count("\n")
    text = re.sub(r"=begin[\s\S]*?=end", _repl, text)
    return text

# Lexer
TOKEN_SPEC = [
    ("CONSTREF", r"\.\{[_a-zA-Z][_a-zA-Z0-9]*\}\."),
    ("NUMBER", r"[+-]?\d+\.?\d*(?:[eE][+-]?\d+)?"),
    ("NAME", r"[_a-zA-Z][_a-zA-Z0-9]*"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("HASH", r"#"),
    ("EQUAL", r"="),
    ("SEMI", r";"),
    ("WS", r"[ \t\r\n]+"),
    ("MISMATCH", r".")
]
MASTER_RE = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line={self.line})"


def tokenize(text):
    text = _remove_comments(text)
    pos = 0
    line = 1
    tokens = []
    while pos < len(text):
        m = MASTER_RE.match(text, pos)
        if not m:
            raise ParseError("Unexpected character", line)
        typ = m.lastgroup
        val = m.group(0)
        if typ == "WS":
            line += val.count("\n")
        elif typ == "MISMATCH":
            raise ParseError(f"Unexpected token: {val!r}", line)
        else:
            if typ == "CONSTREF":
             
                name = val[2:-2]
                tokens.append(Token("CONSTREF", name, line))
            else:
                tokens.append(Token(typ, val, line))
        pos = m.end()
    tokens.append(Token("EOF", "", line))
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _peek(self):
        return self.tokens[self.pos]

    def _next(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self):
        items = []
        while self._peek().type != "EOF":
            if self._peek().type == "NAME" and self._peek().value == "global":
                items.append(self.parse_global())
            else:
              
                items.append(self.parse_value())
        return items

    def parse_global(self):
        gtok = self._next()  # 'global'
        name_tok = self._next()
        if name_tok.type != "NAME":
            raise ParseError("Expected name after 'global'", name_tok.line)
        eq = self._next()
        if eq.type != "EQUAL":
            raise ParseError("Expected '=' in global declaration", eq.line)
        val = self.parse_value()
        semi = self._next()
        if semi.type != "SEMI":
            raise ParseError("Expected ';' after global declaration", semi.line)
        return GlobalDecl(name_tok.value, val)

    def parse_value(self):
        tok = self._peek()
        if tok.type == "NUMBER":
            self._next()
      
            v = tok.value
            try:
                if '.' in v or 'e' in v or 'E' in v:
                    fv = float(v)
                else:
                    fv = int(v)
                return Number(fv)
            except Exception:
                return Number(v)
        elif tok.type == "HASH":
            return self.parse_array()
        elif tok.type == "CONSTREF":
            t = self._next()
            return ConstRef(t.value)
        else:
            raise ParseError(f"Unexpected token in value: {tok.type}", tok.line)

    def parse_array(self):
        hash_tok = self._next()  # '#'
        lp = self._next()
        if lp.type != "LPAREN":
            raise ParseError("Expected '(' after '#'", lp.line)
        items = []
    
        while True:
            if self._peek().type == "RPAREN":
                self._next()
                break
            if self._peek().type == "EOF":
                raise ParseError("Unterminated array, expected ')'")
            items.append(self.parse_value())
        return Array(items)


def node_to_xml(node, constants, indent=2, level=1):
    pad = ' ' * (indent * (level-1))
    if isinstance(node, Number):
        return f"{pad}<number>{node.value}</number>\n"
    if isinstance(node, Array):
        s = f"{pad}<array>\n"
        for it in node.items:
           
            resolved = resolve_const(it, constants)
            s += node_to_xml(resolved, constants, indent, level+1)
        s += f"{pad}</array>\n"
        return s
    if isinstance(node, ConstRef):
     
        if node.name not in constants:
            raise ParseError(f"Unknown constant: {node.name}")
        return node_to_xml(constants[node.name], constants, indent, level)
    raise ParseError("Unknown node type during XML generation")

def resolve_const(node, constants):
    if isinstance(node, ConstRef):
        if node.name not in constants:
            raise ParseError(f"Unknown constant: {node.name}")
        return constants[node.name]
    if isinstance(node, Array):
        return Array([resolve_const(it, constants) for it in node.items])
    return node


def to_xml(items):
    constants = {}
    s = "<config>\n"
    for it in items:
        if isinstance(it, GlobalDecl):
            
            val = resolve_const(it.value, constants)
            constants[it.name] = val
            s += f"  <global name=\"{it.name}\">\n"
            s += node_to_xml(val, constants, indent=4, level=3)
            s += f"  </global>\n"
        else:
            # top-level value
            val = resolve_const(it, constants)
            s += node_to_xml(val, constants, indent=2, level=2)
    s += "</config>\n"
    return s


def parse_text(text):
    tokens = tokenize(text)
    p = Parser(tokens)
    return p.parse()

def translate(text):
    items = parse_text(text)
    return to_xml(items)
