from .scanner import scan

AGGREGATES = ("COUNT", "SUM", "AVG", "MIN", "MAX")

def evaluate_condition(row, condition):
    left = row.get(condition["left"], condition["left"])
    right = condition["right"]
    op = condition["op"]

    try:
        left = float(left)
        right = float(right)
    except (ValueError, TypeError):
        pass

    if op == "=":  return left == right
    if op == "!=": return left != right
    if op == ">":  return left > right
    if op == "<":  return left < right
    if op == ">=": return left >= right
    if op == "<=": return left <= right
    return False

def execute(plan):
    rows = []

    for step in plan:
        op = step["op"]

        if op == "scan":
            rows = scan(step["source"])

        elif op == "filter":
            filtered = []
            for row in rows:
                result = None
                logic = "AND"
                for condition in step["conditions"]:
                    if condition in ("AND", "OR"):
                        logic = condition
                        continue
                    match = evaluate_condition(row, condition)
                    if result is None:
                        result = match
                    elif logic == "AND":
                        result = result and match
                    elif logic == "OR":
                        result = result or match
                if result:
                    filtered.append(row)
            rows = filtered

        elif op == "project":
            columns = step["columns"]
            distinct = step.get("distinct", False)
            if columns == ["*"]:
                pass
            else:
                projected = []
                for row in rows:
                    new_row = {}
                    for col in columns:
                        if isinstance(col, tuple):
                            new_row[col[1]] = row.get(col[0])
                        else:
                            func = None
                            field = col
                            for agg in AGGREGATES:
                                if col.upper().startswith(agg + "("):
                                    func = agg
                                    field = col[len(agg)+1:-1]
                                    break
                            if func:
                                new_row[col] = row.get(field)
                            else:
                                new_row[col] = row.get(col)
                    projected.append(new_row)
                rows = projected
            if distinct:
                seen = set()
                unique = []
                for row in rows:
                    key = tuple(sorted(row.items()))
                    if key not in seen:
                        seen.add(key)
                        unique.append(row)
                rows = unique

        elif op == "group":
            col = step["col"]
            groups = {}
            for row in rows:
                key = row.get(col, "")
                if key not in groups:
                    groups[key] = []
                groups[key].append(row)
            result = []
            for key, group_rows in groups.items():
                new_row = {col: key}
                for s in step["select"]:
                    if isinstance(s, str):
                        for agg in AGGREGATES:
                            if s.upper().startswith(agg + "("):
                                field = s[len(agg)+1:-1]
                                if agg == "COUNT":
                                    new_row[s] = len(group_rows)
                                elif agg == "SUM":
                                    new_row[s] = sum(float(r.get(field, 0)) for r in group_rows)
                                elif agg == "AVG":
                                    new_row[s] = sum(float(r.get(field, 0)) for r in group_rows) / len(group_rows)
                                elif agg == "MIN":
                                    new_row[s] = min(float(r.get(field, 0)) for r in group_rows)
                                elif agg == "MAX":
                                    new_row[s] = max(float(r.get(field, 0)) for r in group_rows)
                result.append(new_row)
            rows = result

        elif op == "sort":
            reverse = step["direction"].upper() == "DESC"
            rows = sorted(rows, key=lambda r: r.get(step["col"], ""), reverse=reverse)

        elif op == "limit":
            rows = rows[:step["n"]]

    return rows