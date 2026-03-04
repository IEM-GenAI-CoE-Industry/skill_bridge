# agent_core.py
from typing import List, Dict


def preprocess_job_data(raw_jobs: List[Dict]) -> List[Dict]:
    """
    Cleans and standardizes job data (e.g., lowercasing, removing noise).

    :param raw_jobs: List of raw job dictionaries.
    :return: List of processed job dictionaries.
    """
    processed_jobs = []
    for job in raw_jobs:
        # Simple data cleaning: lowercasing for easier matching
        job["title_lower"] = job["title"].lower()
        job["summary_lower"] = job["summary"].lower()
        processed_jobs.append(job)
    return processed_jobs


def find_matching_jobs(raw_jobs: List[Dict], target_role: str) -> List[Dict]:
    """
    Filters job listings to find those that closely match the target role.

    :param raw_jobs: List of raw job dictionaries from the scraper.
    :param target_role: The user-specified role (e.g., 'Python developer').
    :return: A list of job dictionaries that match the criteria.
    """
    print(f"\n-> Filtering jobs to match the target role: '{target_role}'")

    processed_jobs = preprocess_job_data(raw_jobs)

    # Simple matching strategy: check if the target role words are in the title
    # or the summary. In a real agent, this would be more sophisticated (e.g., NLP).

    match_keywords = target_role.lower().split()

    matching_jobs = []
    for job in processed_jobs:
        title_matches = all(keyword in job["title_lower"] for keyword in match_keywords)

        # Optionally, check the summary as a secondary match
        # summary_matches = any(keyword in job['summary_lower'] for keyword in match_keywords)

        if title_matches:  # or summary_matches:
            # Revert to original keys for output
            matching_jobs.append(
                {
                    "title": job["title"],
                    "company": job["company"],
                    "location": job["location"],
                    "url": job["url"],
                }
            )

    return matching_jobs
