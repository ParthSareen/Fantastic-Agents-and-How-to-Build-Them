import logging
from dagent import DecisionNode, FunctionNode, call_llm
from dataclasses import asdict
from exa_py import Exa
from fantastic_agents_and_how_to_build_them.shared.browserbase import browserbase_runner
import os
import json

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('dagent_logs.log'), logging.StreamHandler()])


def run_exa(prev_output):
    '''
    Prev output should be the only input to this function, and that is the search query
    '''
    exa = Exa(api_key=os.environ["EXA_API_KEY"])

    result = exa.search_and_contents(
        prev_output,
        type="neural",
        use_autoprompt=True,
        num_results=10,
        text=True
    )
    
    response = asdict(result)
    return response 

    
def structure_data(prev_output):
    """
    Structure the raw content from the Exa search results into a formatted JSON object.

    Args:
        prev_output (dict): The raw output from the Exa search function.

    Returns:
        dict: A structured JSON object containing the formatted data.

    Side Effects:
        - Saves the structured data to a local file named 'structured_data.json'.
        - Prints a confirmation message when the data is saved.
    """
    data_format = {
        "website": "Example Website",
        "data": [
            {
                "url": "https://example.com",
                "headline": "Example Headline",
                "description": "Brief description of the content"
            }
        ]
    }

    # TODO: Implement the logic to structure the data
    # 1. Log the input
    # 2. Call LLM to structure the data
    # 3. Parse the LLM response
    # 4. Save the structured data to a file
    # 5. Return the structured data

    structured_data = {}  # Placeholder, replace with actual implementation
    return structured_data



def entry(user_input):
    """
    Process the initial user input.

    Args:
        user_input (str): The user's input command.

    Returns:
        str: Potentially modified user input.
    """
    # TODO: Implement logic to process and potentially modify user input
    return user_input 


def summarize_final_output(prev_output):
    """
    Summarize the final structured output.

    Args:
        prev_output (dict): The structured data to summarize.

    Side Effects:
        - Prints the final output and summary.
    """
    # TODO: Implement logic to summarize the final output
    # 1. Print the final structured output
    # 2. Call LLM to generate a summary
    # 3. Print the summary
    pass


# Node setup
entry_node = FunctionNode(func=entry)

entry_decision = DecisionNode(
    user_params={'messages': [{'role': 'user', 'content': 'Pick between the provided functions to run given the user input. exa node is for searching for things and browserbase node is for scraping websites. Do not use browserbase unless user specifies scraping a specific site'}]}, 
    max_tool_calls=1
)

run_exa_node = FunctionNode(func=run_exa)
structure_data_node = FunctionNode(func=structure_data)
browserbase_node = FunctionNode(func=browserbase_runner)
summarize_final_output_node = FunctionNode(func=summarize_final_output)

# TODO: Set up node linking
# entry_node.next_nodes = ...
# entry_decision.next_nodes = ...
# run_exa_node.next_nodes = ...
# structure_data_node.next_nodes = ...
# browserbase_node.next_nodes = ...

# TODO: Compile the entry node
# entry_node.compile()

# TODO: Implement the main loop for user interaction
# while True:
#     user_input = input("Enter your command (or 'quit' to exit): ")
#     if user_input.lower() == 'quit':
#         break
#     entry_node.run(user_input=user_input)

