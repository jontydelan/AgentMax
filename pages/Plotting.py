import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Pro-Active Campaign", page_icon="📈")

if "campaign_live" not in st.session_state:
    st.session_state['campaign_live'] = False

def make_live():
    st.session_state['campaign_live']  = True

def load_progress(msg):
    step_output = None
    with st.spinner("Running "+msg):
        time.sleep(1)
        step_output = 10

    mt = st.expander(msg+" Executed !", icon=":material/thumb_up:",)
    with mt:
        if step_output:
            st.info(f"{msg} {step_output} Delays")
    progress_text = msg#"Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    # msg_op = st.empty()
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()
    st.text(msg+"Done..!")


def run_camp():
    load_progress('Analysing delays')
    load_progress('Identified 5 delayed Deliveries today')
    load_progress("Sending email and escalating")

st.button("Start Proacitve compaign..", on_click= make_live)

if st.session_state['campaign_live']:
    run_camp()

st.session_state['campaign_live'] = False
time.sleep(10)
st.button("Rerun")