def plan(ast):
    steps = []
    steps.append({"op": "scan", "source": ast["from"]})

    if ast.get("where"):
        steps.append({"op": "filter", "conditions": ast["where"]})

    if ast.get("group_by"):
        steps.append({"op": "group", "col": ast["group_by"], "select": ast["select"]})
    else:
        steps.append({"op": "project", "columns": ast["select"], "distinct": ast.get("distinct", False)})

    if ast.get("order_by"):
        steps.append({"op": "sort", "col": ast["order_by"]["col"], "direction": ast["order_by"]["direction"]})

    if ast.get("limit"):
        steps.append({"op": "limit", "n": ast["limit"]})

    return steps