import sys
import argparse
import requests
from bs4 import BeautifulSoup
from os.path import exists
from six.moves.html_parser import HTMLParser
import urllib.parse
import glob  
import numpy as np

parser = argparse.ArgumentParser(description=__doc__, epilog = 'xyz')

parser.add_argument("artist", help="Please enter the name of the artist you wanna scrape.")
parser.add_argument("directory", help="Please enter the name of the directory for storing the lyrics.")
args = parser.parse_args()
artist = args.artist
directory = args.directory
#print(artist, directory)

### function for "getting" song links from lyrics.com by artist name
def get_song_links(artist):
    artist = artist.replace(' ', '+')
    lyrics = 'https://www.lyrics.com'
    artists = 'https://www.lyrics.com/artist/'
    data = requests.get((artists + artist))
    soup = BeautifulSoup(data.text, 'html.parser')
    songs_list = []

    for tag in soup.findAll('a', href=True):
        if '/lyric/' in tag['href']:
            link = lyrics + tag['href']
            songs_list.append(link)
    return songs_list

### function for checking if song file (including versions) already exists
def song_file_exists(song_link, directory):
    string = (song_link[song_link.rfind('/')+1:]).replace('+', ' ')
    name = urllib.parse.unquote(string)
    content = glob.glob(directory + '*' + name[:name.find(' [')] + '*') #exclude [version] versions like mono, stereo, remastered etc.
    if content:
        length = len(content[0])
    else:
        length = 0
    if length > 0:
        return True
    else:
        return False

# scrape and store lyrics for the given song list and directory
def scrape_and_store_lyrics(songs_list, directory):
    for song_link in songs_list.copy():
        if not song_file_exists(song_link, directory):
            try: 
                data_2 = requests.get(song_link, timeout=20) 
                soup_2 = BeautifulSoup(data_2.text, 'html.parser')
                shorter = (song_link[:song_link.rfind('/')])#.replace('+', ' ')
                artist = shorter[shorter.rfind('/')+1:]
                lyric_title = artist + ' ' + (soup_2.find(id='lyric-title-text').get_text()) + '.txt'
                try:
                    lyric_text = soup_2.find(id='lyric-body-text').get_text()
                    lyric_text.replace('\n\n', '\n')
                    lyric_text = lyric_text.replace('\r', '')
                    file = open(directory + lyric_title, "w")
                    file.write(lyric_text)
                    file.close()
                    print('successfully scraped ' + lyric_title)
                except:
                    print('could not extract any lyrics for ' + song_link)
            except:
                print('some went wrong with scraping ' + song_link)
                #songs_list.append(song_link)        
        else:
            print('successfully rejected version copy')
        print('\n')

### call functions to run the scraping:

songs_list = get_song_links(artist)

scrape_and_store_lyrics(songs_list, directory)