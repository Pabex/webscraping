from youtube_transcript_api import YouTubeTranscriptApi

video_id="lzxKZx7we4s"
transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['es'])

for transcript in transcript_list:
    print(transcript)
