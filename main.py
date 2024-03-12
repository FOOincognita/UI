import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from streamlit_extras.dataframe_explorer import dataframe_explorer as dfExplorer
from streamlit_option_menu import option_menu

import os
import pandas as pd
import time
import toml
import numpy as np

#!! PUBLIC persistent storage; accessible by multiple employees
# Define the layout of the app, including the sidebar and main pages

# [TODO]: 
#    1. Implement subtabs for analysis (bubbles)
#    2. Add dataframe & prepare table input/output for easy back-end connection
#    3. Brainstrom what kinds of financial & consumer data we'd like to display, & using which graph(s)
#        - Find sources for this info
#    4. Implement settings
#

# App title
st.set_page_config(
    page_title="NX1 Chat", 
    layout="wide",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

def main() -> None:
    with st.sidebar:
        tab = option_menu(
            default_index = 0,
            menu_title    = "Neuro-X1",
            menu_icon     = "capsule", # "prescription"; "prescription2"
            options       = ["Chat", "Output", "Analysis", "Settings"] ,
            icons         = ["robot", "database", "kanban", "gear"],
        )
    
    match tab:
        case 'Chat':
            chat()
        case 'Output':
            output()
        case 'Analysis':
            analysis()
        case 'Settings':
            settings()
        case _:
            raise Exception


# --------------- TEXT STREAM GENERATOR --------------- #
def stream_data(text: str):
    for word in text.split(" "):
        yield f"{word} "
        time.sleep(0.02)

    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )

    for word in text.split(" "):
        yield f"{word} "
        time.sleep(0.02)


# --------------- CHATBOT --------------- #
# Function for generating LLM response
def generate_response(prompt_input: str, email: str, passwd: str) -> hugchat.Message:
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot                        
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)

# Define what will be displayed on each page
def chat() -> None:
    #* Hugging Face Credentials
    with st.sidebar:
        st.title('💬 ChatBot')
        if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
            st.success('HuggingFace Login credentials already provided!', icon='✅')
            hf_email = st.secrets['EMAIL']
            hf_pass  = st.secrets['PASS']
        else:
            hf_email = st.text_input('Enter E-mail:', type='password')
            hf_pass  = st.text_input('Enter password:', type='password')
            if not (hf_email and hf_pass):
                st.warning('Please enter your credentials!', icon='⚠️')
            else:
                st.success('Proceed to entering your prompt message!', icon='👉')
        st.caption('A message can go here') #? or st.markdown/latex/code/divider?
    
    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "DEFAULT RESPONSE"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            #! st.write(message["content"])
            st.write_stream(message["content"])

    # User-provided prompt
    if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt, hf_email, hf_pass) 
                #! st.write(response)
                st.write_stream(response) 
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
    

# --------------- DATA FRAME --------------- #
    #* [ARCHER]
def output() -> None:
    # TODO: Need to install streamlit essentails & use dataframe plugin
    #! Names should be clickable; sends user to analysis to take cloer look at medication.
    st.title('Table')
    
    #? Grab mock data file contents; load into df; correct dime/date [FIXME]
    df = pd.read_csv(os.path.join(os.getcwd(), "tests", "DemoMeds.csv"))
    df['Patent Expiration'] = pd.to_datetime(df['Patent Expiration'], format='%Y-%m-%d', errors='coerce').dt.strftime('%Y-%m-%d')
    
    table = dfExplorer(df, case=False)
    st.dataframe(table, use_container_width=True)
    
    st.markdown("Eventually each drug will be clickable to view individial analytics")


# --------------- ANALYTICS --------------- #
    #* [ALONSO]
def analysis() -> None:
    sub_tab = option_menu(
        None,
        options = ["Research", "Financial"],
        icons = ['prescription2', 'cash-stack'],
        default_index = 0,
        orientation = "horizontal", 
    )

    match sub_tab:
        case 'Research':
            research()
        case 'Financial':
            financial()

def research():
    st.subheader("Drug Progress Bar")
    
def financial():
    st.subheader("Graphs")

# --------------- SETTINGS --------------- #
def settings() -> None:
    st.title('Settings')
    #! About; Contact Us; Light/Dark theme changer; Ticket system (Setup Google Forms); Retrain model?
    #? Data sync between users
 
    CFG_PATH = os.path.join(os.getcwd(), ".streamlit", "config.toml")
    
    LIGHT = {
        'primaryColor'             : '"#3700B3"',
        'backgroundColor'          : '"#FFFFFF"',
        'secondaryBackgroundColor' : '"#F4F4F4"',
        'textColor'                : '"#000000"',
        'font'                     : '"sans serif"'
    }

    DARK = {
        'primaryColor'             : '"#BB86FC"',
        'backgroundColor'          : '"#121212"',
        'secondaryBackgroundColor' : '"#303030"',
        'textColor'                : '"#FFFFFF"',
        'font'                     : '"sans serif"'
    }

    # Check if the switch is on or off
    mode = LIGHT if st.checkbox('Switch Theme', value=False) else DARK

    # Writing changes to config.toml
    if os.path.exists(CFG_PATH):
        CFG = toml.load(CFG_PATH)
        CFG['theme'] = mode
        with open(CFG_PATH, 'w') as file:
            toml.dump(CFG, file)
        st.info('Please rerun the app to apply theme changes', icon='⚠️')
        
    else:
        st.error('[ERROR]: File "/.streamlit/config.toml" Does Not Exist', icon='🚨')
    

if __name__ == "__main__":
    main()
