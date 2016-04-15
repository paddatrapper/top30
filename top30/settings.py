import yaml
import os.path

class settings:
    songs = {}
    voice = {}
    def __init__(self, conf_file):
        """
        Parses the configuration yaml file into a set of useable settings.
        """
        if conf_file == "":
            raise ConfigurationError("No configuration file provided")

        with open(conf_file, 'r') as settings_file:
            conf = yaml.load(settings_file)

        self.songs['length'] = conf['songs']['length']
        self.songs['startTag'] = conf['songs']['startTag']
        self.songs['directory'] = conf['songs']['directory']

        self.voice['directory'] = conf['voice']['directory']

    def getSongConf(self, key):
        return self.songs[key]

    def getVoiceConf(self, key):
        return self.voice[key]

class ConfigurationError(Exception):
    pass
