# src/scraper.py
from tavily import TavilyClient
from typing import List, Dict
from .config import TAVILY_API_KEY

# Initialize the Tavily client
# This client will handle the API request to find relevant job links.
try:
    TAVILY = TavilyClient(api_key=TAVILY_API_KEY)
except Exception as e:
    # Handle the case where the API key might be invalid or missing
    print(f"Error initializing Tavily Client: {e}")
    TAVILY = None


def fetch_job_data(role: str, location: str) -> List[Dict]:
    """
    Constructs a search query and uses the Tavily API to fetch relevant job links.

    :param role: The target job role (e.g., 'data scientist').
    :param location: The desired job location (e.g., 'New York').
    :return: A list of dictionaries, each representing a raw job listing with links.
    """
    if not TAVILY:
        print("Tavily client not initialized. Check your API key in config.py.")
        return []

    # 1. Construct the search query
    search_query = f"{role} job openings in {location} - job search results link"

    print(f"-> Searching for job links using Tavily: '{search_query}'")

    raw_listings = []

    try:
        # 2. Call the Tavily Search API
        # We set search_depth='advanced' for better results, and max_results to limit the output.
        response = TAVILY.search(
            query=search_query, search_depth="advanced", max_results=10
        )

        # 3. Process the results
        # Tavily returns a list of source documents (links)
        for i, result in enumerate(response.get("results", []), 1):
            # We are extracting the link (url) and a descriptive title/snippet
            job_title = result.get("title") or f"Search Result {i}"
            url = result.get("url")

            # Since Tavily gives general search results, we manually structure the output
            # to fit the rest of our agent's expected format.
            raw_listings.append(
                {
                    "title": job_title,
                    "company": url.split("/")[2].replace(
                        "www.", ""
                    ),  # Extract domain as "company"
                    "location": location,
                    "summary": result.get("content") or "",
                    "url": url,
                }
            )

    except Exception as e:
        print(f"  Error fetching data from Tavily API: {e}")
        return []

    print(f"-> Tavily returned {len(raw_listings)} relevant search results.")
    return raw_listings
