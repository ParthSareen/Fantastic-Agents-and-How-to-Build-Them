```mermaid
    graph TD;
    user_input --> entry_node;
    entry_node --> decision_node;
    decision_node --> add_two_nums_node;
    decision_node --> multiply_two_nums_node;
    add_two_nums_node --> print_result_node;
    multiply_two_nums_node --> print_result_node;
```