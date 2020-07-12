import streamlit as st
from speech_parser import parse_speech
import pandas as pd


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
        st.header("Extracted Information")
        info_table = {'Names': [names],
                      'Locations': [locations],
                      'Organizations': [organizations],
                      'Urgency': [urgency]}
        st.dataframe(pd.DataFrame.from_dict(info_table))

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
