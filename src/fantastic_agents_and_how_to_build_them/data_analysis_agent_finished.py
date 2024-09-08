from dagent import DecisionNode, FunctionNode, call_llm
from dataclasses import asdict
from exa_py import Exa
from playwright.sync_api import sync_playwright, Playwright
import os
import json

def run_exa():
    exa = Exa(api_key=os.environ["EXA_API_KEY"])

    result = exa.search_and_contents(
    "betaworks",
    type="neural",
    use_autoprompt=True,
    num_results=10,
    text=True
    )
    
    response = asdict(result)
    return response 

results = run_exa()

print(json.dumps(results['results'][1], indent=2))


def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.connect_over_cdp('wss://connect.browserbase.com?apiKey='+ os.environ["BROWSERBASE_API_KEY"])
    context = browser.contexts[0]
    page = context.pages[0]
    
    # Navigate to a specific page
    url = "https://www.betaworks.com/"
    page.goto(url)
    
    # Wait for the content to load (adjust timeout as needed)
    # page.wait_for_load_state("networkidle", timeout=10000)
    
    # Get the page content
    content = page.content()
    
    print(f"Content from {url}:")
    print(content + '\n')
    data  = call_llm(model='gpt-4-0125-preview', messages=[{"role": "user", "content": "structure this website raw content into a json. I want the website name, headline if any, and anything else important in other fields: " + content}], response_format={'type': 'json_object'})
    print('output', data + '\n')

# with sync_playwright() as playwright:
#     run(playwright)

