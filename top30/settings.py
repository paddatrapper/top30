import yaml
import os.path

class Settings:
    def __init__(self):
        self.SONG_LENGTH = 10 * 1000
        self.SONG_START_TAG = "description"
        self.SONG_DIRECTORY = "../songs"

        self.VOICE_START_OVERLAP = 300
        self.VOICE_END_OVERLAP = 1400
        self.VOICE_DIRECTORY = "../voice"

        self.DEBUG = False

class ConfigurationError(Exception):
    pass
