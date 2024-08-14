from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

###############################################################################
def getTranscript(video_id):
    try:
        # Retrieve the transcript
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id,cookies="youtube_cookies.txt")
        transcript = transcript_list.find_transcript(['en'])
        
        # Convert the transcript to plain text
        formatter = TextFormatter()
        plain_text = formatter.format_transcript(transcript.fetch(),cookies="youtube_cookies.txt")
        
        return plain_text
    except Exception as e:
        print(f"Error retrieving transcript: {e}")
        return None
    
###############################################################################