# -----------------------------------------------------------------------------------
# Imports
# streamlit: creates our GUI: https://docs.streamlit.io/library/api-reference
import streamlit as st
# requests: make API requests (to the FIRST API)
import requests
# pandas: allows easy manipulation of a dataset by loading into dataframes
import pandas as pd
# gspread: allows you to modify and access Google Sheets
import gspread
# Lets you give your credentials so that you can access Google Sheets
    # To install, run: pip install google-auth-oauthlib
    # If that doesn't work, run: pip install google-api-python-client oauth2client
from oauth2client.service_account import ServiceAccountCredentials
# sys + path: helps Streamlit Cloud figure out where to look for other files used in our app
import sys
import path

# -----------------------------------------------------------------------------------
# Set up the path to our app so that the app knows where to look for other required files
dir = path.Path(__file__).abspath()
sys.path.append(dir.parent.parent)

# -----------------------------------------------------------------------------------
# Global Variables
# Name of the credentials JSON file that is required to access Google Sheets
google_creds = './Setup/scout_creds.json'
# Name of the file that stores your FIRST API authorization key
auth_file = 'authorization.txt'
# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
# Functions
# first_api_request: Takes a link to the FIRST API and makes a request. 
# Returns the response as a dictionary representing a JSON file
@st.cache_data
def first_api_request(url):
    # Authentication required to access FIRST API
        # To get your own authorization: https://frc-api-docs.firstinspires.org/#authorization
    auth_unique = open(auth_file, 'r').readline()
    payload={}
    headers = {
        'Authorization': auth_unique
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

# get_data: Loads the given CSV into a dataframe and returns the dataframe.
# Pass in the relative path to CSV file
@st.cache_data
def get_data(path_to_csv):
    return pd.read_csv(path_to_csv)

# get_google_sheet_records: Uses your Google credentials to access a given Google Sheet.
# Returns all of the records in the sheet as a dataframe
@st.cache_data
def get_google_sheet_records(google_sheet_name):
    # Let Google authorize our credentials so we can access our Google Sheets
        # NOTE: Make sure to share the Google Sheets with: 
            # google-drive-scouting-24@scouting-form-413106.iam.gserviceaccount.com
                # This email will not be the same for everyone.
    myscope = ['https://spreadsheets.google.com/feeds',
           'https://www.googleapis.com/auth/drive']
    mycreds = ServiceAccountCredentials.from_json_keyfile_name(google_creds, myscope)
    myclient = gspread.authorize(mycreds)

    # Open the Google Sheet file
    google_sheet = myclient.open(google_sheet_name).sheet1

    # Return all of the records in the Google Sheet as a dataframe
    sheet_records = google_sheet.get_all_records()
    return pd.DataFrame(sheet_records)