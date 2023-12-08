"""
Speech Recognition file:
Consists of AudioTranscriber (STT - Speech-to-Text) class containing recording and transcriber method
"""

import pyaudio
import wave
import os
import whisper

class AudioTranscriber:
    def __init__(self, output_filename="output.wav"):
        """
        Initialize audio configurations, STT model

        Args:
        - output_filename (string): passed parameter to specify filename of recorded file, default set to output.wav

        Initialize audio configurations including chunk samples, format of 16 bits per sample, 2 audio channels, 44100 samples per second, 6 seconds record window time
        Set relative path to speech output file
        Load whispers 'base' model for STT
        """
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 2
        self.fs = 44100
        self.seconds = 6
        self.output_filename = os.path.join(os.path.dirname(__file__), output_filename)
        self.model = whisper.load_model("base")

    def record_and_transcribe(self):
        """
        Records speech data, passes recorded audio for transcription using STT model

        Execution:
        - Initializes PyAudio
        - Opens stream for recording
        - Records audio frames using loop up to specified seconds, appending audio frames to frames list
        - Stops and closes recording stream
        - Saves recorded audio to WAV file
        - Transcribes the recorded audio into text using Whisper's STT model 'transcribe' method

        Returns:
        - result['text'] (string): transcribed text from speech data
        """

        p = pyaudio.PyAudio()
        frames = []

        print('Recording')

        stream = p.open(format=self.sample_format,
                        channels=self.channels,
                        rate=self.fs,
                        frames_per_buffer=self.chunk,
                        input=True)

        for i in range(0, int(self.fs / self.chunk * self.seconds)):
            data = stream.read(self.chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        print('Finished recording')

        wf = wave.open(self.output_filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        result = self.model.transcribe(self.output_filename)

        return result["text"]
