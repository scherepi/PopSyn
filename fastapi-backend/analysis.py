import azapi
import musicbrainzngs
from nrclex import NRCLex
from color import emotions_to_color, rgb_to_hex


# Uses the NRCLex package to determine the emotions in a given lyrical sample, which is then returned in a big data object for your processing pleasure.
def getColor(lyricString: str):
    lyricString = lyricString.replace("\n", ' ')
    emotionalAnalysis = NRCLex(lyricString)
    color_hex = rgb_to_hex(emotions_to_color(emotionalAnalysis.raw_emotion_scores))
    return color_hex