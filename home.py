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

# data = helper.get_delivery_refund_data(2)['data']


st.set_page_config(page_title="Pro-Active Campaign Agent", page_icon="📈")


if "campaign_live" not in st.session_state:
    st.session_state['campaign_live'] = False
    st.session_state['summary'] = False

if "Agent_live" not in st.session_state:
    st.session_state['Agent_live'] = False
    st.session_state['Agent'] = None

def make_live():
    st.session_state['campaign_live']  = True
    st.session_state['run_eval'] = False

if st.session_state['Agent_live'] == False:
    try:
        st.session_state['Agent'] = True
        st.session_state['Agent_live'] = True
    except:
        st.session_state['Agent_live'] = False

with st.container():
    col1, col2, col3 = st.columns([3, 3, 2])  # Adjust spacing to push right
    with col3:
        if st.session_state.Agent_live:
            st.text("🟢 Agent Live")
        else:
            st.text("🔴 Agent Offline")

# st.markdown("---")

st.header("Autonomous Customer Satisfaction Campaigns 📈 ")
st.text(datetime.date.today().strftime("%d-%b-%Y"))
st.markdown("---")

# ---------------Run campaing -----------------

st.button("Run Agent",icon="⚙️", on_click=make_live)

if st.session_state['campaign_live']:
    with st.container():
        st.text("Using groq API")
        agent = Proactive_Cx_agent.get_agent()
        eval_text = st.empty()
        with st.spinner("Loading Customer data.."):
            df =  helper.get_delivery_refund_data(20)['data']
            df_eval = agent_lib.get_issue_info(df)
            st.session_state['eval'] = df_eval
            

            time.sleep(1)
            # Display in a text block
            eval_text.text(
                f"📍 Refund Delays Identified: {df_eval['refund_issue']}\n"
                f"📦 Delivery Delays Identified: {df_eval['delivery_issue']}"
            )

        results = []
        for _, row in df.iterrows():
            payload = row.to_dict()
            spin_msg = f""" {payload['custID']} ( {payload['first_name']} {payload['last_name'] })"""
            with st.spinner("Agent working on custoer :"+spin_msg):
                time.sleep(1)
                state = {
                    "message": "Check order status",
                    "payload": payload
                }
                final_state = agent.invoke(state)
                results.append(final_state)

                if final_state:
                    # refund_delay_email
                    # delivery_delay_email
                    message = f"""Agent resolving {('Refund delay' if final_state['res']['refund_esc'] else '')} {('&' if final_state['res']['refund_esc'] and final_state['res']['delivery_esc'] else '')} {("Delivery delay" if final_state['res']['delivery_esc'] else '' )} for {spin_msg}"""
                    if final_state['res']['refund_esc'] or final_state['res']['delivery_esc']:
                        with st.expander(message):
                            emails = f"""{(final_state['res']['refund_delay_email'] if final_state['res']['refund_esc'] else '')} 
                            \n{(final_state['res']['delivery_delay_email'] if final_state['res']['delivery_esc'] else '' )}"""
                            st.text(emails)
                else:
                    st.text("No Delay ")
        st.session_state['summary'] = True
        



# ---------Campaign Evaluation ------------

if 'run_eval' not in st.session_state:
    st.session_state['run_eval'] = False

def run_eval():
    st.session_state['campaign_live'] = False
    st.session_state['run_eval'] = True
    # st.switch_page("./pages/Summary.py")

# summary = st.empty()
if st.session_state['summary']:
    st.button("View summary" ,on_click= run_eval)

if st.session_state['run_eval']:
    with st.container(border = True):
        st.subheader("Summary")
        st.markdown("---")

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
