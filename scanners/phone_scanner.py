"""Phone number scanner."""

import re
from typing import Optional

from scanners.base_scanner import BaseScanner
from youtube.models import YouTubeComment, ScanResult


class PhoneScanner(BaseScanner):
    """Detect phone numbers in YouTube comments."""

    PHONE_PATTERNS = [
        re.compile(
            r"(?<!\d)"
            r"(?:\+\d{1,3}[\s./-]?)"
            r"(?:\(?\d{1,4}\)?[\s./-]?)"
            r"(?:\d[\s./-]?){5,12}"
            r"(?!\d)"
        ),
    ]

    COUNTRY_CODES = {
        "+43": "AT",
        "+49": "DE",
        "+41": "CH",
        "+44": "GB",
        "+33": "FR",
        "+39": "IT",
        "+34": "ES",
        "+31": "NL",
        "+32": "BE",
        "+48": "PL",
        "+46": "SE",
        "+47": "NO",
        "+45": "DK",
        "+1": "US/CA",
    }

    def __init__(self, country_filter: Optional[str] = None):
        super().__init__(country_filter)
        self.scanner_type = "phone"

    def scan(self, comment: YouTubeComment) -> Optional[ScanResult]:
        """Scan a comment for phone numbers."""

        matches = []

        for pattern in self.PHONE_PATTERNS:
            matches.extend(pattern.findall(comment.text))

        if not matches:
            return None

        unique_matches = list(dict.fromkeys(matches))

        masked_numbers = [
            self.mask_phone_number(number)
            for number in unique_matches
        ]

        return ScanResult(
            comment=comment,
            scanner_type=self.scanner_type,
            matches={
                "phone_numbers": unique_matches,
                "masked_numbers": masked_numbers,
            },
            confidence=0.95,
            masked_display=", ".join(masked_numbers),
        )

    def mask_phone_number(self, number: str) -> str:
        """Mask most digits of a phone number."""

        digits = re.sub(r"\D", "", number)

        if len(digits) <= 4:
            return "***"

        visible = digits[-2:]
        prefix = number[:3] if number.startswith("+") else ""

        return f"{prefix} *** **{visible}"

    def supports_country(self, country_code: str) -> bool:
        """Check whether a country is supported."""

        return country_code.upper() in self.get_supported_countries()

    def get_supported_countries(self) -> list:
        """Return supported country codes."""

        return list(self.COUNTRY_CODES.values())
