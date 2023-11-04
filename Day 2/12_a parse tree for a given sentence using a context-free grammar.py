class EarleyItem:
    def __init__(self, production, dot_position, start_position):
        self.production = production
        self.dot_position = dot_position
        self.start_position = start_position

    def __str__(self):
        prod = list(self.production)
        prod.insert(self.dot_position, "●")
        return f"{self.production[0]} -> {' '.join(prod[1:])}, {self.start_position}"

def earley_parse(grammar, input_string):
    chart = [[] for _ in range(len(input_string) + 1)]

    # Initialize the chart with the start rule
    start_rule = list(grammar.keys())[0]
    initial_item = EarleyItem(start_rule, 0, 0)
    chart[0].append(initial_item)

    for i in range(len(input_string) + 1):
        for item in chart[i]:
            if not item_completed(item):
                next_symbol = item.production[item.dot_position]
                if next_symbol in grammar:
                    for production in grammar[next_symbol]:
                        new_item = EarleyItem(production, 0, i)
                        if new_item not in chart[i]:
                            chart[i].append(new_item)
            else:
                completer(i, item, chart)

    # Check if the goal symbol is completed in the final position
    final_item = EarleyItem(start_rule, len(start_rule) - 1, len(input_string))
    return final_item in chart[len(input_string)]

def item_completed(item):
    return item.dot_position == len(item.production) - 1

def completer(position, item, chart):
    for existing_item in chart[item.start_position]:
        if not item_completed(existing_item) and existing_item.production[existing_item.dot_position] == item.production[0]:
            new_item = EarleyItem(existing_item.production, existing_item.dot_position + 1, existing_item.start_position)
            if new_item not in chart[position]:
                chart[position].append(new_item)

# Example usage:
if __name__ == "__main__":
    grammar = {
        "S": [["NP", "VP"]],
        "NP": [["The", "N"], ["I"]],
        "VP": [["V", "NP"], ["eats"]],
        "N": [["cat"], ["dog"]],
        "V": [["chases"], ["eats"]],
    }

    input_string = "The cat eats"

    if earley_parse(grammar, input_string.split()):
        print("Parsing successful!")
    else:
        print("Parsing failed.")
