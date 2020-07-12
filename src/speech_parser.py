import speech_recognition as sr
from transformers import pipeline


def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as audio_source:
        audio = recognizer.listen(audio_source)
        transcript = recognizer.recognize_google(audio)
        return transcript


def extract_information(transcript):
    name_location_organization_extractor = pipeline('ner')
    names_locations_organizations = name_location_organization_extractor(transcript)
    name_list = []
    location_list = []
    organization_list = []
    for entry in names_locations_organizations:
        if entry['score'] >= 0.9:
            if entry['name'] == 'B-PER' or entry['name'] == 'I-PER':
                name_list.append(entry['word'])
            elif entry['entity'] == 'B-LOC' or entry['entity'] == 'I-LOC':
                location_list.append(entry['word'])
            elif entry['entity'] == 'B-ORG' or entry['entity'] == 'I-ORG':
                organization_list.append(entry['word'])

    names = ""
    for name in name_list:
        names += name + ", "
    names = names[0:-2]

    locations = ""
    for location in location_list:
        locations += location + ", "
    locations = locations[0:-2]

    organizations = ""
    for organization in organization_list:
        names += organization + ", "
    organizations = organizations[0:-2]

    summary_extractor = pipeline('summarization')
    summary = summary_extractor(transcript, max_length=100)

    urgency_extractor = pipeline('sentiment-analysis')
    urgency = urgency_extractor(transcript)[0]
    if urgency['label'] == 'POSITIVE' or (urgency['label'] == 'NEGATIVE' and urgency['score'] < 0.55):
        urgency = 'Urgent'
    else:
        urgency = 'Critically Urgent'

    return names, locations, organizations, summary, urgency


def parse_speech(audio_file):
    try:
        transcript = speech_to_text(audio_file)
        names, locations, organizations, summary, urgency = extract_information(transcript)
        return transcript, names, locations, organizations, summary, urgency
    except sr.RequestError:
        return 'RequestError', None, None, None, None, None
    except sr.UnknownValueError:
        return 'UnknownValueError', None, None, None, None, None
    except ValueError:
        return 'ValueError', None, None, None, None, None
    except:
        return 'UnknownError', None, None, None, None, None
