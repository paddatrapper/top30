#!/usr/bin/env python3
from pydub import AudioSegment

silence = AudioSegment.silent(duration=20*1000)
silence.export("silence.ogg", format="ogg", tags={"DESCRIPTION": "00:08"})
