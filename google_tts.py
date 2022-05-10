import os
import google.cloud.texttospeech_v1beta1 as tts

from kaleb_mistyPy import Robot

class MistyGoogleTTS:
    def __init__(self, robot):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/kaleb/Desktop/google-auth.json'

        self.language = 'en-US'
        self.voice = 'en-US-Standard-C'

        self.voice_params = tts.VoiceSelectionParams(
            language_code=self.language,
            name=self.voice
        )

        self.audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)
        self.client = tts.TextToSpeechClient()
        self.robot = robot

    def tts_callback(self, msg):
        text_input = tts.SynthesisInput(text=msg)
        response = self.client.synthesize_speech(input=text_input, voice=self.voice_params, audio_config=self.audio_config)
        with open("tts.mp3", "wb") as out:
            out.write(response.audio_content)
        
        # send to Misty
        self.robot.uploadAudio("tts.mp3", apply=True, overwrite=True)

# if __name__ == "__main__":
#     node = MistyGoogleTTS()