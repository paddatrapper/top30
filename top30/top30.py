import settings
import os

class top30:
    def __init__(self, conf_file):
        config = settings(conf_file)
        
    def run(self):
        song_list = os.listdir(settings.getSongConf('directory'))
        voice_list = os.listdir(settings.getVoiceConf('directory'))

        intro_tag = settings.getVoiceConf('introTag')
        outro_tag = settings.getVoiceConf('outroTag')

        song_length = int(settings.getSongConf('length')
