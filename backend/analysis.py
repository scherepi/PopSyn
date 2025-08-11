import azapi
import musicbrainzngs
from nrclex import NRCLex
import threading


# Uses the NRCLex package to determine the emotions in a given lyrical sample, which is then returned in a big data object for your processing pleasure.
def getAnalysis(lyricString: str):
    lyricString = lyricString.replace("\n", ' ')
    emotionalAnalysis = NRCLex(lyricString)
    return {
        "dominantEmotion": emotionalAnalysis.top_emotions[0][0],
        "emotionList": emotionalAnalysis.raw_emotion_scores
    }