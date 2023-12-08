"""
Speech Synthesis file:
Consists of SpeechSynthesizer (TTS - Text-to-Speech) class containing simple process audio output method
"""

import os
from playsound import playsound
from gtts import gTTS

class SpeechSynthesizer:
	def __init__(self):
		"""
		Initialize relative path
		"""

		self.path = os.path.join(os.path.dirname(__file__), "\\")

	def produce_audio_output(self,sentence):
		"""
		Process audio output method to turn passed text into audio form

		Args:
		- sentence (string): Sentence passed to output text into speech

		Execution:
		- Sentence is passed to gTTS (Google Text-to-Speech), passing language 'en' - English and passing accent 'ie' - Irish
		- An English (Irish accent) speech output is saved as mp3 file and played to the user
		"""

		tts = gTTS(sentence, lang='en', tld='ie')
		tts.save(self.path + 'output.mp3')
		playsound(self.path + 'output.mp3')
