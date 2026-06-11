import re

TOKENS = [
    ("KEYWORD", r"\b(SELECT|FROM|WHERE|AND|OR|LIMIT|ORDER|BY|ASC|DESC|COUNT|SUM|AVG|MIN|MAX|GROUP|AS|DISTINCT)\b"),
    ("NUMBER",  r"\d+(\.\d+)?"),
    ("STRING",  r"'[^']*'"),
    ("SYMBOL",  r"[=<>!,\(\)\*;]|!=|<=|>="),
    ("IDENT",   r"[a-zA-Z_][a-zA-Z0-9_\./]*"),
    ("SKIP",    r"[ \t\n]+"),
]

def tokenize(query):
    tokens = []
    i = 0
    while i < len(query):
        matched = False
        for token_type, pattern in TOKENS:
            m = re.match(pattern, query[i:], re.IGNORECASE)
            if m:
                val = m.group(0)
                if token_type != "SKIP":
                    tokens.append((token_type, val.upper() if token_type == "KEYWORD" else val))
                i += len(val)
                matched = True
                break
        if not matched:
            i += 1
    return tokens