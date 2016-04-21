import yaml
import os.path

class Settings:
    songs = {}
    voice = {}
    def __init__(self, conf_file):
        if conf_file == "":
            raise ConfigurationError("No configuration file provided")

        with open(conf_file, 'r') as settings_file:
            conf = yaml.load(settings_file)

        self.songs['length'] = conf['songs']['length']
        self.songs['startTag'] = conf['songs']['startTag']
        self.songs['directory'] = conf['songs']['directory']

        self.voice['beginOverlap'] = conf['voice']['beginningOverlap']
        self.voice['endOverlap'] = conf['voice']['endOverlap']
        self.voice['directory'] = conf['voice']['directory']

    def get_song_conf(self, key):
        return self.songs[key]

    def get_voice_conf(self, key):
        return self.voice[key]

class ConfigurationError(Exception):
    pass
