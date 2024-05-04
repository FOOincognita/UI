import os
import pandas as pd
import time

from openai import OpenAI

import streamlit as st
##from hugchat import hugchat
##from hugchat.login import Login
from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer as dfExplorer

##from Modules.Agents import _ConfigAgent as Cfg, _ChatAgent as ChatUI #? Read/Write to/from settings.json
from Modules.HMAIntegrated import get_bio_response  as promptBio,  \
                                  get_user_response as stdIn,      \
                                  generate_response as genResponse
from WIPCode.financial import financial as fin
from WIPCode.MUI import dashboard as dash


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
            options       = ["Chat", "Output", "Analysis", "Files", "HMA", "Dashboard"] , #? Maybe move settings to bottom; cog icon?
            icons         = ["robot", "database", "kanban", "file", "bounding-box", "columns-gap"],
        )
    
    match tab:
        case 'Chat':     chat()
        case 'Output':   output()
        case 'Analysis': analysis()
        case 'Files': settings()
        case 'HMA': HMA()
        case 'Dashboard': dashboard()
        case _:
            st.exception(RuntimeError("[ERROR]: Default Case Reached in main()"))


def sstream(txt: str, speed: float=0.04):
    for word in txt.split():
        yield f"{word} "
        time.sleep(speed)

#* --------------- CHATBOT --------------- *#

PORT = 1234
endpoint = OpenAI(base_url=f"http://localhost:{PORT}/v1", api_key="lm-studio")

bio_messages = [{"role": "system", "content": "Respond to the best of your ability."}]
BIO_MODEL_NAME = "MaziyarPanahi/BioMistral-7B-GGUF/BioMistral-7B.Q8_0.gguf"

# Function for generating LLM response
def generate_response(prompt_input: str="", email: str="", passwd: str="") -> str | None:
    # Hugging Face Login
    # sign = Login(email, passwd)
    # cookies = sign.login()
    # Create ChatBot                        
    # chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    # return chatbot.chat(prompt_input)
    
    completion = endpoint.chat.completions.create(
        messages=st.session_state.messages,
        temperature=0.7,
        model=BIO_MODEL_NAME,
    )
    
    return completion.choices[0].message.content
    
    


# Define what will be displayed on each page
def chat() -> None:
    # Hugging Face Credentials
    with st.sidebar:
        st.caption("In this window, a chat interface is available. The current model is BioMistral, a 7B parameter model trained on PubMed")
        st.caption("\nNOTE: A bug currently exists that causes the previous response to appear if >1 question is asked, though it is temporary & will be patched in future releases.")
    
    # Store LLM generated responses
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Welcome to MedGet! My name is BioMistral! I am a Mistral-7B model trained on Pubmed datasets. What can I help you with today?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            ##st.write_stream(sstream(message["content"])) 

    # User-provided prompt
    # if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    if prompt := st.chat_input(disabled=False):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt)
                st.write(response)
                ##st.write_stream(sstream(response))
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
    

#* --------------- DATA FRAME --------------- *#
def output() -> None:
    #? Names clickable; sends user to analysis to take cloer look at medication.
    st.title('Table Output')
    st.caption("This feature is not yet dynamically updated by model output, however we've provided a mock dataset to show the concept.\nUsing the pull down, the dataframe can be filtered using any of the columns present.\nWhen a model outputs a list of medications it recommends, each of those medications + all associated data will populate this table.\n\nThe user will then be able to click any of the medications, which will bring them to the 'Analysis' tab, where they can view any/all data associated with the medication")
    
    #? Grab mock data file contents; load into df; correct dime/date [FIXME]
    # df = pd.read_csv(os.path.join(os.getcwd(), "tests", "DemoMeds.csv"))
    df = pd.read_csv("./tests/DemoMeds.csv")
    df['Patent Expiration'] = pd.to_datetime(df['Patent Expiration'], format='%Y-%m-%d', errors='coerce').dt.strftime('%Y-%m-%d')
    
    table = dfExplorer(df, case=False)
    st.dataframe(table, use_container_width=True)



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
    #* 0. Stepper Bar - Progress Bar for Drug
    from WIPCode.maps import research
    
    research()

    #* 1. Graphs
        ## i. 3D Map
            ## ia. 
        ## ii. 
        ## iii. 
        ## iv. 
        
def financial():
    fin()
    #* 0. 

#* --------------- SETTINGS --------------- *#
def settings() -> None:
    st.title('File Embedding')
    st.caption("We are currently in the process of implementing a LangChain integration. LangChain will allow users to upload files such as PDFs, Excel spreadsheets, etc containing unique/private data, it will store it on a local private vector database, then all models will have access to it & will refer to it when necessary.\nLangChain will also give the models access to Google services like Search, Drive, & even YouTube transcripts.")
    files = st.file_uploader("Upload files to embed", accept_multiple_files=True)
    if files:
        st.write("Files Sucessfully uploaded")
        ##st.write(bytes_data)
        
        
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
    
    
#!! get_bio_response as promptBio, get_user_response as stdIn, generate_response as genResponse
def HMA():
    with st.sidebar:
        st.subheader("IMPORTANT")
        st.caption("This is certainly a work in progress -- while the intended communication path does work sometimes, other times the models will begin to argue back & forth to eachother, or begin to confuse eachother.\nWe are testing various prompt structures to minimize these internal loops.\nIf on the chat window after the 'Thinking...' spinner goes away, if you do not see a new response, you may be able to see the models argue back & forth in LMStudio's window by slightly scrolling up on the 'Server Logs' text window.")
        st.subheader("What is HMA?")
        st.caption("Hybrid Model Architecture utilizes 2 or more models. In our case, we use 2 -- Llama-3-8B is used to handle user interactions (will be replaced by the 70B or 400B Llama-3 model, or Mixtral 8x22B), though if the user asks any biomedical questions, Llama will ask BioMistral, a Mistral model trained on Pubmed. It will then read & reformat BioMistral's response such that it is more digestible by a user.\nBiomistral will soon be replaced by Mixtral 8x22B which we will train on PubMed datasets.")
    
    # Store LLM generated responses
    if "HMA" not in st.session_state:
        st.session_state["HMA"] = [{"role": "assistant", "content": "Howdy! I'm an assistant here to help answer any questions you might have. I can provide information on a wide range of topics, and if there's a question that requires specific biomedical knowledge, I can consult with a biomedical AI model to ensure you get the most accurate answer possible. How can I assist you today?"}]

    # Display chat messages
    for message in st.session_state.HMA:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            ##st.write_stream(sstream(message["content"])) 

    # User-provided prompt
    if prompt := st.chat_input(disabled=False):
        st.session_state.HMA.append({"role": "user", "content": f"[USER] prompt"})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate a new response if last message is not from assistant
        if st.session_state.HMA[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = genResponse(prompt)
                    ##st.write(response)
                    st.write_stream(sstream(message["content"])) 
            st.session_state.HMA.append({"role": "assistant", "content": response})

#      
        


def dashboard():
    st.title("Dynamic Dashboard")
    st.caption("This is a proof of concept for using the material UI kit in Streamlit to build dynamic interfaces that the user can modify freely.\n\nThis doesn't look too aesthetcially pleasing at the moment, however once fully implemented, it will allow users to tailor their experience to their liking.\nGiven this is purely aesthetic, it has low-priority")
    dash()
    pass

if __name__ == "__main__":
    main()
