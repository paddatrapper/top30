from lib.settings import Settings

from mutagen.oggvorbis import OggVorbis
from pydub import AudioSegment

class Top30Creator:
    config = Settings("config.yaml")

    def get_start_time(self, song_meta):
        tag = self.config.get_song_conf('startTag') 
        time_code_start = song_meta.find(tag + "=") + len(tag) + 1
        time_code = song_meta[time_code_start:]
        song_length = float(time_code.split(':')[0]) * 60 + float(time_code.split(':')[1])
        song_length *= 1000
        return song_length
        
    def create_rundown(self, start, end, directory):
        print("Creating rundown ", directory, start, "-", end, sep="") 
        self.voice_beginning_overlap = int(self.config.get_voice_conf('beginOverlap'))
        self.voice_end_overlap = int(self.config.get_voice_conf('endOverlap'))
        self.song_length = int(self.config.get_song_conf('length')) * 1000

        song_dir = self.config.get_song_conf('directory')
        voice_dir = self.config.get_voice_conf('directory')
        if not directory == "":
            song_dir += "/" + directory
            directory += "_"

        intro = "%s/%s%02d-%02d_intro.ogg" % (voice_dir, directory, start, end)
        rundown = AudioSegment.from_ogg(intro)[:-self.voice_end_overlap]

        song_file = song_dir + "/" + str(start) + ".ogg"
        rundown = self.add_song(song_file, rundown)


        for i in range(start - 1, end - 1, -1):
            voice_file = voice_dir + "/" + str(i) + ".ogg"
            rundown = self.add_voice(voice_file, rundown)

            song_file = song_dir + "/" + str(i) + ".ogg"
            rundown = self.add_song(song_file, rundown)

        outro = "%s/%s%02d-%02d_outro.ogg" % (voice_dir, directory, start, end)
        outro = AudioSegment.from_ogg(outro)
        rundown = rundown.append(outro, crossfade=0)
        rundown_name = "rundown-%s%02d-%02d.mp3" % (directory, start, end)
        rundown.export(rundown_name, format="mp3")
        print("Exported", rundown_name) 

    def add_voice(self, voice_file, rundown):
        voice = AudioSegment.from_ogg(voice_file)
        rundown = rundown.overlay(voice[:self.voice_beginning_overlap], 
                position=-self.voice_beginning_overlap)
        return rundown.append(voice[self.voice_beginning_overlap:-self.voice_end_overlap], 
                crossfade=0)

    def add_song(self, song_file, rundown):
        song_meta = OggVorbis(song_file)
        start_time = self.get_start_time(song_meta.pprint())

        song = AudioSegment.from_ogg(song_file)
        song = song.overlay(rundown[-self.voice_end_overlap:])
        return rundown.append(song[start_time:start_time + self.song_length],
                crossfade=0)

    def run(self):
        self.create_rundown(30, 21, "")

