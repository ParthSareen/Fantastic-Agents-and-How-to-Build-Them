from playwright.sync_api import sync_playwright, Playwright
from dagent import call_llm
import json
import os


def browserbase_runner(urls: list[str]):
    def browserbase_runner(urls: list[str]) -> list[dict]:
        """
        Run a browser automation process to scrape and structure data from given URLs.

        This function uses Playwright to connect to a remote browser, navigate to each URL,
        extract the page content, and use an LLM to structure the data into JSON format.

        Args:
            urls (list[str]): A list of URLs to scrape and process.

        Returns:
            list[dict]: A list of dictionaries containing structured data for each successfully processed URL.

        Side Effects:
            - Prints the raw content and structured data for each URL.
            - Saves the structured data to a local file named 'site_data.json'.

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
        site_data = []
        
        for url in urls:
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
                continue
            site_data.append(json.loads(data))
            print('Site data:', json.dumps(site_data[-1], indent=2) + '\n')
        
        # Save the site data locally as a JSON file
        with open('site_data.json', 'w') as f:
            json.dump(site_data, f, indent=2)
        
        print("Site data has been saved to 'site_data.json'")
        return site_data
    finally:
        playwright.stop()

# browserbase_helper(['https://www.betaworks.com/', 'https://extensible.dev/', 'https://jsonify.com'])