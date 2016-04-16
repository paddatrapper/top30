from mutagen.oggvorbis import OggVorbis
from pydub import AudioSegment
from top30 import settings

class top30Creator:
    config = settings.settings("config.yaml")

    def getStartTime(self, song_meta):
        
        time_code_start = song_meta.find("DESCRIPTION=") + 12
        time_code = song_meta[time_code_start:time_code_start + 5]
        song_length = int(time_code.split(':')[0]) * 60 + int(time_code.split(':')[1])
        song_length *= 1000
        return song_length
        
    def run(self):
        print("Creating rundown 30-21") 
        #self.createRundown(30, 21)
        print("Creating rundown 20-11") 
        #self.createRundown(20, 11)
        print("Creating rundown 10-02") 
        self.createRundown(10, 2)

    def createRundown(self, start, end):
        voice_beginning_overlap = 200
        voice_end_overlap = 1500
        song_length = int(self.config.getSongConf('length')) * 1000

        song_dir = self.config.getSongConf('directory')
        voice_dir = self.config.getVoiceConf('directory')

        intro = "%s/%02d-%02d_intro.ogg" % (voice_dir, start, end)
        rundown = AudioSegment.from_ogg(intro)[:-voice_end_overlap]

        song_file = song_dir + "/" + str(start) + ".ogg"
        song_meta = OggVorbis(song_file)
        start_time = self.getStartTime(song_meta.pprint())

        song = AudioSegment.from_ogg(song_file)
        song = song.overlay(rundown[-voice_end_overlap:])
        rundown = rundown.append(song[start_time:start_time + song_length], crossfade=0)

        for i in range(start - 1, end - 1, -1):
            voice_file = voice_dir + "/" + str(i) + ".ogg"
            voice = AudioSegment.from_ogg(voice_file)
            rundown = rundown.overlay(voice[:voice_beginning_overlap])
            rundown = rundown.append(voice[voice_beginning_overlap:-voice_end_overlap], crossfade=200)

            song_file = song_dir + "/" + str(i) + ".ogg"
            song_meta = OggVorbis(song_file)
            start_time = self.getStartTime(song_meta.pprint())
            song = AudioSegment.from_ogg(song_file)
            song = song.overlay(voice[-voice_end_overlap:])
            rundown = rundown.append(song[start_time:start_time + song_length], crossfade=0)

        outro = "%s/%02d-%02d_outro.ogg" % (voice_dir, start, end)
        outro = AudioSegment.from_ogg(outro)
        rundown = rundown.append(outro, crossfade=0)
        rundown_name = "rundown-%02d-%02d.mp3" % (start, end)
        rundown.export(rundown_name, format="mp3")
        print("Exported", rundown_name) 
