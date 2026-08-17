"""Data models for YouTube API objects."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class YouTubeVideo:
    """Represents a YouTube video."""

    video_id: str
    title: str
    channel_name: str
    published_at: datetime
    url: str
    thumbnail_url: Optional[str] = None
    comment_count: int = 0
    view_count: int = 0
    like_count: Optional[int] = None

    def __str__(self) -> str:
        """String representation."""
        return f"{self.title} by {self.channel_name}"


@dataclass
class YouTubeComment:
    """Represents a YouTube comment."""

    comment_id: str
    author: str
    text: str
    published_at: datetime
    video_id: str
    video_title: str
    url: str  # Direct link to the comment
    likes: int = 0
    reply_count: int = 0
    author_id: Optional[str] = None

    def __str__(self) -> str:
        """String representation."""
        truncated_text = self.text[:50] + "..." if len(self.text) > 50 else self.text
        return f"{self.author}: {truncated_text}"


@dataclass
class ScanResult:
    """Result of a scanner scan operation."""

    comment: YouTubeComment
    scanner_type: str  # "phone", "keyword", "email", etc.
    matches: dict = field(default_factory=dict)  # Scanner-specific matches
    confidence: float = 1.0  # 0.0-1.0
    metadata: Optional[dict] = None
    masked_display: str = ""  # Privacy-filtered version

    def __str__(self) -> str:
        """String representation."""
        return f"ScanResult({self.scanner_type}, confidence={self.confidence})"
