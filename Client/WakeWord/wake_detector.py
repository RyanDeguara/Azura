"""
Wake Word Detector file:
Consists of WakeWordDetector class containing setup, listen, cleanup methods
"""

import struct
import pyaudio
import pvporcupine
import os

class WakeWordDetector:
    def __init__(self):
        """
        Initialize porcupine access key, relative path to porcupine model
        Set additional attributes initialized to None
        """
        self.porcupine = None
        self.audio_stream = None
        self.pa = None
        self.access_key = 'KcRmIypWkCCrWA80XJBkYGiwU2acunVw/QW6ZoMsp10cfZraUfhj/A=='
        self.keyword_path = os.path.join(os.path.dirname(__file__), "models/hey-azura_en_raspberry-pi_v3_0_0.ppn")

    def setup(self):
        """
        Loads porcupine model using path to model and access_key
        Load PyAudio to record from audio stream passing porcupine parameters to it
        Validation in case setup improperly
        """
        try:
            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keyword_paths=[self.keyword_path]
            )

            self.pa = pyaudio.PyAudio()

            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )

        except Exception as e:
            print("Error during setup")

    def listen_for_wake_word(self):
        """
        Validation done to check PyAudio audio stream or porcupine is properly initialized
        In a continuous loop, read frames of audio data from audio buffer
        Unpack audio data into tuples of integers
        Unpacked audio data (PCM) passed to be processed using porcupine, returns output to keyword_index - -1 if no wake word detected
        If returned output greater or equal to 0, return 1

        Returns:
        - 1 (integer): indicating wake word detected
        """

        if self.porcupine is None or self.audio_stream is None or self.pa is None:
            print("Not properly initialized. Call 'setup' first.")
            return

        try:
            while True:
                pcm = self.audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

                keyword_index = self.porcupine.process(pcm)

                if keyword_index >= 0:
                    return 1

        except KeyboardInterrupt:
            print("Interrupted")

    def cleanup(self):
        """
        Cleanup method to call to delete model, close audio stream and terminate PyAudio
        """
        if self.porcupine is not None:
            self.porcupine.delete()

        if self.audio_stream is not None:
            self.audio_stream.close()

        if self.pa is not None:
            self.pa.terminate()
