from pydub import AudioSegment
from top30 import settings

class top30Creator:
    config = settings.settings("config.yaml")
        
    def run(self):
        voice_beginning_overlap = 400
        voice_end_overlap = 1500
        song_dir = self.config.getSongConf('directory')
        voice_dir = self.config.getVoiceConf('directory')

        length = int(self.config.getSongConf('length')) * 1000

        intro = voice_dir + "/30-21_intro.ogg"
        rundown = AudioSegment.from_ogg(intro)[:-voice_end_overlap]

        song = AudioSegment.from_ogg(song_dir + "/30.ogg")
        song = song.overlay(rundown[-voice_end_overlap:])
        rundown = rundown.append(song[len(song)//2:len(song)//2 + length], crossfade=0)

        for i in range(29, 20, -1):
            voice = voice_dir + "/" + str(i) + ".ogg"
            voice = AudioSegment.from_ogg(voice)
            rundown = rundown.overlay(voice[:voice_beginning_overlap])
            rundown = rundown.append(voice[voice_beginning_overlap:-voice_end_overlap], crossfade=0)

            song = song_dir + "/" + str(i) + ".ogg"
            song = AudioSegment.from_ogg(song)
            song = song.overlay(voice[-voice_end_overlap:])
            rundown = rundown.append(song[len(song)//2:len(song)//2 + length], crossfade=0)

        outro = voice_dir + "/30-21_outro.ogg"
        outro = AudioSegment.from_ogg(outro)
        rundown = rundown.append(outro, crossfade=0)
        rundown.export("rundown-30-21.mp3", format="mp3")
