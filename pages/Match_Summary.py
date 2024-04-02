# Match_Summary
    # This page will display general statistics about a given match.
# -----------------------------------------------------------------------------------
# Imports
# streamlit: creates our GUI: https://docs.streamlit.io/library/api-reference
import streamlit as st
# os: used to find locally stored files and open them
import os
# pandas: allows easy manipulation of a dataset by loading into dataframes
import pandas as pd
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Global Variables
# Set the default configuration for our GUI
st.set_page_config(page_title="RDOS Scouting", layout="wide", page_icon=":crystal-ball:")
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Functions

# -----------------------------------------------------------------------------------
# To-Do List
# - qual/playoff, match number
# - FIRST API estimated time it plays at
# - teams in match
#     - each team's super basic stats
#         - average pts?, average speaker, average amp, # pieces in auto or something
# - tournament rankings for each team
# - match prediction
#     - broken percent, avg pts, put weights on stuff, etc.
#     - prediction rate for tournament (see how good it is hehe)
#     - this is like the last thing to waste time on tbh. probably off season or pre-worlds (i hope) addition
# - estimated RP? given who can climb, if the alliance's average notes is 15-18 or w/e