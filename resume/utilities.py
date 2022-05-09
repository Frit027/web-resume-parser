import re


def remove_invalid_quotes(s):
    return s.replace('"', '').strip() if s.count('"') % 2 else s


def remove_invalid_brackets(s):
    remove_ind = set()
    stack_ind = []
    for ind, char in enumerate(s):
        if char not in "()":
            continue
        if char == "(":
            stack_ind.append(ind)
        elif not stack_ind:
            remove_ind.add(ind)
        else:
            stack_ind.pop()
    remove_ind = remove_ind.union(set(stack_ind))
    output = ""
    for ind, char in enumerate(s):
        if ind in remove_ind:
            continue
        output += char
    return output


def get_json_filename(path):
    return re.sub(r'\.(pdf|doc|docx)$', '.json', path.lower().replace('resume/', ''))
