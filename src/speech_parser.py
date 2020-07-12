import speech_recognition as sr


def speech_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as audio_source:
        audio = recognizer.listen(audio_source)
        try:
            transcript = recognizer.recognize_google(audio)
            return transcript
        except:
            return "Google Web Speech API not accessible"
