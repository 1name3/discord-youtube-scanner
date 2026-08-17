"""YouTube Data API integration."""

from datetime import datetime
from typing import List, Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import Config
from youtube.models import YouTubeComment, YouTubeVideo


class YouTubeAPI:
    """Wrapper around the YouTube Data API."""

    def __init__(self):
        """Initialize the YouTube API client."""
        self.youtube = build(
            "youtube",
            "v3",
            developerKey=Config.YOUTUBE_API_KEY,
        )

    def search_videos(
        self,
        query: str,
        max_results: int = 10,
    ) -> List[YouTubeVideo]:
        """Search YouTube for videos matching a query."""
        try:
            response = self.youtube.search().list(
                part="snippet",
                q=query,
                type="video",
                maxResults=min(max_results, 50),
            ).execute()

            video_ids = [
                item["id"]["videoId"]
                for item in response.get("items", [])
                if "videoId" in item.get("id", {})
            ]

            if not video_ids:
                return []

            details_response = self.youtube.videos().list(
                part="snippet,statistics",
                id=",".join(video_ids),
            ).execute()

            videos = []

            for item in details_response.get("items", []):
                snippet = item.get("snippet", {})
                statistics = item.get("statistics", {})

                published_at = self._parse_datetime(
                    snippet.get("publishedAt")
                )

                videos.append(
                    YouTubeVideo(
                        video_id=item["id"],
                        title=snippet.get("title", ""),
                        channel_name=snippet.get("channelTitle", ""),
                        published_at=published_at,
                        url=f"https://www.youtube.com/watch?v={item['id']}",
                        thumbnail_url=(
                            snippet.get("thumbnails", {})
                            .get("high", {})
                            .get("url")
                        ),
                        comment_count=int(
                            statistics.get("commentCount", 0)
                        ),
                        view_count=int(
                            statistics.get("viewCount", 0)
                        ),
                        like_count=(
                            int(statistics["likeCount"])
                            if "likeCount" in statistics
                            else None
                        ),
                    )
                )

            return videos

        except HttpError as e:
            raise RuntimeError(
                f"YouTube API error while searching videos: {e}"
            ) from e

    def get_video(
        self,
        video_id: str,
    ) -> Optional[YouTubeVideo]:
        """Get a single YouTube video by its ID."""
        try:
            response = self.youtube.videos().list(
                part="snippet,statistics",
                id=video_id,
            ).execute()

            items = response.get("items", [])

            if not items:
                return None

            item = items[0]
            snippet = item.get("snippet", {})
            statistics = item.get("statistics", {})

            published_at = self._parse_datetime(
                snippet.get("publishedAt")
            )

            return YouTubeVideo(
                video_id=item["id"],
                title=snippet.get("title", ""),
                channel_name=snippet.get("channelTitle", ""),
                published_at=published_at,
                url=f"https://www.youtube.com/watch?v={item['id']}",
                thumbnail_url=(
                    snippet.get("thumbnails", {})
                    .get("high", {})
                    .get("url")
                ),
                comment_count=int(
                    statistics.get("commentCount", 0)
                ),
                view_count=int(
                    statistics.get("viewCount", 0)
                ),
                like_count=(
                    int(statistics["likeCount"])
                    if "likeCount" in statistics
                    else None
                ),
            )

        except HttpError as e:
            raise RuntimeError(
                f"YouTube API error while getting video: {e}"
            ) from e

    def get_comments(
        self,
        video: YouTubeVideo,
        max_results: int = 100,
    ) -> List[YouTubeComment]:
        """Get top-level comments from a YouTube video."""
        comments = []

        try:
            response = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video.video_id,
                maxResults=min(max_results, 100),
                textFormat="plainText",
            ).execute()

            for item in response.get("items", []):
                comment = item.get("snippet", {}).get(
                    "topLevelComment", {}
                )

                snippet = comment.get("snippet", {})

                published_at = self._parse_datetime(
                    snippet.get("publishedAt")
                )

                comment_id = comment.get(
                    "id",
                    item.get("id", ""),
                )

                comments.append(
                    YouTubeComment(
                        comment_id=comment_id,
                        author=snippet.get(
                            "authorDisplayName",
                            "",
                        ),
                        text=snippet.get(
                            "textDisplay",
                            "",
                        ),
                        published_at=published_at,
                        video_id=video.video_id,
                        video_title=video.title,
                        url=(
                            f"https://www.youtube.com/watch?v="
                            f"{video.video_id}"
                            f"&lc={comment_id}"
                        ),
                        likes=int(
                            snippet.get(
                                "likeCount",
                                0,
                            )
                        ),
                        reply_count=int(
                            item.get("snippet", {}).get(
                                "totalReplyCount",
                                0,
                            )
                        ),
                        author_id=snippet.get(
                            "authorChannelId",
                            {}).get("value")
                        if snippet.get("authorChannelId")
                        else None,
                    )
                )

            return comments

        except HttpError as e:
            if e.resp.status == 403:
                raise RuntimeError(
                    "YouTube comments could not be accessed. "
                    "Comments may be disabled or the API quota "
                    "may be exhausted."
                ) from e

            raise RuntimeError(
                f"YouTube API error while getting comments: {e}"
            ) from e

    @staticmethod
    def _parse_datetime(value: Optional[str]) -> datetime:
        """Convert a YouTube ISO timestamp to a datetime."""
        if not value:
            return datetime.now()

        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
```

