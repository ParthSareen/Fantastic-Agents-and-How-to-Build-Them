```mermaid
graph TD
    A[entry_node] --> B{entry_decision}
    B -->|Option 1| C[run_exa_node]
    B -->|Option 2| D[broswerbase_node]
    C -->  F[structure_data_node]
    F --> G[print_final_output_node]
    D --> G
```