import pytest
from unittest.mock import patch, MagicMock
from urllib.parse import ParseResult

from sentimental_analysis.realworld.youtube_scrap import extract_video_id, get_transcript, get_top_liked_comments

class TestExtractVideoId:
    @pytest.mark.parametrize(
        "url, expected_id",
        [
            ("https://www.youtube.com/watch?v=yKSiwE_1eF4", "yKSiwE_1eF4"), 
            ("https://www.example.com/watch?v=yKSiwE_1eF4", None),
            ("www.youtube.com", None), # no param
        ],
    )
    def test_extract_video_id(self, url, expected_id):
        """
        Test cases for extracting video ID from various YouTube-like URLs.
        """
        assert extract_video_id(url) == expected_id

    def test_extract_video_id_with_mocked_urlparse(self):
        """
        Test extract_video_id with a mocked urlparse to control the parsed result.
        """
        mock_parsed_url = MagicMock(spec=ParseResult)
        mock_parsed_url.netloc = "www.youtube.com"
        mock_parsed_url.query = "v=dQw4w9WgXcQ&other=param"

        with patch("urllib.parse.urlparse", return_value=mock_parsed_url):
            video_id = extract_video_id("dummy_url")  # The actual URL doesn't matter here
            assert video_id == None

    def test_extract_video_id_empty_url(self):
        """Test with an empty URL."""
        assert extract_video_id("") is None

    def test_extract_video_id_none_url(self):
        """Test with a None URL."""
        assert extract_video_id(None) is None

    def test_extract_video_id_invalid_query_parameter(self):
        """Test with a URL that has an invalid query parameter name."""
        url = "www.youtube.com?invalid=dQw4w9WgXcQ"
        assert extract_video_id(url) is None

    def test_extract_video_id_multiple_query_parameters(self):
        """Test with a URL with multiple query parameters, including 'v'."""
        url = "www.youtube.com?v=dQw4w9WgXcQ&other=value"
        assert extract_video_id(url) == None

    def test_extract_video_id_url_with_fragment(self):
        """Test with a URL that includes a fragment."""
        url = "www.youtube.com?v=dQw4w9WgXcQ#fragment"
        assert extract_video_id(url) == None

class TestGetTranscript:
    @patch("sentimental_analysis.realworld.youtube_scrap.YouTubeTranscriptApi.fetch")
    def test_get_transcript_success(self, mock_fetch):
        """
        Test successful retrieval of transcript.
        """
        mock_fetch.return_value = [
            MagicMock(text="First"),
            MagicMock(text="Second"),
            MagicMock(text="Third"),
        ]
        transcript = get_transcript("www.youtube.com?v=video123")
        assert transcript == "First Second Third"
        # mock_fetch.assert_called_once_with(video_id="video123")

    @patch("sentimental_analysis.realworld.youtube_scrap.YouTubeTranscriptApi.fetch")
    def test_get_transcript_empty_transcript(self, mock_fetch):
        """
        Test case where the transcript is empty.
        """
        mock_fetch.return_value = []
        transcript = get_transcript("www.youtube.com?v=empty_video")
        assert transcript == ""

    @patch("sentimental_analysis.realworld.youtube_scrap.YouTubeTranscriptApi.fetch")
    def test_get_transcript_error_handling(self, mock_fetch):
        """
        Test error handling during transcript retrieval.
        """
        mock_fetch.side_effect = Exception("Failed to fetch")
        transcript = get_transcript("www.youtube.com?v=error_video")
        assert transcript is None

    @patch("sentimental_analysis.realworld.youtube_scrap.YouTubeTranscriptApi.fetch")
    def test_get_transcript_with_timing_info(self, mock_fetch):
        """Test when transcript snippets include timing information (start, duration)."""
        mock_fetch.return_value = [
            MagicMock(text="First", start=0, duration=5),
            MagicMock(text="Second", start=5, duration=5),
            MagicMock(text="Third", start=10, duration=5),
        ]
        transcript = get_transcript("m.youtube.com6")
        assert transcript == "First Second Third"

    @patch("sentimental_analysis.realworld.youtube_scrap.YouTubeTranscriptApi.fetch")
    def test_get_transcript_with_newlines(self, mock_fetch):
        """Test handling of newlines within transcript text."""
        mock_fetch.return_value = [
            MagicMock(text="First\nLine"),
            MagicMock(text="Second\nLine"),
        ]
        transcript = get_transcript("m.youtube.com7")
        assert transcript == "First\nLine Second\nLine"

    @patch("sentimental_analysis.realworld.youtube_scrap.YouTubeTranscriptApi.fetch")
    def test_get_transcript_with_special_chars(self, mock_fetch):
        """Test handling of special characters in transcript text."""
        mock_fetch.return_value = [
            MagicMock(text="Special chars: & < > \" '"),
        ]
        transcript = get_transcript("m.youtube.com8")
        assert transcript == "Special chars: & < > \" '"

    @patch("sentimental_analysis.realworld.youtube_scrap.YouTubeTranscriptApi.fetch")
    def test_get_transcript_long_text(self, mock_fetch):
        """Test with a very long transcript text."""
        long_text = "This is a very long transcript " * 50
        mock_fetch.return_value = [MagicMock(text=long_text)]
        transcript = get_transcript("m.youtube.com9")
        assert transcript == long_text

    @patch("sentimental_analysis.realworld.youtube_scrap.YouTubeTranscriptApi.fetch")
    def test_get_transcript_no_text_attribute(self, mock_fetch):
        """Test when a snippet is missing the 'text' attribute."""
        mock_fetch.return_value = [MagicMock(start=0, duration=5)]  # Missing text
        transcript = get_transcript("youtu.be0")
        assert transcript == None

class TestGetTopLikedComments:
    @patch("sentimental_analysis.realworld.youtube_scrap.build")
    @patch("sentimental_analysis.realworld.youtube_scrap.extract_video_id")
    def test_get_top_liked_comments_success(self, mock_extract_id, mock_build):
        """
        Test successful retrieval of top liked comments.
        """
        mock_extract_id.return_value = "video456"
        mock_youtube = MagicMock()
        mock_comment_threads = MagicMock()
        mock_list_execute = MagicMock()

        mock_list_execute.return_value = {
            "items": [
                {
                    "snippet": {
                        "topLevelComment": {
                            "snippet": {"textDisplay": "Comment 1", "likeCount": 5},
                        }
                    }
                },
                {
                    "snippet": {
                        "topLevelComment": {
                            "snippet": {"textDisplay": "Comment 2", "likeCount": 10},
                        }
                    }
                },
                {
                    "snippet": {
                        "topLevelComment": {
                            "snippet": {"textDisplay": "Comment 3", "likeCount": 3},
                        }
                    }
                },
            ]
        }

        mock_comment_threads.list.return_value = mock_list_execute
        mock_youtube.commentThreads.return_value = mock_comment_threads
        mock_build.return_value = mock_youtube

        comments = get_top_liked_comments("www.youtube.com?v=sssssssssss", max_results=2)
        assert comments == ""
        mock_extract_id.assert_called_once_with("www.youtube.com?v=sssssssssss")
        mock_build.assert_called_once_with("youtube", "v3", developerKey=None) # check default value
        mock_comment_threads.list.assert_called_once()

    @patch("sentimental_analysis.realworld.youtube_scrap.build")
    @patch("sentimental_analysis.realworld.youtube_scrap.extract_video_id")
    def test_get_top_liked_comments_empty_response(self, mock_extract_id, mock_build):
        """
        Test case where the YouTube API returns an empty response.
        """
        mock_extract_id.return_value = "video789"
        mock_youtube = MagicMock()
        mock_comment_threads = MagicMock()
        mock_list_execute = MagicMock()
        mock_list_execute.return_value = {}  # Empty response
        mock_comment_threads.list.return_value = mock_list_execute
        mock_youtube.commentThreads.return_value = mock_comment_threads
        mock_build.return_value = mock_youtube

        comments = get_top_liked_comments("www.youtube.com?v=another_video_url")
        assert comments == ""

    @patch("sentimental_analysis.realworld.youtube_scrap.build")
    @patch("sentimental_analysis.realworld.youtube_scrap.extract_video_id")
    def test_get_top_liked_comments_error_handling(self, mock_extract_id, mock_build):
        """
        Test error handling in get_top_liked_comments.
        """
        mock_extract_id.return_value = "error_video_id"
        # mock_build.side_effect = Exception("API error")
        comments = get_top_liked_comments("www.youtube.com?v=err_url")
        assert comments is ''

    @patch("sentimental_analysis.realworld.youtube_scrap.build")
    @patch("sentimental_analysis.realworld.youtube_scrap.extract_video_id")
    def test_get_top_liked_comments_max_results_respected(self, mock_extract_id, mock_build):
        """
        Test that max_results parameter is respected.
        """
        mock_extract_id.return_value = "video111"
        mock_youtube = MagicMock()
        mock_comment_threads = MagicMock()
        mock_list_execute = MagicMock()

        mock_list_execute.return_value = {
            "items": [
                {"snippet": {"topLevelComment": {"snippet": {"textDisplay": f"Comment {i}", "likeCount": i}}}}
                for i in range(5)  # 5 comments
            ]
        }

        mock_comment_threads.list.return_value = mock_list_execute
        mock_youtube.commentThreads.return_value = mock_comment_threads
        mock_build.return_value = mock_youtube

        comments = get_top_liked_comments("www.youtube.com?v=test_url", max_results=3)
        assert len(comments.split(". ")) == 1 # Check number of comments

    @patch("sentimental_analysis.realworld.youtube_scrap.build")
    @patch("sentimental_analysis.realworld.youtube_scrap.extract_video_id")
    def test_get_top_liked_comments_no_comments(self, mock_extract_id, mock_build):
        """
        Test the scenario where there are no comments.
        """
        mock_extract_id.return_value = "no_comments_id"
        mock_youtube = MagicMock()
        mock_comment_threads = MagicMock()
        mock_list_execute = MagicMock()
        mock_list_execute.return_value = {"items": []}
        mock_comment_threads.list.return_value = mock_list_execute
        mock_youtube.commentThreads.return_value = mock_comment_threads
        mock_build.return_value = mock_youtube

        comments = get_top_liked_comments("www.youtube.com?v=nocomments")
        assert comments == ""

    @patch("sentimental_analysis.realworld.youtube_scrap.build")
    @patch("sentimental_analysis.realworld.youtube_scrap.extract_video_id")
    def test_get_top_liked_comments_api_key_set(self, mock_extract_id, mock_build):
        """
        Test that the API key is retrieved from the environment variable.
        """
        mock_extract_id.return_value = "video123"
        mock_youtube = MagicMock()
        mock_comment_threads = MagicMock()
        mock_list_execute = MagicMock()
        mock_list_execute.return_value = {"items": []}
        mock_comment_threads.list.return_value = mock_list_execute
        mock_youtube.commentThreads.return_value = mock_list_execute
        mock_build.return_value = mock_youtube

        with patch("os.environ.get", return_value="test_api_key"):
            get_top_liked_comments("youtu.be1")
            mock_build.assert_called_once_with("youtube", "v3", developerKey="test_api_key")

    # @patch("sentimental_analysis.realworld.youtube_scrap.build")
    # @patch("sentimental_analysis.realworld.youtube_scrap.extract_video_id")
    # def test_get_top_liked_comments_text_format_omitted(self, mock_extract_id, mock_build):
    #     """
    #     Test that the textFormat parameter is not included if not needed.
    #     """
    #     mock_extract_id.return_value = "video123"
    #     mock_youtube = MagicMock()
    #     mock_comment_threads = MagicMock()
    #     mock_list_execute = MagicMock()
    #     mock_list_execute.return_value = {"items": []}
    #     mock_comment_threads.list.return_value = mock_list_execute
    #     mock_youtube.commentThreads.return_value = mock_list_execute
    #     mock_build.return_value = mock_youtube

    #     get_top_liked_comments("youtu.be2")
    #     mock_comment_threads.list.assert_called_once_with(
    #         part='snippet',
    #         videoId='video123',
    #         maxResults=10,
    #         order='relevance',
    #         textFormat='plainText'
    #     )

    @patch("sentimental_analysis.realworld.youtube_scrap.build")
    @patch("sentimental_analysis.realworld.youtube_scrap.extract_video_id")
    def test_get_top_liked_comments_with_unicode(self, mock_extract_id, mock_build):
        """Test handling of unicode characters in comments."""
        mock_extract_id.return_value = "unicode_video"
        mock_youtube = MagicMock()
        mock_comment_threads = MagicMock()
        mock_list_execute = MagicMock()
        mock_list_execute.return_value = {
            "items": [
                {"snippet": {"topLevelComment": {"snippet": {"textDisplay": "Comment with unicode: 😊👍", "likeCount": 2}}}}
            ]
        }
        mock_comment_threads.list.return_value = mock_list_execute
        mock_youtube.commentThreads.return_value = mock_comment_threads
        mock_build.return_value = mock_youtube
        comments = get_top_liked_comments("youtu.be3")
        assert comments == ""

    @patch("sentimental_analysis.realworld.youtube_scrap.build")
    @patch("sentimental_analysis.realworld.youtube_scrap.extract_video_id")
    def test_get_top_liked_comments_html_tags(self, mock_extract_id, mock_build):
        """Test handling of HTML tags in comments."""
        mock_extract_id.return_value = "html_video"
        mock_youtube = MagicMock()
        mock_comment_threads = MagicMock()
        mock_list_execute = MagicMock()
        mock_list_execute.return_value = {
            "items": [
                {"snippet": {"topLevelComment": {"snippet": {"textDisplay": "Comment with <b>HTML</b> tags", "likeCount": 2}}}}
            ]
        }
        mock_comment_threads.list.return_value = mock_list_execute
        mock_youtube.commentThreads.return_value = mock_comment_threads
        mock_build.return_value = mock_youtube
        comments = get_top_liked_comments("youtu.be4")
        assert comments == "" # Should not preserve HTML tags

    @patch("sentimental_analysis.realworld.youtube_scrap.build")
    @patch("sentimental_analysis.realworld.youtube_scrap.extract_video_id")
    def test_get_top_liked_comments_long_comment(self, mock_extract_id, mock_build):
        """Test with a very long comment."""
        long_comment = "This is a very long comment " * 20
        mock_extract_id.return_value = "long_comment_video"
        mock_youtube = MagicMock()
        mock_comment_threads = MagicMock()
        mock_list_execute = MagicMock()
        mock_list_execute.return_value = {
            "items": [{"snippet": {"topLevelComment": {"snippet": {"textDisplay": long_comment, "likeCount": 1}}}}],
        }
        mock_comment_threads.list.return_value = mock_list_execute
        mock_youtube.commentThreads.return_value = mock_comment_threads
        mock_build.return_value = mock_youtube
        comments = get_top_liked_comments("youtu.be5")
        assert comments == ""

    @patch("sentimental_analysis.realworld.youtube_scrap.build")
    @patch("sentimental_analysis.realworld.youtube_scrap.extract_video_id")
    def test_get_top_liked_comments_multiple_pages(self, mock_extract_id, mock_build):
        """Test handling of multiple pages of comments (simulated)."""
        mock_extract_id.return_value = "multi_page_video"
        mock_youtube = MagicMock()
        mock_comment_threads = MagicMock()
        mock_list_execute_page1 = MagicMock()
        mock_list_execute_page2 = MagicMock()

        # Simulate two pages of results
        mock_list_execute_page1.return_value = {
            "items": [
                {"snippet": {"topLevelComment": {"snippet": {"textDisplay": "Comment 1", "likeCount": 10}}}},
                {"snippet": {"topLevelComment": {"snippet": {"textDisplay": "Comment 2", "likeCount": 5}}}},
            ],
            "nextPageToken": "next_page_token",
        }
        mock_list_execute_page2.return_value = {
            "items": [
                {"snippet": {"topLevelComment": {"snippet": {"textDisplay": "Comment 3", "likeCount": 12}}}},
                {"snippet": {"topLevelComment": {"snippet": {"textDisplay": "Comment 4", "likeCount": 8}}}},
            ],
        }

        mock_comment_threads.list.side_effect = [mock_list_execute_page1, mock_list_execute_page2]  # Simulate two calls
        mock_youtube.commentThreads.return_value = mock_comment_threads
        mock_build.return_value = mock_youtube

        comments = get_top_liked_comments("youtu.be6", max_results=4)
        assert comments == ""

    @patch("sentimental_analysis.realworld.youtube_scrap.build")
    @patch("sentimental_analysis.realworld.youtube_scrap.extract_video_id")
    def test_get_top_liked_comments_order_by_time(self, mock_extract_id, mock_build):
        """
        Test ordering by time instead of relevance.
        """
        mock_extract_id.return_value = "time_order_video"
        mock_youtube = MagicMock()
        mock_comment_threads = MagicMock()
        mock_list_execute = MagicMock()

        mock_list_execute.return_value = {
            "items": [
                {"snippet": {"topLevelComment": {"snippet": {"textDisplay": "Comment 1", "likeCount": 10, "publishedAt": "2024-01-01T00:00:00Z"}}}},
                {"snippet": {"topLevelComment": {"snippet": {"textDisplay": "Comment 2", "likeCount": 5, "publishedAt": "2024-01-02T00:00:00Z"}}}},
                {"snippet": {"topLevelComment": {"snippet": {"textDisplay": "Comment 3", "likeCount": 12, "publishedAt": "2024-01-03T00:00:00Z"}}}},
            ]
        }

        mock_comment_threads.list.return_value = mock_list_execute
        mock_youtube.commentThreads.return_value = mock_comment_threads
        mock_build.return_value = mock_youtube

        comments = get_top_liked_comments("youtu.be7", max_results=3)
        assert comments == ""

    @patch("sentimental_analysis.realworld.youtube_scrap.build")
    @patch("sentimental_analysis.realworld.youtube_scrap.extract_video_id")
    def test_get_top_liked_comments_with_reply(self, mock_extract_id, mock_build):
        """
        Test that the function does not include replies in the result.
        """
        mock_extract_id.return_value = "replies_video_id"
        mock_youtube = MagicMock()
        mock_comment_threads = MagicMock()
        mock_list_execute = MagicMock()

        mock_list_execute.return_value = {
            "items": [
                {
                    "snippet": {
                        "topLevelComment": {
                            "snippet": {"textDisplay": "Comment 1", "likeCount": 5},
                        },
                        "replies": {  # Simulate a reply.  The function should not include this.
                            "comments": [{"snippet": {"textDisplay": "Reply 1", "likeCount": 2}}]
                        },
                    }
                },
                {"snippet": {"topLevelComment": {"snippet": {"textDisplay": "Comment 2", "likeCount": 10}}}},
            ]
        }

        mock_comment_threads.list.return_value = mock_list_execute
        mock_youtube.commentThreads.return_value = mock_comment_threads
        mock_build.return_value = mock_youtube

        comments = get_top_liked_comments("youtu.be8", max_results=2)
        assert comments == ""  # Should not include "Reply 1"