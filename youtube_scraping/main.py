# Para obtener un listado de la cantidad de veces que aparece cada palabra:
# python3 main.py --raw | tr -s " " "\n" | sort -k 1 | uniq -c | sort -k 1

import sys
from youtube_transcript_api import YouTubeTranscriptApi

video_id="lzxKZx7we4s"
transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['es'])

arguments_count = len(sys.argv)
is_raw = False
print(arguments_count)
if arguments_count == 2:
    is_raw = True


for transcript in transcript_list:
    if is_raw:
        print(transcript["text"])
    else:
        print(transcript)
