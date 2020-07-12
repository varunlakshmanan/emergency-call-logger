import speech_recognition as sr
from transformers import pipeline


def speech_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as audio_source:
        audio = recognizer.listen(audio_source)
        try:
            transcript = recognizer.recognize_google(audio)
            return transcript
        except:
            return "Google Web Speech API not accessible"


def extract_information(transcript):
    name_location_organization_extractor = pipeline("ner")
    names_locations_organizations = name_location_organization_extractor(transcript)
    names = []
    locations = []
    organizations = []
    for entry in names_locations_organizations:
        if entry['score'] >= 0.9:
            if entry['name'] == 'B-PER' or entry['name'] == 'I-PER':
                names.append(entry['word'])
            elif entry['entity'] == 'B-LOC' or entry['entity'] == 'I-LOC':
                locations.append(entry['word'])
            elif entry['entity'] == 'B-ORG' or entry['entity'] == 'I-ORG':
                organizations.append(entry['word'])

    summary_extractor = pipeline("summarization")
    summary = summary_extractor(transcript, max_length=100)

    urgency_extractor = pipeline("sentiment-analysis")
    urgency = urgency_extractor(transcript)[0]

    return names, locations, organizations, summary, urgency
