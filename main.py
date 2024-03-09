import streamlit as st
#!! PUBLIC persistent storage; accessible by multiple employees
# Define the layout of the app, including the sidebar and main pages

"""
# [TODO]: 
    1. Implement subtabs for analysis (bubbles)
    2. Implement Home chatbot screen (using streamlit essentials)
    3. Add dataframe & prepare table input/output for easy back-end connection
    4. Brainstrom what kinds of financial & consumer data we'd like to display, & using which graph(s)
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
    #* [ALONSO]
def home() -> None:
    #TODO: Streamlit Essentials has a chat plugin already
    """ Welcome & Chat """
    st.title('Home')
    st.write('<short & sweet intro>\n\n<Chatbot goes here>')
        #! "Welcome to Neuro-X1's GPT Bot"
        #! ChatBot/Chatbox "What are you looking to research today?"
    
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
        #? SUB-TAB: Drug financials (simialr drugs financials?)
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
