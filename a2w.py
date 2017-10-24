import parser
import calc
import printer

raw_text = input('Bitte eine Aussage angeben (a-z, (), AND: +, OR: -, NEG: ~, IMP: >, AEQ: =): ')

symbols, symbol_vars = parser.parse_raw(raw_text)
print(symbols)

if symbols:
    bracket_tree = parser.to_bracket_tree(symbols)
    #print(bracket_tree)

    if bracket_tree:
        symbol_tree = parser.to_symbol_tree(bracket_tree)
        #print(symbol_tree)

        if symbol_tree:
            value_trees = calc.values_symbol_tree(symbol_tree, symbol_vars)
            #print(value_trees[0])

            latex = printer.to_latex(raw_text, value_trees, symbol_vars)
            print()
            for line in latex:
                print(line)


