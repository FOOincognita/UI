import json
import time
import streamlit as st

""" This file contains agents which will perform background operations (eg read/write)"""


class _ConfigAgent:
    """ This class will handle read/write to settings.json """ 
    
    def __init__(self) -> None:
        pass
    
    
    
#* --------------- CHAT STREAM GENERATOR --------------- #
#? Used to make chatbot responses print to screen similar to ChatGPT
#> Maybe use st.write when len(txt) is below threshold; low char count writes fun, though appears buggy
class _ChatAgent():
    
    #? Placeholder (default) str Messsage
    _LOREM = "Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor" \
           + "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis"         \
           + "nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."      \
    
    def __init__(self) -> None:
        pass

    @staticmethod
    def sstream(txt: str = _LOREM):
        #? Generator to feed st.write_stream(str)
        if type(txt) is not str:
            st.exception(TypeError("[ERROR]: stream_data() passed non-str type as input"))
            
        for word in txt.split(" "):
            yield f"{word} "
            time.sleep(0.04)