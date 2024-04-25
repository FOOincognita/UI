import os
import pandas as pd

import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer as dfExplorer

from Modules.Agents import _ConfigAgent as Cfg, _ChatAgent as ChatUI #? Read/Write to/from settings.json


# TODO:
#    * ADD AUTO-SEND FOR CRASHES FOR REMOTE & AUTONOMOUS BUG FIXES
#    * Brainstrom what kinds of financial & consumer data we'd like to display, & using which graph(s)
#        > Find sources for this info
#    * Implement settings

#* Add bouncing image on first boot


#* --------------- GLOBAL CONFIG --------------- *#
# Global App Config
st.set_page_config(
    page_title = "Aggies Create | MedGet", 
    page_icon  = "assets/NX1_Favicon.png",
    layout     = "wide",
    menu_items = {             
        # FIXME: Replace with proper links 
        'Get Help'     : 'https://github.com/FOOincognita/UI/', #!
        'Report a bug' : "https://github.com/FOOincognita/UI/", #!
        'About'        : "# This is a Header!"                  #!
    }
)


def main() -> None:
    with st.sidebar:
        tab = option_menu(
            default_index = 0,
            menu_title    = "MedGet",
            menu_icon     = "capsule", # "prescription"; "prescription2"
            options       = ["Chat", "Output", "Analysis", "Settings"] , #? Maybe move settings to bottom; cog icon?
            icons         = ["robot", "database", "kanban", "gear"],
        )
    
    match tab:
        case 'Chat':     chat()
        case 'Output':   output()
        case 'Analysis': analysis()
        case 'Settings': settings()
        case _:
            st.exception(RuntimeError("[ERROR]: Default Case Reached in main()"))


#* --------------- CHATBOT --------------- *#
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
    # Hugging Face Credentials
    with st.sidebar:
        st.title('💬 MedGet HF Login')
        if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
            st.success('HuggingFace Login credentials already provided!', icon='✅')
            hf_email = st.secrets['EMAIL']
            hf_pass  = st.secrets['PASS']
        else:
            hf_email = "" # st.text_input('Enter E-mail:', type='email')
            hf_pass  = "" # st.text_input('Enter Password:', type='password')
            if not (hf_email and hf_pass):
                st.warning('Please enter your credentials!', icon='⚠️')
            else:
                st.success('Proceed to entering your prompt message!', icon='👉')
        st.caption('A message can go here') #? or st.markdown
    
    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Welcome to MedGet! What can I help you with today?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            #! st.write(message["content"])
            st.write_stream(ChatUI.sstream(message["content"])) 

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
                st.write_stream(ChatUI.sstream(response))
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
    

#* --------------- DATA FRAME --------------- *#
def output() -> None:
    #? Names clickable; sends user to analysis to take cloer look at medication.
    st.title('Table')
    
    #? Grab mock data file contents; load into df; correct dime/date [FIXME]
    df = pd.read_csv(os.path.join(os.getcwd(), "tests", "DemoMeds.csv"))
    df['Patent Expiration'] = pd.to_datetime(df['Patent Expiration'], format='%Y-%m-%d', errors='coerce').dt.strftime('%Y-%m-%d')
    
    table = dfExplorer(df, case=False)
    st.dataframe(table, use_container_width=True)
    
    st.caption("Eventually each drug will be clickable to view individial analytics")


#* --------------- ANALYTICS --------------- *#
def analysis() -> None:
    sub_tab = option_menu(
        None,
        options       = ["Research", "Financial"],
        icons         = ['prescription2', 'cash-stack'],
        default_index = 0,
        orientation   = "horizontal", 
    )

    match sub_tab:
        case 'Research':  research()
        case 'Financial': financial()
        case _:
            st.exception(RuntimeError("[ERROR]: Default Case Reached in analysis()"))

def research():
    st.subheader("Drug Progress Bar")
    #* 0. Stepper Bar - Progress Bar for Drug

    #* 1. Graphs
        ## i. 3D Map
            ## ia. 
        ## ii. 
        ## iii. 
        ## iv. 
        
def financial():
    st.subheader("Graphs")
    #* 0. 

#* --------------- SETTINGS --------------- *#
def settings() -> None:
    st.title('Settings')

    
    #* 0. App settings
        ## i. App Theme
    
    #* 1. File Handling
        ## i. File Selection Box (ADD WARNING)
        ## ii. File Upload for AI model
        
    #* 2. Model Settings
        ## i. Model Type
        
    #* 3. Information
        ## i. About
        ## ii. Contact Us
        ## iii. Updates & version no & last updated counter
    

if __name__ == "__main__":
    main()
