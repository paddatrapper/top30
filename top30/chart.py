###########################################################################
# Top30 is Copyright (C) 2016-2017 Kyle Robbertze <krobbertze@gmail.com>
#
# Top30 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# Top30 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Top30.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################
"""
Manages the Top30 chart and related functions
"""
from __future__ import unicode_literals

import docx2txt
from mutagen.oggvorbis import OggVorbis
import os
import youtube_dl

from top30.settings import Settings

class Chart:
    """
    A Top 30 chart is what is sent detailing the top 30 songs of the week.
    """
    def __init__(self, chart_file):
        self.songs = parse_docx(chart_file)
        for i in range(0, len(self.songs)):
            self.find_song(i)

    def get(self, position, attribute):
        """
        Returns a property from the spng at a position in the chart
        """
        return self.songs[position - 1][attribute]

    def find_song(self, position):
        """
        Finds a song in the download directory. If it is not found
        it attempts to download it.
        """
        song = self.songs[position]
        for filename in os.listdir(Settings.song_directory):
            if filename.endswith(song['artist'] + " - " + song['title'] + \
                                 ".ogg"):
                self.songs[position]['path'] = Settings.song_directory + \
                        "/" + filename
                return
        print(song['title'] + " by " + song['artist'] + " cannot be found")
        url = input("Enter the youtube URL of the song: ")
        download_song(url, song['artist'], song['title'])
        self.songs[position]['path'] = Settings.song_directory + "/" + \
                song['artist'] + " - " + song['title'] + ".ogg"
        start = input("Enter the start time (mm:ss):")
        set_start(self.songs[position]['path'], start)

def parse_docx(filename):
    """
    Parses a docx at filename
    """
    text = docx2txt.process(filename)
    chart_list = text.split("\n")
    chart_list = [i for i in chart_list if i != '' and i != ' '] # Ignore blank lines
    # Just the chart_list items
    chart_list = chart_list[chart_list.index('1'):chart_list.index('30') + 5]
    chart = []
    for i in range(0, len(chart_list), 5):
        chart.append({"artist": chart_list[i + 1], "title": chart_list[i + 2]})
    return chart

def download_song(url, artist, title):
    """
    Downloads a song at url and converts it into a useable format
    """
    ydl_opts = {
        'outtmpl': Settings.song_directory + "/" + artist + " - " + title + \
                  ".%(ext)s",
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'vorbis',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def set_start(filename, start_time):
    """
    Writes the start of the song section to file
    """
    song_meta = OggVorbis(filename)
    song_meta[Settings.song_start_tag] = start_time
    song_meta.save()
