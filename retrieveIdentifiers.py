import csv
import struct
import urllib.parse, urllib.request
import json


def retrieve_itunes_identifier(title, artist):
    headers = {
        "X-Apple-Store-Front" : "143446-10,32 ab:rSwnYxS0 t:music2",
        "X-Apple-Tz" : "7200" 
    }
    url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/search?clientApplication=MusicPlayer&term=" + urllib.parse.quote(title)
    request = urllib.request.Request(url, None, headers)

    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        songs = [result for result in data["storePlatformData"]["lockup"]["results"].values() if result["kind"] == "song"]
        
        # Attempt to match by title & artist
        for song in songs: 
            if song["name"].lower() == title.lower() and (song["artistName"].lower() in artist.lower() or artist.lower() in song["artistName"].lower()):
                return song["id"]
        
        # Attempt to match by title if we didn't get a title & artist match
        for song in songs: 
            if song["name"].lower() == title.lower():
                return song["id"]

    except:
        # We don't do any fancy error handling.. Just return None if something went wrong
        return None


itunes_identifiers = []


with open('spotify.csv', encoding='utf-8') as playlist_file:
    playlist_reader = csv.reader(playlist_file)
    next(playlist_reader)

    for row in playlist_reader:
        title, artist = row[1], row[2]
        itunes_identifier = retrieve_itunes_identifier(title, artist)

        if itunes_identifier:
            itunes_identifiers.append(itunes_identifier)
            print("{} - {} => {}".format(title, artist, itunes_identifier))
        else:
            print("{} - {} => Not Found".format(title, artist))
            noresult = "{} - {} => Not Found".format(title, artist)
            with open('noresult.txt', 'a+') as f:
                f.write(noresult)
                f.write('\n')


with open('itunes.csv', 'w', encoding='utf-8') as output_file:
    for itunes_identifier in itunes_identifiers:
        output_file.write(str(itunes_identifier) + "\n")


# Developped by @therealmarius on GitHub
# Based on the work of @simonschellaert on GitHub
# Github project page: https://github.com/therealmarius/Spotify-2-AppleMusic