import streamlit as st
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


# Define what will be displayed on each page
    #* [ALONSO]
def home() -> None:
    #TODO: Streamlit Essentials has a chat plugin already
    #! "Welcome to Neuro-X1's GPT Bot"
    #! ChatBot/Chatbox "What are you looking to research today?"
    
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    def send_message():
        user_input = st.session_state.user_input
        if user_input:
            st.session_state.history.append(f"You: {user_input}")
            chatbot_response = "Chatbot response..." #! [FIXME]: ChatBot Response
            st.session_state.history.append(f"Chatbot: {chatbot_response}")
            st.session_state.user_input = ""

   
    st.title('Neuro-X1 AI')
    #st.write('What are you looking to research today?\n\n<Chatbot goes here>')
    chat_container = st.container()
            
    with st.container():
        # This will be fixed at the bottom of the page
        user_input = st.text_input("Your question", key = "user_input", on_change = send_message, placeholder = "Type here...")

    with chat_container:
        for idx, message in enumerate(st.session_state.history):
            st.text_area("", value = message, height = 75, key = (f"msg_{idx}"))


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
