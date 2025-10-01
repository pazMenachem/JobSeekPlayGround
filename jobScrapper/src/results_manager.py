"""Results management for saving and organizing found job URLs."""

import logging
import json
import os
from datetime import datetime
from typing import List, Set, Dict, Any
from pathlib import Path
from src.config import OUTPUT_FILE


class ResultsManager:
    """Manages saving and organizing found job results.
    
    This class handles the storage and retrieval of found job URLs,
    including deduplication and various output formats.
    """
    
    def __init__(self, output_file: str = OUTPUT_FILE) -> None:
        """Initialize the results manager.
        
        Args:
            output_file: Path to the output file for saving results.
        """
        self.output_file = output_file
        self.logger = logging.getLogger(__name__)
        self.found_jobs: Set[str] = set()
        self.results_data: List[Dict[str, Any]] = []
        self.run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_dir = self._create_results_directory()
    
    def _create_results_directory(self) -> Path:
        """Create a timestamped results directory for this run.
        
        Returns:
            Path to the created results directory.
        """
        results_base = Path("results")
        run_dir = results_base / f"run_{self.run_timestamp}"
        
        # Create the directory if it doesn't exist
        run_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Created results directory: {run_dir}")
        return run_dir
    
    def add_job_url(self, url: str, title: str = "", source_url: str = "") -> None:
        """Add a job URL to the results.
        
        Args:
            url: URL of the job listing.
            title: Title of the job (optional).
            source_url: URL of the page where this job was found (optional).
        """
        if url not in self.found_jobs:
            self.found_jobs.add(url)
            job_data = {
                "url": url,
                "title": title,
                "source_url": source_url,
                "found_at": datetime.now().isoformat()
            }
            self.results_data.append(job_data)
            self.logger.info(f"Added job URL: {url}")
    
    def add_job_urls(self, urls: List[str], source_url: str = "") -> None:
        """Add multiple job URLs to the results.
        
        Args:
            urls: List of job URLs to add.
            source_url: URL of the page where these jobs were found (optional).
        """
        for url in urls:
            self.add_job_url(url, source_url=source_url)
    
    def save_results(self, format_type: str = "txt") -> str:
        """Save results to file in specified format.
        
        Args:
            format_type: Format to save results in ('txt', 'json', 'csv').
            
        Returns:
            Path to the saved file.
        """
        if not self.found_jobs:
            self.logger.warning("No results to save")
            return ""
        
        match format_type:
            case "txt":
                return self._save_as_txt()
            case "json":
                return self._save_as_json()
            case "csv":
                return self._save_as_csv()
            case _:
                raise ValueError(f"Unsupported format type: {format_type}") 
        
    
    def _save_as_txt(self) -> str:
        """Save results as plain text file.
            
        Returns:
            Path to the saved file.
        """
        filename = f"jobs_{self.run_timestamp}.txt"
        filepath = self.results_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Job Scraping Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total jobs found: {len(self.found_jobs)}\n\n")
            
            for i, job_data in enumerate(self.results_data, 1):
                f.write(f"{i}. {job_data['url']}\n")
                if job_data.get('title'):
                    f.write(f"   Title: {job_data['title']}\n")
                if job_data.get('source_url'):
                    f.write(f"   Source: {job_data['source_url']}\n")
                f.write(f"   Found at: {job_data['found_at']}\n\n")
        
        self.logger.info(f"Results saved to: {filepath}")
        return str(filepath)
    
    def _save_as_json(self) -> str:
        """Save results as JSON file.
            
        Returns:
            Path to the saved file.
        """
        filename = f"jobs_{self.run_timestamp}.json"
        filepath = self.results_dir / filename
        
        output_data = {
            "metadata": {
                "total_jobs": len(self.found_jobs),
                "scraped_at": datetime.now().isoformat(),
                "output_file": str(filepath)
            },
            "jobs": self.results_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Results saved to: {filepath}")
        return str(filepath)
    
    def _save_as_csv(self) -> str:
        """Save results as CSV file.
            
        Returns:
            Path to the saved file.
        """
        import csv
        
        filename = f"jobs_{self.run_timestamp}.csv"
        filepath = self.results_dir / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if self.results_data:
                writer = csv.DictWriter(f, fieldnames=['url', 'title', 'source_url', 'found_at'])
                writer.writeheader()
                writer.writerows(self.results_data)
        
        self.logger.info(f"Results saved to: {filepath}")
        return str(filepath)
    
    def save_run_summary(self) -> str:
        """Save a summary file for this run.
        
        Returns:
            Path to the saved summary file.
        """
        summary_file = self.results_dir / "run_summary.txt"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"Job Scraper Run Summary\n")
            f.write("=" * 30 + "\n\n")
            f.write(f"Run Timestamp: {self.run_timestamp}\n")
            f.write(f"Total Jobs Found: {len(self.found_jobs)}\n")
            f.write(f"Unique URLs: {len(self.found_jobs)}\n")
            f.write(f"Run Directory: {self.results_dir}\n\n")
            
            if self.found_jobs:
                f.write("Found Job URLs:\n")
                f.write("-" * 20 + "\n")
                for i, url in enumerate(self.found_jobs, 1):
                    f.write(f"{i}. {url}\n")
            else:
                f.write("No jobs found in this run.\n")
        
        self.logger.info(f"Run summary saved to: {summary_file}")
        return str(summary_file)
    
    def get_results_summary(self) -> Dict[str, Any]:
        """Get a summary of the results.
        
        Returns:
            Dictionary containing results summary.
        """
        return {
            "total_jobs": len(self.found_jobs),
            "unique_urls": len(self.found_jobs),
            "scraped_at": datetime.now().isoformat(),
            "jobs": list(self.found_jobs)
        }
    
    def clear_results(self) -> None:
        """Clear all stored results."""
        self.found_jobs.clear()
        self.results_data.clear()
        self.logger.info("Results cleared")
    
    def load_results_from_file(self, filepath: str) -> bool:
        """Load results from a previously saved file.
        
        Args:
            filepath: Path to the file to load.
            
        Returns:
            True if loading was successful, False otherwise.
        """
        try:
            file_path = Path(filepath)
            
            if file_path.suffix == '.json':
                return self._load_from_json(file_path)
            elif file_path.suffix == '.txt':
                return self._load_from_txt(file_path)
            else:
                self.logger.error(f"Unsupported file format: {file_path.suffix}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error loading results from {filepath}: {e}")
            return False
    
    def _load_from_json(self, filepath: Path) -> bool:
        """Load results from JSON file.
        
        Args:
            filepath: Path to JSON file.
            
        Returns:
            True if loading was successful, False otherwise.
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if 'jobs' in data:
            for job in data['jobs']:
                self.add_job_url(
                    job.get('url', ''),
                    job.get('title', ''),
                    job.get('source_url', '')
                )
        
        return True
    
    def _load_from_txt(self, filepath: Path) -> bool:
        """Load results from text file.
        
        Args:
            filepath: Path to text file.
            
        Returns:
            True if loading was successful, False otherwise.
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('='):
                if line.startswith(('http://', 'https://')):
                    self.add_job_url(line)
        
        return True
