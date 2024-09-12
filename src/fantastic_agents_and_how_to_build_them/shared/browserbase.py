from playwright.sync_api import sync_playwright
from dagent import call_llm
import json
import os

def browserbase_runner(url: str) -> dict:
    """
    Run a browser automation process to scrape and structure data from a given URL.

    This function uses Playwright to connect to a remote browser, navigate to the URL,
    extract the page content, and use an LLM to structure the data into JSON format.

    Args:
        url (str): The URL to scrape and process.

    Returns:
        dict: A dictionary containing structured data for the successfully processed URL.

    Side Effects:
        - Saves the structured data to a local file named 'site_data_browserbase.json'.

    Raises:
        Any exceptions that occur during the browser automation or LLM processing are caught and printed,
        but do not stop the overall process.

    Note:
        This function requires a valid BROWSERBASE_API_KEY environment variable to be set.
    """
    playwright = sync_playwright().start()
    try:
        chromium = playwright.chromium
        browser = chromium.connect_over_cdp('wss://connect.browserbase.com?apiKey='+ os.environ["BROWSERBASE_API_KEY"])
        context = browser.contexts[0]
        page = context.pages[0]
        
        # Navigate to the page
        page.goto(url)
        
        # Get the page content
        content = page.content()
        
        try:
            # Limit content to approximately 127500 tokens
            content = ' '.join(content.split()[:127500])

            data = call_llm(
                model='gpt-4-0125-preview',
                messages=[{
                    "role": "user",
                    "content": f"Structure this website raw content into a JSON. Include the website name, headline if any, and any other important fields: {content}"
                }],
                response_format={'type': 'json_object'}
            )
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            return {}
        
        structured_data = json.loads(data)
        
        # Save the site data locally as a JSON file
        with open('site_data_browserbase.json', 'w') as f:
            json.dump(structured_data, f, indent=2)
        
        print("Site data has been saved to 'site_data.json'")
        return structured_data
    finally:
        playwright.stop()