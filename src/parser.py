from .lexer import tokenize

def parse(query):
    tokens = tokenize(query)
    i = 0

    def peek():
        return tokens[i] if i < len(tokens) else None

    def consume():
        nonlocal i
        t = tokens[i]
        i += 1
        return t

    def expect_keyword(word):
        t = consume()
        if t[1].upper() != word.upper():
            raise SyntaxError(f"Expected {word} got {t[1]}")
        return t

    ast = {}
    expect_keyword("SELECT")

    columns = []
    distinct = False

    if peek() and peek()[1] == "DISTINCT":
        consume()
        distinct = True

    if peek() and peek()[1] == "*":
        consume()
        columns = ["*"]
    else:
        while True:
            col = consume()[1]
            if peek() and peek()[1] == "AS":
                consume()
                alias = consume()[1]
                columns.append((col, alias))
            else:
                columns.append(col)
            if not peek() or peek()[1] != ",":
                break
            consume()

    ast["select"] = columns
    ast["distinct"] = distinct

    expect_keyword("FROM")
    ast["from"] = consume()[1]

    ast["where"] = None
    ast["order_by"] = None
    ast["limit"] = None
    ast["group_by"] = None

    while peek():
        keyword = peek()[1].upper()

        if keyword == "WHERE":
            consume()
            conditions = []
            while peek() and peek()[1] not in ("ORDER", "LIMIT", "GROUP"):
                left = consume()[1]
                op = consume()[1]
                right = consume()[1].strip("'")
                conditions.append({"left": left, "op": op, "right": right})
                if peek() and peek()[1] in ("AND", "OR"):
                    conditions.append(consume()[1])
            ast["where"] = conditions

        elif keyword == "ORDER":
            consume()
            expect_keyword("BY")
            col = consume()[1]
            direction = "ASC"
            if peek() and peek()[1] in ("ASC", "DESC"):
                direction = consume()[1]
            ast["order_by"] = {"col": col, "direction": direction}

        elif keyword == "LIMIT":
            consume()
            ast["limit"] = int(consume()[1])

        elif keyword == "GROUP":
            consume()
            expect_keyword("BY")
            ast["group_by"] = consume()[1]

        else:
            break

    return ast