import azapi
import musicbrainzngs
# API.artist = 'Rick Astley'
# API.title = 'Never Gonna Give You Up'


# # API.getLyrics(save=True, ext='lrc')

# print(API.lyrics)

# # Correct Artist and Title are updated from webpage
# print(API.title, API.artist)


def getLyrics(artist, title):
    # Capitalize each word in artist and title
    API = azapi.AZlyrics('Duckduckgo', accuracy=0.5)
    newName = " ".join(word.capitalize() for word in artist.split())
    newTitle = " ".join(word.capitalize() for word in title.split())

    
    API.artist = newName
    API.title = newTitle
    # Do not write to disk in server environments
    API.getLyrics(save=False)

    lyrics = API.lyrics


    return newName, newTitle, lyrics


def verifyArtist(trackTitle):
    musicbrainzngs.set_useragent("PopSyn", "v0.0.1", "owner@jschere.com")
    


if __name__ == "__main__":
    print(getLyrics("Rick Astley", "never gonna give you up"))