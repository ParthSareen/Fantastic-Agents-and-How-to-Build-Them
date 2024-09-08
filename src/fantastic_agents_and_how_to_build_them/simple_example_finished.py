from dagent import DecisionNode, FunctionNode


def add_two_nums(a: int, b: int) -> int:
    return a + b


def multiply_two_nums(a: int, b: int) -> int:
    return a * b


# `prev_output` is the output from the previous node, needs to be specified in the function signature if it is used
def print_result(prev_output:int) -> None:
    print(prev_output)
    return prev_output


def entry_func(input):
    # Some mutation of input here
    return input

# Setup function nodes
add_two_nums_node = FunctionNode(func=add_two_nums)
multiply_two_nums_node = FunctionNode(func=multiply_two_nums)
print_result_node = FunctionNode(func=print_result)
entry_node = FunctionNode(func=entry_func)

# Setup decision node
decision_node = DecisionNode(model='gpt-4-0125-preview', api_base=None)

# Link nodes together
entry_node.next_nodes = [decision_node] 

decision_node.next_nodes = [
    add_two_nums_node,
    multiply_two_nums_node,
]

add_two_nums_node.next_nodes = [
    print_result_node
]

multiply_two_nums_node.next_nodes = [
    print_result_node
]

# Compile the nodes
entry_node.compile(force_load=False)

# Run the nodes
while True:
    user_input = input("Enter your command (or 'quit' to exit): ")
    if user_input.lower() == 'quit':
        break
    entry_node.run(input=user_input)

# Commented out examples:
# messages = [{"role": "user", "content": "add the numbers 2 and 3"}]
# messages = [{"role": "user", "content": "multiply the numbers 2 and 3"}]






