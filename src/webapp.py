import streamlit as st
from speech_parser import parse_speech


def render_webapp():
    st.title("Emergency Call Logger")

    audio_file = st.file_uploader(label="Upload audio file", type=['wav', 'mp3', 'mp4'])

    transcript, names, locations, organizations, summary, urgency = parse_speech(audio_file)

    st.header("Extracted Information")
    st.subheader("Names")
    st.write(names)
    st.subheader("Locations")
    st.write(locations)
    st.write("Organizations")
    st.write(organizations)

    st.header("Urgency")
    if urgency['label'] == 'POSITIVE' or (urgency['label'] == 'NEGATIVE' and urgency['score'] < 0.55):
        st.write("Urgent")
    else:
        st.write("Critical")

    st.header("Summary of Transcript")
    st.write(summary)

    st.header("Transcript")
    st.write(transcript)

render_webapp()