import streamlit as st
#!! PUBLIC persistent storage; accessible by multiple employees
# Define the layout of the app, including the sidebar and main pages

"""
# [TODO]: 
    1. Implement subtabs for analysis (bubbles)
    2. Implement Home chatbot screen using streamlit essentials
    3. Add dataframe & stage table IO
    4. Brainstrom financial & consumer data we'd like to display
        - Find sources for this info
    5. Implement settings
    
"""

def main():
    st.sidebar.title('Navigation')
    tab = st.sidebar.radio(('Home', 'Output', 'Analysis', 'Settings', 'Chat'))

    match tab:
        case 'Home':
            home()
        case 'Table':
            output()
        case 'Analysis':
            analysis()
        case 'Settings':
            settings()
        case _:
            raise Exception


# Define what will be displayed on each page
def home() -> None:
    #TODO: Streamlit Essentials has a chat plugin already
    """ Welcome & Chat """
    st.title('Home')
    st.write('<short & sweet intro>\n\n<Chatbot goes here>')
    #! Description
    #! ChatBot/Chatbox 
    

def output() -> None:
    # TODO: Need to install streamlit essentails & use dataframe plugin
    """ This page will show rank table """
    st.title('Table')
    st.write('This is the Table page!')
    #! Full Dataframe with Filter, save, & expand
        #> Names should be clickable; sends user to analysis to take cloer look at medication.

def analysis() -> None:
    """ This page will show analytics fropm table & additional financial analytics """
    st.title('Analytics')
    st.write('This is the data page. Display your datasets or data-related functionalities here.')
    #! GRAPHS
    #! TAB: Drug research stage (eg stage II clinical trials)
    #! TAB: Drug financials (simialr drugs financials?)
    #! TAB: Consumer Data


def settings() -> None:
    """ This is a simple settings page """
    st.title('Settings')
    st.write('This is the settings page. Add your configuration settings or user preferences here.')
    #! Light/Dark theme changer 
    #! Ticket system
    #! Data sync between users 
    #! User IDs
    #! Retrain model option
    #! Find out where it will be ran:
        #> If local, mutex lock
        #> If Azure, no problem

if __name__ == "__main__":
    main()
