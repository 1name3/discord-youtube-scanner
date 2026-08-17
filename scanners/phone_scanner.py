"""Phone number scanner."""

import re
from typing import Optional

from scanners.base_scanner import BaseScanner
from youtube.models import YouTubeComment, ScanResult


class PhoneScanner(BaseScanner):
    """Detect phone numbers in YouTube comments."""

    COUNTRY_CODES = {
        "+43": "AT",
        "+49": "DE",
        "+41": "CH",
        "+44": "GB",
        "+1": "US/CA",
        "+33": "FR",
        "+39": "IT",
        "+34": "ES",
        "+31": "NL",
        "+32": "BE",
        "+48": "PL",
        "+46": "SE",
        "+47": "NO",
        "+45": "DK",
    }

    # International formats such as:
    # +43 660 1234567
    # +49-151-12345678
    # +1 (555) 123-4567
    INTERNATIONAL_PATTERN = re.compile(
        r"(?<![\d+])"
        r"\+\d{1,3}"
        r"(?:[\s./-]?\(?\d{1,4}\)?){2,5}"
        r"(?!\d)"
    )

    # Common local formats such as:
    # 0660 1234567
    # 030 12345678
    LOCAL_PATTERN = re.compile(
        r"(?<!\d)"
        r"(?:0\d{2,4})"
        r"(?:[\s./-]\d{2,4}){1,3}"
        r"(?!\d)"
    )

    def __init__(self, country_filter: Optional[str] = None):
        super().__init__(country_filter)
        self.scanner_type = "phone"
        self.country_filter = country_filter

    def scan(self, comment: YouTubeComment) -> Optional[ScanResult]:
        """Scan a comment for phone numbers."""

        text = comment.text

        matches = []

        # International numbers.
        matches.extend(self.INTERNATIONAL_PATTERN.findall(text))

        # Local numbers are only useful when a specific country
        # is selected, because otherwise their country is ambiguous.
        if self.country_filter:
            matches.extend(self.LOCAL_PATTERN.findall(text))

        valid_numbers = []

        for number in matches:
            number = number.strip()

            if not self.is_valid_phone_number(number):
                continue

            detected_country = self.detect_country(number)

            if self.country_filter:
                if detected_country != self.country_filter:
                    continue

            valid_numbers.append(number)

        if not valid_numbers:
            return None

        unique_numbers = list(dict.fromkeys(valid_numbers))

        masked_numbers = [
            self.mask_phone_number(number)
            for number in unique_numbers
        ]

        return ScanResult(
            comment=comment,
            scanner_type=self.scanner_type,
            matches={
                "phone_numbers": unique_numbers,
                "masked_numbers": masked_numbers,
            },
            confidence=0.95,
            masked_display=", ".join(masked_numbers),
        )

    def is_valid_phone_number(self, number: str) -> bool:
        """Check whether a detected string looks like a phone number."""

        digits = re.sub(r"\D", "", number)

        # International phone numbers normally contain 7-15 digits.
        if len(digits) < 7 or len(digits) > 15:
            return False

        # A phone number should contain several digits, but avoid
        # treating a random sequence in a huge text as a phone number.
        digit_count = sum(char.isdigit() for char in number)

        if digit_count < 7:
            return False

        # Reject numbers made almost entirely from one repeated digit.
        if len(set(digits)) <= 2:
            return False

        return True

    def detect_country(self, number: str) -> Optional[str]:
        """Detect the country from an international phone prefix."""

        number = number.strip()

        if not number.startswith("+"):
            return None

        for prefix, country in sorted(
            self.COUNTRY_CODES.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        ):
            if number.startswith(prefix):
                return country

        return None

    def mask_phone_number(self, number: str) -> str:
        """Mask most digits of a phone number."""

        digits = re.sub(r"\D", "", number)

        if len(digits) <= 4:
            return "***"

        visible = digits[-2:]

        if number.startswith("+"):
            prefix_match = re.match(r"^\+\d{1,3}", number)
            prefix = prefix_match.group(0) if prefix_match else "+"
            return f"{prefix} *** **{visible}"

        return f"*** *** **{visible}"

    def supports_country(self, country_code: str) -> bool:
        """Check whether a country is supported."""

        return country_code.upper() in self.get_supported_countries()

    def get_supported_countries(self) -> list:
        """Return supported country codes."""

        return list(self.COUNTRY_CODES.values())
