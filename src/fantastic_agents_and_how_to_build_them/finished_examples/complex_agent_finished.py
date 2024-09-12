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

    This function takes the output from the Exa search (prev_output) and processes it
    to create a structured JSON object. The structured data includes the website name
    and a list of data points for each search result, containing the URL, headline,
    and a brief description.

    Args:
        prev_output (dict): The raw output from the Exa search function.

    Returns:
        dict: A structured JSON object containing the formatted data.

    Side Effects:
        - Saves the structured data to a local file named 'structured_data.json'.
        - Prints a confirmation message when the data is saved.

    Note:
        This function uses an LLM to process and structure the data, which may
        introduce some variability in the output format and content.
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


    logging.info(f"Structure data function called with prev_output: {prev_output}")
    data = call_llm(
        model='gpt-4-0125-preview',
        messages=[
            {
                "role": "user",
                "content": f"""
                Structure this website raw content into a JSON format matching this pattern:
                {json.dumps(data_format, indent=2)}
                
                The JSON should include the website name, and for each result, include:
                - URL
                - Headline (if any)
                - Brief description

                Raw content to structure:
                {str(prev_output)}
                """
            }
        ],
        response_format={'type': 'json_object'}
    )
    logging.info(f"Data from LLM: {data}")

    # Parse the JSON string into a Python dictionary
    structured_data = json.loads(data)

    # Save the structured data locally as a JSON file
    with open('structured_data_exa.json', 'w') as f:
        json.dump(structured_data, f, indent=2)
    
    print("Structured data has been saved to 'structured_data.json'")
    
    return structured_data
    

def entry(user_input):
    # There could be some mutation here or something to enhance a query
    if 'scrape' in user_input.split():
        user_input += ' Make sure to scraping occurs either after exa node or browserbase node'
    return user_input 


def print_final_output(prev_output):
    print("Final output:", json.dumps(prev_output, indent=2))
    summary = call_llm(
        model='gpt-4-0125-preview',
        messages=[
            {
                "role": "user",
                "content": f"""
                Summarize the following structured data into a concise overview:
                {json.dumps(prev_output, indent=2)}
                """
            }
        ],
        response_format={'type': 'text'}
    )
    print("Summary of the data:", summary)
    print("Data should be saved as well")

# Node setup
entry_node = FunctionNode(func=entry)

entry_decision = DecisionNode(user_params={'messages': [{'role': 'user', 'content': 'Pick between the provided functions to run given the user input. exa node is for searching for things and browserbase node is for scraping websites. Do not use browserbase unless user specifies scraping a specific site'}]}, max_tool_calls=1)

run_exa_node = FunctionNode(func=run_exa)
structure_data_node = FunctionNode(func=structure_data)
broswerbase_node = FunctionNode(func=browserbase_runner)
# user_params={'messages': [{'role': 'user', 'content': 'Only scrape using browserbase if specified by user.'}]},
decision_filter_node = DecisionNode(max_tool_calls=1)

print_final_output_node = FunctionNode(func=print_final_output)


# Linking
entry_node.next_nodes = [entry_decision]

entry_decision.next_nodes = [run_exa_node, broswerbase_node]

run_exa_node.next_nodes = [structure_data_node] 

# decision_filter_node.next_nodes = [structure_data_node, broswerbase_node]

broswerbase_node.next_nodes = [print_final_output_node]
structure_data_node.next_nodes = [print_final_output_node]


entry_node.compile()

while True:
    user_input = input("Enter your command (or 'quit' to exit): ")
    if user_input.lower() == 'quit':
        break
    entry_node.run(user_input=user_input)