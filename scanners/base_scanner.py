"""Base class for all scanners."""

from abc import ABC, abstractmethod
from typing import Optional
from youtube.models import YouTubeComment, ScanResult
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseScanner(ABC):
    """Abstract base class for all content scanners."""

    def __init__(self, country_filter: Optional[str] = None):
        """Initialize the scanner.

        Args:
            country_filter: Optional country code to filter results (e.g., 'AT', 'DE')
        """
        self.country_filter = country_filter
        self.scanner_type = self.__class__.__name__.replace("Scanner", "").lower()

    @abstractmethod
    def scan(self, comment: YouTubeComment) -> Optional[ScanResult]:
        """Scan a comment for matches.

        Args:
            comment: The comment to scan

        Returns:
            ScanResult if matches found, None otherwise
        """
        pass

    @abstractmethod
    def supports_country(self, country_code: str) -> bool:
        """Check if scanner supports a specific country.

        Args:
            country_code: The country code (e.g., 'AT', 'DE')

        Returns:
            True if country is supported, False otherwise
        """
        pass

    def get_supported_countries(self) -> list:
        """Get list of supported countries.

        Returns:
            List of country codes
        """
        return []
