import streamlit as st
import toml 
import os

def settings() -> None:
    st.title('Settings')
    CFG_PATH = os.path.join(os.getcwd(), ".streamlit", "config.toml")

    # Define theme options
    LIGHT = {
        'primaryColor':   '"#3700B3"',
        'backgroundColor': '"#FFFFFF"',
        'secondaryBackgroundColor': '"#F4F4F4"',
        'textColor': '"#000000"',
        'font': '"sans serif"'
    }

    DARK = {
        'primaryColor': '"#BB86FC"',
        'backgroundColor': '"#121212"',
        'secondaryBackgroundColor': '"#303030"',
        'textColor': '"#FFFFFF"',
        'font': '"sans serif"'
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
        st.error('[ERROR]: /.streamlit/config.toml Does Not Exist!')
