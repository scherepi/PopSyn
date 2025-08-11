import azapi
import musicbrainzngs
from nrclex import NRCLex


# Uses the NRCLex package to determine the emotions in a given lyrical sample, which is then returned in a big data object for your processing pleasure.
def getColor(lyricString: str):
    lyricString = lyricString.replace("\n", ' ')
    emotionalAnalysis = NRCLex(lyricString)
    