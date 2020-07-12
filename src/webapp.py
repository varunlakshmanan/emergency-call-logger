import streamlit as st
from speech_parser import parse_speech


def on_button_press(audio_file):
    transcript, names, locations, organizations, summary, urgency = parse_speech(audio_file)
    if summary is None:
        if transcript == 'RequestError':
            st.error('Web Speech API couldn\'t be reached at this time. Please try again at a later time.')
        elif transcript == 'UnknownValueError':
            st.error('Your speech couldn\'t be recognized. Please try speaking more clearly.')
        elif transcript == 'ValueError':
            st.error("File format error. Ensure that your WAV file is encoded in the PCM format.")
        else:
            st.error("Unknown error. Please try again later and ensure that your WAV file is encoded in the PCM format.")
    else:
        st.header('Extracted Information')
        st.subheader('Names')
        st.write(names)
        st.subheader('Locations')
        st.write(locations)
        st.subheader('Organizations')
        st.write(organizations)

        st.header('Urgency')
        if urgency['label'] == 'POSITIVE' or (urgency['label'] == 'NEGATIVE' and urgency['score'] < 0.55):
            st.write('Urgent')
        else:
            st.write('Critical')

        st.header('Summary of Transcript')
        st.write(summary)

        st.header('Transcript')
        st.write(transcript)


def render_webapp():
    st.title('Emergency Call Logger')

    audio_file = st.file_uploader(label='Upload audio file', type=['wav'])
    if st.button('Upload file'):
        on_button_press(audio_file)


render_webapp()
