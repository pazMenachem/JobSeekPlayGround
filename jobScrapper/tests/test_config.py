"""Tests for configuration settings."""

import pytest
from src.config import (
    DEFAULT_KEYWORDS,
    TARGET_URLS,
    JOB_TITLE_SELECTORS,
    NEXT_PAGE_SELECTORS,
    OUTPUT_FILE,
    LOG_LEVEL,
    SCROLL_PAUSE_TIME,
    PAGE_LOAD_TIMEOUT
)


class TestConfig:
    """Test configuration settings."""
    
    @pytest.mark.unit
    def test_default_keywords_exist(self):
        """Test that default keywords are defined."""
        assert DEFAULT_KEYWORDS is not None
        assert isinstance(DEFAULT_KEYWORDS, list)
        assert len(DEFAULT_KEYWORDS) > 0
        assert all(isinstance(keyword, str) for keyword in DEFAULT_KEYWORDS)
    
    @pytest.mark.unit
    def test_default_keywords_content(self):
        """Test that default keywords contain expected values."""
        # Check that we have at least one keyword
        assert len(DEFAULT_KEYWORDS) > 0
        # Check that all keywords are strings
        assert all(isinstance(keyword, str) for keyword in DEFAULT_KEYWORDS)
        # Check that keywords are not empty
        assert all(keyword.strip() != "" for keyword in DEFAULT_KEYWORDS)
    
    @pytest.mark.unit
    def test_target_urls_exist(self):
        """Test that target URLs are defined."""
        assert TARGET_URLS is not None
        assert isinstance(TARGET_URLS, list)
        assert len(TARGET_URLS) > 0
        assert all(isinstance(url, str) for url in TARGET_URLS)
    
    @pytest.mark.unit
    def test_target_urls_valid(self):
        """Test that target URLs are valid."""
        for url in TARGET_URLS:
            assert url.startswith(("http://", "https://"))
            assert "." in url  # Should contain domain
    
    @pytest.mark.unit
    def test_job_title_selectors_exist(self):
        """Test that job title selectors are defined."""
        assert JOB_TITLE_SELECTORS is not None
        assert isinstance(JOB_TITLE_SELECTORS, list)
        assert len(JOB_TITLE_SELECTORS) > 0
        assert all(isinstance(selector, str) for selector in JOB_TITLE_SELECTORS)
    
    @pytest.mark.unit
    def test_job_title_selectors_valid(self):
        """Test that job title selectors are valid CSS selectors."""
        for selector in JOB_TITLE_SELECTORS:
            assert selector.strip() != ""
            # Basic CSS selector validation
            assert not selector.startswith(" ")
            assert not selector.endswith(" ")
    
    @pytest.mark.unit
    def test_next_page_selectors_exist(self):
        """Test that next page selectors are defined."""
        assert NEXT_PAGE_SELECTORS is not None
        assert isinstance(NEXT_PAGE_SELECTORS, list)
        assert len(NEXT_PAGE_SELECTORS) > 0
        assert all(isinstance(selector, str) for selector in NEXT_PAGE_SELECTORS)
    
    @pytest.mark.unit
    def test_next_page_selectors_variations(self):
        """Test that next page selectors include different variations."""
        selectors_text = " ".join(NEXT_PAGE_SELECTORS).lower()
        # Should include different case variations
        assert "next" in selectors_text or "Next" in " ".join(NEXT_PAGE_SELECTORS)
        # Should include different attribute variations
        assert any("aria-label" in selector for selector in NEXT_PAGE_SELECTORS)
    
    @pytest.mark.unit
    def test_output_file_defined(self):
        """Test that output file is defined."""
        assert OUTPUT_FILE is not None
        assert isinstance(OUTPUT_FILE, str)
        assert OUTPUT_FILE.strip() != ""
    
    @pytest.mark.unit
    def test_log_level_valid(self):
        """Test that log level is valid."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        assert LOG_LEVEL.upper() in valid_levels
    
    @pytest.mark.unit
    def test_scroll_pause_time_positive(self):
        """Test that scroll pause time is positive."""
        assert SCROLL_PAUSE_TIME > 0
        assert isinstance(SCROLL_PAUSE_TIME, (int, float))
    
    @pytest.mark.unit
    def test_page_load_timeout_positive(self):
        """Test that page load timeout is positive."""
        assert PAGE_LOAD_TIMEOUT > 0
        assert isinstance(PAGE_LOAD_TIMEOUT, (int, float))
    
    @pytest.mark.unit
    def test_config_consistency(self):
        """Test that configuration values are consistent."""
        # All lists should not be empty
        assert len(DEFAULT_KEYWORDS) > 0
        assert len(TARGET_URLS) > 0
        assert len(JOB_TITLE_SELECTORS) > 0
        assert len(NEXT_PAGE_SELECTORS) > 0
        
        # Timeout values should be reasonable
        assert 1 <= SCROLL_PAUSE_TIME <= 10
        assert 5 <= PAGE_LOAD_TIMEOUT <= 60
    
    @pytest.mark.unit
    def test_no_duplicate_keywords(self):
        """Test that there are no duplicate keywords."""
        keywords_lower = [kw.lower() for kw in DEFAULT_KEYWORDS]
        assert len(keywords_lower) == len(set(keywords_lower))
    
    @pytest.mark.unit
    def test_no_duplicate_urls(self):
        """Test that there are no duplicate URLs."""
        assert len(TARGET_URLS) == len(set(TARGET_URLS))
    
    @pytest.mark.unit
    def test_no_duplicate_selectors(self):
        """Test that there are no duplicate selectors."""
        assert len(JOB_TITLE_SELECTORS) == len(set(JOB_TITLE_SELECTORS))
        assert len(NEXT_PAGE_SELECTORS) == len(set(NEXT_PAGE_SELECTORS))
