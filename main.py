import streamlit as st
#!! PUBLIC persistent storage; accessible by multiple employees
# Define the layout of the app, including the sidebar and main pages

def main():
    st.sidebar.title('Navigation')
    tab = st.sidebar.radio(('Home', 'Table', 'Analysis', 'Settings', 'Chat'))

    match tab:
        case 'Home':
            home()
        case 'Table':
            table()
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
    st.write('Welcome to the home page!')

def table() -> None:
    # TODO: Need to install streamlit essentails & use dataframe plugin
    """ This page will show rank table """
    st.title('Table')
    st.write('This is the Table page!')

def analysis() -> None:
    """ This page will show analytics fropm table & additional financial analytics """
    st.title('Analytics')
    st.write('This is the data page. Display your datasets or data-related functionalities here.')

def settings() -> None:
    """ This is a simple settings page """
    st.title('Settings')
    st.write('This is the settings page. Add your configuration settings or user preferences here.')

if __name__ == "__main__":
    main()