"""Scanner for finding custom keywords in YouTube comments."""

from typing import List, Optional

from scanners.base_scanner import BaseScanner
from youtube.models import YouTubeComment, ScanResult


class KeywordScanner(BaseScanner):
    """Scans YouTube comments for specified keywords."""

    scanner_type = "keyword"

    def __init__(
        self,
        keywords: Optional[List[str]] = None,
        country_filter: Optional[str] = None,
    ):
        """Initialize the keyword scanner.

        Args:
            keywords: Keywords to search for.
            country_filter: Optional country filter.
        """
        super().__init__(country_filter)

        self.keywords = [
            keyword.lower().strip()
            for keyword in (keywords or [])
            if keyword.strip()
        ]

    def scan(self, comment: YouTubeComment) -> Optional[ScanResult]:
        """Scan a comment for matching keywords.

        Args:
            comment: YouTube comment to scan.

        Returns:
            ScanResult if keywords are found, otherwise None.
        """
        if not self.keywords:
            return None

        comment_text = comment.text.lower()

        matches = [
            keyword
            for keyword in self.keywords
            if keyword in comment_text
        ]

        if not matches:
            return None

        return ScanResult(
            comment=comment,
            scanner_type=self.scanner_type,
            matches={"keywords": matches},
            confidence=1.0,
            masked_display=comment.text,
        )

    def supports_country(self, country_code: str) -> bool:
        """Check whether the scanner supports a country filter.

        Keyword scanning itself is not country-specific.
        """
        return True

    def get_supported_countries(self) -> List[str]:
        """Return supported countries.

        Keyword scanning supports all countries.
        """
        return []
