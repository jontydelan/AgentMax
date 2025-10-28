import importlib, sys
import streamlit as st
import time
import numpy as np
sys.path.append("./Experiment")
import helper
import Proactive_Cx_agent ,agent_lib
import datetime
importlib.reload(helper)
importlib.reload(Proactive_Cx_agent)
importlib.reload(agent_lib)

st.header("Campaigns Summary ")
st.text(datetime.date.today().strftime("%d-%b-%Y"))
st.markdown("---")

data = helper.get_delivery_refund_data(20)['data']

df_eval = agent_lib.get_issue_info(data)
st.session_state['eval'] = df_eval

with st.spinner("Identifying delays.."):
    time.sleep(2)

with st.container():
    st.subheader("📦 Delivery Perocess performance today ", divider="blue")
    colA, colB = st.columns(2)
    with colA:
        st.metric(label="Delayed Deliveries", value=st.session_state['eval']['delivery_issue'], delta="-3 from yesterday")
    with colB:
        st.metric(label="Escalated Deliveries", value=st.session_state['eval']['delivery_issue'])

    st.subheader("💵 Refund Perocess performance today ", divider="blue")
    colA, colB = st.columns(2)
    with colA:
        st.metric(label="Refund Delays", value=st.session_state['eval']['refund_issue'], delta="+2 from yesterday")
    with colB:
        st.metric(label="Escalated Refunds", value=st.session_state['eval']['refund_issue'])
