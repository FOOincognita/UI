import streamlit as st
#!! PUBLIC persistent storage; accessible by multiple employees
# Define the layout of the app, including the sidebar and main pages
def main():
    st.sidebar.title('Navigation')
    tab = st.sidebar.radio("Go to", ('Home', 'Table', 'Analysis', 'Settings', 'Chat'))

    if tab == 'Home':
        home()
    elif tab == 'Table':
        data()
    elif tab == 'Analysis':
        analysis()
    elif tab == 'Settings':
        settings()
    elif tab == 'Chat':
        chat()

# Define what will be displayed on each page
def home():
    st.title('Home')
    st.write('Welcome to the home page!')

def analysis():
    st.title('Table')
    st.write('This is the analysis page. You can add your analysis tools and visualizations here.')

def data():
    st.title('Analytics')
    st.write('This is the data page. Display your datasets or data-related functionalities here.')

def settings():
    st.title('Settings')
    st.write('This is the settings page. Add your configuration settings or user preferences here.')
    
def chat():
    st.title('Settings')
    st.write('This is the settings page. Add your configuration settings or user preferences here.')

if __name__ == "__main__":
    main()
