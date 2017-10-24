import re

import calc
from parser import Bracket

def to_latex(original, value_trees, all_vars):
    bin_values = calc.calc_bin(all_vars)

    max_n = 0
    lines = []
    for k, bin_value in enumerate(bin_values):
        var_list = [0] * len(all_vars)

        for i, bin_v in enumerate(bin_value):
            var_list[i] = bin_v

        line = []

        for l_var in var_list:
            line.append(l_var)

        out = to_out(value_trees[k], [])
        line.append(out)

        # Ganz ekliger hack:
        line_s = str(line).replace('[', '').replace(']', '').replace(',', '').replace("'", '').replace(' ', ' & ')
        n = line_s.count('&') + 1
        max_n = max(max_n, n)
        line_s += ' \\tabularnewline'

        lines.append(line_s)

    start = '\\begin{tabular}{'
    for n in range(max_n):
        if n <= len(var_list):
            start += '|c'
        else:
            start += 'c'
    start += '|}'

    title_var = ''
    for a_var in all_vars:
        title_var += '$' + a_var + '$ & '

    title_var = title_var[:-2]

    processed = ''
    match_var = re.compile('([a-z])')
    for symbol in original:
        if match_var.match(symbol):
            processed += '& $' + symbol + '$'
        else:
            processed += symbol

    original = processed

    original = original.replace('+', '& $\\AND$').replace('-', '& $\\OR$').replace('~', '& $\\neg$').replace('>', '& $\\IMP$')
    original = original.replace('=', '& $\\Leftrightarrow$')

    title_var += original + '\\tabularnewline\hline'

    lines.insert(0, title_var.replace('\\\\', '\\'))
    lines.insert(0, start)
    lines.append('\\end{tabular}')

    return lines


def to_out(bracket, out):
    b_type = get_bracket_type(bracket)

    if b_type == 'bracket' or b_type == 'subbracket':

        if b_type == 'bracket':
            next_bracket = bracket.scope
        elif b_type == 'subbracket':
            next_bracket = bracket.scope[0]

        if next_bracket.neg:
            out.append(next_bracket.value)
            next_out = to_out(next_bracket, [])
            if len(next_out) > 0:
                out.append(next_out)
        else:
            next_out = to_out(next_bracket, [])
            if len(next_out) > 0:
                out.append(next_out)

    elif b_type == 'var':
        return [int(bracket.value)]

    elif b_type == 'math':
        before = bracket.scope[0]
        here = bracket.value
        after = bracket.scope[2]

        next_out = to_out(before, [])
        if len(next_out) > 0:
            out.append(next_out)

        out.append(here)

        next_out = to_out(after, [])
        if len(next_out) > 0:
            out.append(next_out)

    return out


def get_bracket_type(bracket):
    if isinstance(bracket.scope, Bracket):
        return 'bracket'
    elif len(bracket.scope) == 1 and isinstance(bracket.scope[0], Bracket):
        return 'subbracket'
    elif len(bracket.scope) == 1:
        return 'var'
    elif len(bracket.scope) == 3:
        return 'math'
    else:
        raise ValueError('This should not occur. Cannot parse: ', str(bracket))



















