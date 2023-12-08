"""
Server Root executed file, culmination of client side Wake Word,Speech Recognition, NLU, Speech Synthesis modules functionality
- Server url specified to be used to communicate to server side NLU functionality
- Instantiate the four modules prior to looping
- Loop the following execution to create continuous cycle of the following steps (making Azura run without stopping until turned off)
 - Call to wake detection to setup and continually listen for wake word, waiting for 1 (wake word detected) to be returned
 - Upon 1 returned (Wake word detected - "Hey Azura" called), execute the following steps:
  - Call speech recognition to listen and return textually transcribed user queries to transcribed_text
  - Pass transcribed_text as json to POST REST API request to server at app route '/classify-intent'
  - Response is returned from server consisting of classified intent, entities, labels derived from transcribed_text
  - Using ActionFactory's singleton instance, call to handle_intent method passing predicted query information returning the generated response made from intent's associated class
  - Pass generated response to the speech synthesizer, outputting the textual response as speech
"""

import requests
from WakeWord.wake_detector import WakeWordDetector
from SpeechRecognition.audio_transcribe import AudioTranscriber
from NLU.action_handler import ActionFactory
from SpeechSynthesis.speech_synthesizer import SpeechSynthesizer
server_url = 'http://192.168.1.115:5000'

wake_detect = WakeWordDetector()
transcriber = AudioTranscriber()
action_handler = ActionFactory.get_instance()
tts = SpeechSynthesizer()

while True:
	wake_detect.setup()
	print("Call wake word detection")
	result = wake_detect.listen_for_wake_word()

	if result == 1:
		wake_detect.cleanup()
		print("Call speech recognition")
		transcribed_text = transcriber.record_and_transcribe()
		print("Transcribed text: " + transcribed_text)

		print("Call NLU Classification models")
		response = requests.post(f'{server_url}/classify-intent', json={"text": transcribed_text})
		predicted_intent = response.json()['intent']
		entities = response.json()['entities']
		labels = response.json()['labels']

		print("Predicted Intent: ", predicted_intent)
		print("Entities: ", entities)
		print("Labels: ", labels)
		try:
			result = action_handler.handle_intent(predicted_intent, entities, labels)
		except:
			result = predicted_intent + " action not implemented yet"
		print(result)

		print("Call speech synthesis")
		tts.produce_audio_output(result)
