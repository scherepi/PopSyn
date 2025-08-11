import azapi
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
    API.getLyrics(save=True, ext='lrc')

    lyrics = API.lyrics


    return newName, newTitle, lyrics





print(getLyrics("Rick Astley", "never gonna give you up"))