"""Example usage of the job scraper application."""

import logging
from webdriver_manager import WebDriverManager
from job_scraper import JobScraper
from url_manager import URLManager
from results_manager import ResultsManager


def example_basic_usage():
    """Example of basic usage with predefined URLs and keywords."""
    print("=== Basic Usage Example ===")
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Define your target URLs
    urls = [
        "https://www.indeed.com/jobs?q=python+developer&l=Remote",
        "https://www.linkedin.com/jobs/search/?keywords=software%20engineer&location=Remote"
    ]
    
    # Define keywords to search for
    keywords = ["python", "developer", "software engineer", "remote"]
    
    try:
        with WebDriverManager() as driver:
            # Initialize components
            job_scraper = JobScraper(driver)
            url_manager = URLManager(driver)
            results_manager = ResultsManager()
            
            print(f"Scraping {len(urls)} URLs for keywords: {keywords}")
            
            # Process URLs
            found_jobs = url_manager.process_urls(
                urls,
                lambda: job_scraper.find_jobs_with_keywords(keywords)
            )
            
            # Save results
            if found_jobs:
                results_manager.add_job_urls(found_jobs)
                saved_file = results_manager.save_results("json")
                print(f"Found {len(found_jobs)} jobs and saved to {saved_file}")
            else:
                print("No jobs found matching the keywords")
                
    except Exception as e:
        print(f"Error: {e}")


def example_custom_configuration():
    """Example with custom configuration and specific job sites."""
    print("\n=== Custom Configuration Example ===")
    
    # Custom keywords for specific roles
    keywords = [
        "data scientist",
        "machine learning engineer", 
        "ML engineer",
        "data analyst",
        "python developer"
    ]
    
    # Specific job sites
    urls = [
        "https://www.indeed.com/jobs?q=data+scientist&l=New+York%2C+NY",
        "https://www.glassdoor.com/Job/new-york-data-scientist-jobs-SRCH_IL.0,8_IC1132348_KO9,23.htm"
    ]
    
    try:
        with WebDriverManager() as driver:
            job_scraper = JobScraper(driver)
            url_manager = URLManager(driver)
            results_manager = ResultsManager("custom_jobs.json")
            
            print(f"Searching for data science roles in: {urls}")
            
            # Process each URL individually for more control
            for url in urls:
                print(f"\nProcessing: {url}")
                
                if url_manager.navigate_to_url(url):
                    # Search for jobs on current page
                    page_jobs = job_scraper.find_jobs_with_keywords(keywords)
                    results_manager.add_job_urls(page_jobs, source_url=url)
                    
                    # Handle pagination
                    while url_manager.go_to_next_page():
                        page_jobs = job_scraper.find_jobs_with_keywords(keywords)
                        results_manager.add_job_urls(page_jobs, source_url=url)
            
            # Save in multiple formats
            json_file = results_manager.save_results("json")
            txt_file = results_manager.save_results("txt")
            
            print(f"Results saved to: {json_file} and {txt_file}")
            
    except Exception as e:
        print(f"Error: {e}")


def example_single_url_scraping():
    """Example of scraping a single URL with detailed control."""
    print("\n=== Single URL Scraping Example ===")
    
    url = "https://www.indeed.com/jobs?q=python+developer&l=San+Francisco%2C+CA"
    keywords = ["python", "django", "flask", "fastapi", "backend"]
    
    try:
        with WebDriverManager() as driver:
            job_scraper = JobScraper(driver)
            url_manager = URLManager(driver)
            results_manager = ResultsManager()
            
            print(f"Scraping single URL: {url}")
            
            if url_manager.navigate_to_url(url):
                page_count = 1
                
                while True:
                    print(f"Processing page {page_count}")
                    
                    # Find jobs on current page
                    jobs = job_scraper.find_jobs_with_keywords(keywords)
                    results_manager.add_job_urls(jobs, source_url=url)
                    
                    print(f"Found {len(jobs)} jobs on page {page_count}")
                    
                    # Try to go to next page
                    if not url_manager.go_to_next_page():
                        break
                    
                    page_count += 1
                    
                    # Limit pages to avoid infinite loops
                    if page_count > 5:
                        print("Reached page limit")
                        break
                
                # Save results
                if results_manager.found_jobs:
                    saved_file = results_manager.save_results("json")
                    print(f"Total jobs found: {len(results_manager.found_jobs)}")
                    print(f"Results saved to: {saved_file}")
                else:
                    print("No jobs found")
            else:
                print("Failed to navigate to URL")
                
    except Exception as e:
        print(f"Error: {e}")


def example_results_analysis():
    """Example of analyzing and working with results."""
    print("\n=== Results Analysis Example ===")
    
    # This would typically load from a previously saved file
    results_manager = ResultsManager()
    
    # Simulate some results (in real usage, load from file)
    sample_jobs = [
        "https://example.com/job/1",
        "https://example.com/job/2", 
        "https://example.com/job/3"
    ]
    
    results_manager.add_job_urls(sample_jobs)
    
    # Get summary
    summary = results_manager.get_results_summary()
    print(f"Results summary: {summary}")
    
    # Save in different formats
    json_file = results_manager.save_results("json")
    txt_file = results_manager.save_results("txt")
    csv_file = results_manager.save_results("csv")
    
    print(f"Results saved in multiple formats:")
    print(f"- JSON: {json_file}")
    print(f"- Text: {txt_file}")
    print(f"- CSV: {csv_file}")


if __name__ == "__main__":
    print("Job Scraper - Example Usage")
    print("=" * 40)
    
    # Run examples
    example_basic_usage()
    example_custom_configuration() 
    example_single_url_scraping()
    example_results_analysis()
    
    print("\n" + "=" * 40)
    print("Examples completed!")
    print("\nTo run the main application:")
    print("python main.py")
