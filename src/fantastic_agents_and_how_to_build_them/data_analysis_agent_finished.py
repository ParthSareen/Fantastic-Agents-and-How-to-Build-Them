from dagent import DecisionNode, FunctionNode, call_llm
from dataclasses import asdict
from exa_py import Exa
from fantastic_agents_and_how_to_build_them.shared.browserbase import browserbase_runner
import os
import json

def run_exa(prev_output):
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

    # Parse the JSON string into a Python dictionary
    structured_data = json.loads(data)

    # Save the structured data locally as a JSON file
    with open('structured_data.json', 'w') as f:
        json.dump(structured_data, f, indent=2)
    
    print("Structured data has been saved to 'structured_data.json'")
    
    return structured_data
    

def entry():
    search_term = input("Either enter a search")
    return search_term

entry_node = FunctionNode(func=entry)
decision1 = DecisionNode(messages=[{'role': 'user', 'content': 'Pick between the provided functions to run given the user input. exa node is for searching for things and browserbase node is for scraping websites.'}])
run_exa_node = FunctionNode(func=run_exa)
structure_data_node = FunctionNode(func=structure_data)
broswerbase_node = FunctionNode(func=browserbase_runner)

decision_filter = DecisionNode(messages=[{'role': 'user', 'content': 'if the user wants relevant sites scraped as well'}])

entry_node.next_nodes = [decision1]
decision1.next_nodes = [run_exa_node, broswerbase_node]

run_exa_node.next_nodes = [structure_data_node]

run_exa_node.compile(force_load=False)

