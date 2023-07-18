from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
# from IPython.display import YouTubeVideo


def youtube_summary(link):
    video_id = link.split("=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    result = ""
    for i in transcript:
        result += " " + i["text"]
    return result

summarizer = pipeline("summarization")
# print(youtube_summary("https://www.youtube.com/watch?v=zW_kG_NORYo"))
