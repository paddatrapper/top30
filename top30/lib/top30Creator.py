from lib.settings import Settings

from mutagen.oggvorbis import OggVorbis
from pydub import AudioSegment

class Top30Creator:
    def __init__(self, config_file):
        self.config = Settings(config_file)
        self.voice_begin_overlap = int(self.config.get_voice_conf('beginOverlap'))
        self.voice_end_overlap = int(self.config.get_voice_conf('endOverlap'))
        self.song_length = int(self.config.get_song_conf('length')) * 1000
        
    def create_rundown(self, start, end, directory):
        song_dir = self.config.get_song_conf('directory')
        voice_dir = self.config.get_voice_conf('directory')
        if directory:
            song_dir += "/" + directory
            directory += "_"

        intro = "%s/%s%02d-%02d_intro.ogg" % (voice_dir, directory, start, end)
        rundown = self.get_start(intro)
        song_file = song_dir + "/" + str(start) + ".ogg"
        rundown = self.add_song(song_file, rundown)

        for i in range(start - 1, end - 1, -1):
            voice_file = voice_dir + "/" + str(i) + ".ogg"
            rundown = self.add_voice(voice_file, rundown)
            song_file = song_dir + "/" + str(i) + ".ogg"
            rundown = self.add_song(song_file, rundown)

        outro = "%s/%s%02d-%02d_outro.ogg" % (voice_dir, directory, start, end)
        rundown = self.add_end(outro, rundown)
        rundown_name = "rundown-%s%02d-%02d" % (directory, start, end)
        self.export(rundown_name, "mp3", rundown)

    def get_start(self, filename):
        return AudioSegment.from_ogg(filename)[:-self.voice_end_overlap]

    def add_voice(self, voice_file, rundown):
        voice = AudioSegment.from_ogg(voice_file)
        rundown = rundown.overlay(voice[:self.voice_begin_overlap], 
                position=-self.voice_begin_overlap)
        return rundown.append(voice[self.voice_begin_overlap:-self.voice_end_overlap], 
                crossfade=0)

    def add_song(self, song_file, rundown):
        start_time = self.get_start_time(song_file)

        song = AudioSegment.from_ogg(song_file)
        song = song.overlay(rundown[-self.voice_end_overlap:])
        return rundown.append(song[start_time:start_time + self.song_length],
                crossfade=0)

    def add_end(self, filename, rundown):
        outro = AudioSegment.from_ogg(filename)
        return rundown.append(outro, crossfade=0)

    def export(self, filename, file_type, rundown):
        if filename.endswith(file_type):
            rundown.export(filename, format=file_type)
        else:
            rundown.export(filename + "." + file_type, format=file_type)

    def get_start_time(self, filename):
        song_meta = OggVorbis(filename).pprint()
        tag = self.config.get_song_conf('startTag') 
        time_code_start = song_meta.find(tag + "=") + len(tag) + 1
        time_code = song_meta[time_code_start:]
        song_length = float(time_code.split(':')[0]) * 60 + float(time_code.split(':')[1])
        song_length *= 1000
        return song_length

    def get_song_length(self):
        return self.song_length

    def get_voice_begin_overlap(self):
        return self.voice_begin_overlap

    def get_voice_end_overlap(self):
        return self.voice_end_overlap

    def set_song_length(self, song_length):
        self.song_length = song_length

    def set_voice_begin_overlap(self, voice_begin_overlap):
        self.voice_begin_overlap = voice_begin_overlap

    def set_voice_end_overlap(self, voice_end_overlap):
        self.voice_end_overlap = voice_end_overlap

    def run(self):
        self.create_rundown(30, 21, "")

