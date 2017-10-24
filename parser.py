import re
import copy


def parse_raw(raw_text):
    raw_text = raw_text.replace(' ', '')

    match_all = re.compile('([a-z()+-=~>])')
    match_var = re.compile('([a-z])')

    symbol_vars = []
    symbols = []
    for raw_symbol in raw_text:
        if match_var.match(raw_symbol) and not raw_symbol in symbol_vars:
            symbol_vars.append(raw_symbol)

        if match_all.match(raw_symbol):
            symbols.append(raw_symbol)
        else:
            print('Undefined symbol:', raw_symbol)
            return False

    for i, symbol in enumerate(symbols):
        if symbol == '~' and symbols[i+1:i+2] != '((':
            symbols.insert(i + 2, ')')
            symbols.insert(i + 2, ')')
            symbols.insert(i + 1, '(')
            symbols.insert(i + 1, '(')

    return symbols, symbol_vars


def to_bracket_tree(symbols):  # e.g. symbols = ['(', '(', 'a', ')', '+', '(', 'b', '-', 'c', ')', ')']
    tree = replace_brackets(symbols)
    return tree


def replace_brackets(symbols):
    brackets = find_brackets(symbols)
    occurences_pos = [pos for pos, bracket in enumerate(brackets) if bracket == 1]

    if len(occurences_pos) < 2:
        return symbols

    if len(occurences_pos) % 2 != 0:
        print('Invalid brackets')
        raise ValueError('Invalid brackets')

    full_tree = []

    last_occurrence = 0
    for sub, occurrence in enumerate(occurences_pos):
        if sub % 2 != 0:
            continue

        # Get Brackets Scope
        first_pos = occurences_pos[sub]
        second_pos = occurences_pos[sub+1]

        # Get Symbols before Brackets
        symbols_before = symbols[last_occurrence:first_pos]
        last_occurrence = second_pos+1

        neg = False

        if len(symbols_before) != 0 and symbols_before[-1] == '~':
            neg = True
            full_tree.extend(symbols_before[:-1])
        else:
            full_tree.extend(symbols_before)

        # Get Symbols in Brackets
        sub_symbols = symbols[first_pos + 1:second_pos]

        # Get Brackets replaced of sub-tree
        sub_symbols_tree = replace_brackets(sub_symbols)

        # Add tree as list
        full_tree.append(Bracket(sub_symbols_tree, neg))

    end = symbols[last_occurrence:]
    full_tree.extend(end)

    return full_tree


def find_brackets(symbol_tree):
    brackets = []  # e.g. = [1, 2, False, 2, False, 2, False, False, False, 2, 1]
    brackets_depth = 0

    for symbol in symbol_tree:
        if symbol == '(':
            brackets_depth += 1
            brackets.append(brackets_depth)
        elif symbol == ')':
            brackets.append(brackets_depth)
            brackets_depth -= 1
        else:
            brackets.append(False)
    return brackets


def to_symbol_tree(bracket_tree):
    return Bracket(sub_symbol_tree(bracket_tree), False)


def sub_symbol_tree(bracket_tree):

    # Find math symbol
    symbols = ['+', '-', '>', '=']
    symbol_pos = False
    for symbol in symbols:
        if symbol in bracket_tree:
            all_symbol_pos = [pos for pos, token in enumerate(bracket_tree) if token == symbol]
            symbol_pos = all_symbol_pos[0]

    if not symbol_pos:
        if isinstance(bracket_tree[0], Bracket):
            if bracket_tree[0].neg:
                back = Bracket(sub_symbol_tree(bracket_tree[0].scope), True)
                return back
            else:
                back = Bracket(sub_symbol_tree(bracket_tree[0].scope), False)
                return back
        elif len(bracket_tree) == 1:
            return bracket_tree
        else:
            raise ValueError('Invalid bracket/ This should never occur:', str(bracket_tree))

    before = Bracket(sub_symbol_tree(bracket_tree[:symbol_pos]), False)
    after = Bracket(sub_symbol_tree(bracket_tree[symbol_pos + 1:]), False)

    symbol_tree = [before, bracket_tree[symbol_pos], after]
    return symbol_tree


def find_first_symbol(bracket_tree, symbol):
    occurences = [i for i, token in bracket_tree if token == symbol]
    if len(occurences) == 0:
        return False
    return occurences[0]


class Bracket:

    def __init__(self, scope, neg):
        self.scope = scope
        self.neg = neg
        self.value = None

    def to_str(self):
        out = '~' if self.neg else ''
        out += '{' + str(self.scope).replace('[', '').replace(']', '') + '}'
        out += ('(' + str(self.value) + ')') if self.value is not None else ''
        return out

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.to_str()
















