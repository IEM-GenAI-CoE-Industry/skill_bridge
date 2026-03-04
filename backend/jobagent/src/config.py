# src/config.py

# ==============================================================================
# 1. TAVILY API CONFIGURATION
# ==============================================================================

# IMPORTANT: Replace "YOUR_TAVILY_API_KEY_HERE" with your actual Tavily API key.
TAVILY_API_KEY = "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"

# Default values for search
DEFAULT_LOCATION = "remote"

# ==============================================================================
# 2. HTML SELECTORS (These are now redundant but kept for future use if needed)
# ==============================================================================

# Since we are using an API, these selectors are mostly unused.
SELECTORS = {
    "listing_container": "div.jobsearch-SerpJobCard",
    "job_title": "h2.jobTitle a",
    "company_name": "span.companyName",
    "location": "div.companyLocation",
    "summary": "div.job-snippet",
    "job_url_attr": "href",
}

# Standard headers and timeout (used for general requests, if any)
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

REQUEST_TIMEOUT = 10
