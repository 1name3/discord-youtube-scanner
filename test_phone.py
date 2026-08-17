from scanners.phone_scanner import PhoneScanner
from youtube.models import YouTubeComment
from datetime import datetime, timezone

comment = YouTubeComment(
    comment_id="test",
    author="TestUser",
    text="Call me at +43 660 1234567",
    published_at=datetime.now(timezone.utc),
    video_id="test",
    video_title="Test Video",
    url="https://youtube.com/",
)

scanner = PhoneScanner()

result = scanner.scan(comment)

if result:
    print("✅ Telefonnummer erkannt!")
    print("Gefunden:", result.matches["phone_numbers"])
    print("Maskiert:", result.masked_display)
else:
    print("❌ Keine Telefonnummer erkannt.")
