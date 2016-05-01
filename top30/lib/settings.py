import yaml
import os.path

class Settings:
    def __init__(self, conf_file):
        if conf_file == "":
            raise ConfigurationError("No configuration file provided")

        with open(conf_file, 'r') as settings_file:
            conf = yaml.load(settings_file)

        self.SONG_LENGTH = int(conf['songs']['length']) * 1000
        self.SONG_START_TAG = conf['songs']['startTag']
        self.SONG_DIRECTORY = conf['songs']['directory']

        self.VOICE_START_OVERLAP = int(conf['voice']['beginningOverlap'])
        self.VOICE_END_OVERLAP = int(conf['voice']['endOverlap'])
        self.VOICE_DIRECTORY = conf['voice']['directory']

        self.DEBUG = False

class ConfigurationError(Exception):
    pass
