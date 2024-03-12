import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
#!! PUBLIC persistent storage; accessible by multiple employees
# Define the layout of the app, including the sidebar and main pages

# [TODO]: 
#    1. Implement subtabs for analysis (bubbles)
#    2. [Almost Done] Implement Home chatbot screen (using streamlit essentials)
#    3. Add dataframe & prepare table input/output for easy back-end connection
#    4. Brainstrom what kinds of financial & consumer data we'd like to display, & using which graph(s)
#        - Find sources for this info
#    5. Implement settings
#

# App title
st.set_page_config(page_title="NX1 Chat")

def main():
    st.sidebar.title('Navigation')
    tab = st.sidebar.radio('Tabs', ('Home', 'Output', 'Analysis', 'Settings'))

    match tab:
        case 'Home':
            home()
        case 'Output':
            output()
        case 'Analysis':
            analysis()
        case 'Settings':
            settings()
        case _:
            raise Exception


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
    #! ChatBot Docs: https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/
def home() -> None:
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
        st.markdown('A message can go here')
    
    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "DEFAULT RESPONSE"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

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
                st.write(response) 
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
    

# --------------- DATA FRAME --------------- #
    #* [ARCHER]
def output() -> None:
    # TODO: Need to install streamlit essentails & use dataframe plugin
    """ This page will show rank table """
    st.title('Table')
    st.write('This is the Table page!')
    #* [ARCHER] 
    #! Full Dataframe with Filter, save, & expand
        #> Names should be clickable; sends user to analysis to take cloer look at medication.
    
    #! LATER DOWN THE LINE:
        #> Clickable option to pull up single/specific analysis page


# --------------- ANALYTICS --------------- #
    #* [ALONSO]
def analysis() -> None:
    """ This page will show analytics fropm table & additional financial analytics """
    st.title('Analytics')
    st.write('This is the data page. Display your datasets or data-related functionalities here.')
    #! GRAPHS
    #! TOP 5s; Overview for each
        #? SUB-TAB: Drug research stage (eg stage II clinical trials)
        #? SUB-TAB: Drug financials (simialar drugs financials?)
        #? SUB-TAB: Consumer Data


# --------------- SETTINGS --------------- #
    #* [ARCHER]
def settings() -> None:
    """ This is a simple settings page """
    st.title('Settings')
    st.write('This is the settings page. Add your configuration settings or user preferences here.')
    #! Light/Dark theme changer 
    #! Ticket system; Setup Google Form using @neurox1.com email
    #! Data sync between users 
        #> If local, R/W lock
        #> If Azure, no problem; only 1 person can access anyways
        
    #! LATER DOWN THE LINE: TAB: Retrain model?
    

if __name__ == "__main__":
    main()
