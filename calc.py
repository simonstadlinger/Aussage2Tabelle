import re
import copy

from parser import Bracket


def values_symbol_tree(symbol_tree, symbol_vars):
    bin_values = calc_bin(symbol_vars)

    value_trees = []

    # Calc for each bin_value
    for bin_value in bin_values:
        var_list = {}

        # Create empty list
        for s_var in symbol_vars:
            var_list[s_var] = 0

        for i, bin_v in enumerate(bin_value):
            var_list[symbol_vars[i]] = bin_v

        value_tree = copy.deepcopy(symbol_tree)
        calc_values(value_tree, var_list)
        value_trees.append(value_tree)

    return value_trees


def calc_bin(symbol_vars):
    n = 2 ** len(symbol_vars)

    bin_values = [str(bin(i))[2:] for i in range(n)]

    # Normalize
    for n, bin_value in enumerate(bin_values):
        while len(bin_values[n]) < len(bin_values[-1]):
            bin_values[n] = '0' + bin_values[n]
    return bin_values


def calc_values(scope, var_list):
    s_type = get_bracket_type(scope)
    if s_type == 'bracket':
        return calc_bracket(scope, var_list)

    elif s_type == 'var':
        return var_list[scope[0]]

    elif s_type == 'math':
        math_symbol = scope[1]
        before = scope[0]
        after = scope[2]

        if math_symbol == '+':
            return l_add(before, after, var_list)
        elif math_symbol == '-':
            return l_or(before, after, var_list)
        elif math_symbol == '>':
            return l_imp(before, after, var_list)
        elif math_symbol == '=':
            return l_aeq(before, after, var_list)


def l_add(before, after, var_list):
    before_v = int(calc_values(before, var_list))
    after_v = int(calc_values(after, var_list))

    if before_v == 1 and after_v == 1:
        return 1
    else:
        return 0


def l_or(before, after, var_list):
    before_v = int(calc_values(before, var_list))
    after_v = int(calc_values(after, var_list))

    if before_v == 1 or after_v == 1:
        return 1
    else:
        return 0


def l_imp(before, after, var_list):
    before_v = int(calc_values(before, var_list))
    after_v = int(calc_values(after, var_list))

    if before_v == 1 and after_v == 0:
        return 0
    else:
        return 1


def l_aeq(before, after, var_list):
    before_v = int(calc_values(before, var_list))
    after_v = int(calc_values(after, var_list))

    if before_v == after_v:
        return 1
    else:
        return 0


def l_neg(scope, var_list):
    f_value = int(calc_values(scope, var_list))
    return 0 if f_value == 1 else 1


def calc_bracket(bracket, var_list):
    b_type = get_bracket_type(bracket)
    if b_type != 'bracket':
        raise ValueError('Bracket was no bracket', bracket)

    value = None
    if bracket.neg:
        value = l_neg(bracket.scope, var_list)
    else:
        value = calc_values(bracket.scope, var_list)

    bracket.value = value
    return value


def get_bracket_type(symbol_tree):
    match_var = re.compile('([a-z])')

    if isinstance(symbol_tree, Bracket):
        return 'bracket'
    else:
        if len(symbol_tree) == 1 and match_var.match(symbol_tree[0]):
            return'var'
        if len(symbol_tree) == 3 and isinstance(symbol_tree[0], Bracket) \
                and symbol_tree[1] in ['+', '-', '>', '='] \
                and isinstance(symbol_tree[2], Bracket):
            return 'math'

    raise ValueError('This should not occur. There seems to be a wrong bracket')


def l_not(bracket):
    values = calc_values(bracket.scope)

    neg_values = []
    for value in values:
        pass

