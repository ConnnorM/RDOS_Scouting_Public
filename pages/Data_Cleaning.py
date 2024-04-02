# Data Cleaning
    # This page will display the output of our data validation efforts. It does not make any changes
    # to the input data; it merely informs the user where incorrect data is detected.
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
# Store our st.session_state attributes in more readable terms 
# TODO: don't copy session_state variables we won't actually use
matches_quals_dict = st.session_state.matches_quals_dict
scores_quals_dict = st.session_state.scores_quals_dict
teams_list_dict = st.session_state.teams_list_dict
# rankings_dict = st.session_state.rankings_dict
pit_DF = st.session_state.pit_DF
stand_DF = st.session_state.stand_DF
teamsAtEvent = st.session_state.teamsAtEvent
pitScoutedTeamsList = st.session_state.pitScoutedTeamsList
mostRecentMatchScout = st.session_state.mostRecentMatchScout
mostRecentMatchAPI = st.session_state.mostRecentMatchAPI
# Maximum robot perimeter for current year + 5 inches per each side (margin for bumpers)
max_perimeter_inches = 120 + 20
# Set the default configuration for our GUI
st.set_page_config(page_title="RDOS Scouting", layout="wide", page_icon=":broom:")
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Functions
# get_photos_taken_list: Returns a list of all of the teams whose robot we have a picture of
@st.cache_data
def get_photos_taken_list():
    # NOTE: The photos' filenames should be ####.filetype EX: "123.jpeg"
    photosTakenList = []
    # In the folder where your home page (Statsheet.py) is stored, find and enter the folder
    # called 'Team_Photos'
    teamPhotosFolderPath = os.getcwd() + '/Team_Photos/OC/'
    # Loop through each file in the given photos folder
    try:
        for file in os.listdir(teamPhotosFolderPath):
            # Get the file name
            filename = os.fsdecode(file)
            # Extract only the integer value corresponding to the team's number
            # Don't include the funky invisible file that Mac sometimes creates
            if filename != '.DS_Store':
                filename = int(filename.split('.')[0])
                # Add the team number to the list of teams we have a photo for
                photosTakenList.append(filename)
        # Once we have all the team numbers, sort the list
        if len(photosTakenList) != 0:
            photosTakenList.sort()
    except:
        # If there is nothing in the folder, the function returns an empty list
        pass
    
    return photosTakenList

# get_missing_pit_entries: Returns a list of all the teams that we are missing pit scouting data for
@st.cache_data
def get_missing_pit_entries():
    missing = []
    for team in st.session_state.teamsAtEvent:
        if team not in pitScoutedTeamsList:
            missing.append(team)
    return missing

# get_missing_photos: Returns a list of all the teams that we are missing photos for
@st.cache_data
def get_missing_photos(photosTakenList):
    missing = []
    for team in st.session_state.teamsAtEvent:
        if team not in photosTakenList:
            missing.append(team)
    return missing

# get_wrong_team_numbers_pit: Returns a list of all the incorrect team numbers in our pit scouting data
@st.cache_data
def get_wrong_team_numbers_pit():
    wrong = []
    for team in pitScoutedTeamsList:
        if team not in st.session_state.teamsAtEvent:
            wrong.append(team)
    return wrong

# get_wrong_team_numbers_photos: Returns a list of all the incorrect team numbers in our robot photos
@st.cache_data
def get_wrong_team_numbers_photos(photosTakenList):
    wrong = []
    for team in photosTakenList:
        if team not in st.session_state.teamsAtEvent:
            wrong.append(team)
    return wrong

# get_illegal_perimeters: Returns a list of teams who have an illegal (too big) frame perimeter
@st.cache_data
def get_illegal_perimeters():
    illegal = []
    for team in st.session_state.teamsAtEvent:
        # TODO: figure out why we need .values[0] here and explain it in comments
        team_entry = pit_DF.loc[pit_DF['Team Number'] == team]
        length = team_entry['Robot Length'].values[0]
        width = team_entry['Robot Width'].values[0]
        perimeter = 2*length + 2*width
        if perimeter > max_perimeter_inches:
            illegal.append(team)
    return illegal

# get_wrong_team_numbers_stand: Finds entries with wrong team numbers. Returns a list of invalid team numbers
@st.cache_data
def get_wrong_team_numbers_stand():
    wrong_teams = []
    # A list of every value in the Team Number column from the stand scouting data (includes duplicates)
    allStandScoutedTeams = stand_DF['Team Number'].to_list()
    # Get the indexes in the stand scouting dataframe of matches with wrong team numbers
    for team in allStandScoutedTeams:
        if team not in st.session_state.teamsAtEvent:
            wrong_teams.append(team)
    wrong_teams.sort()
    return wrong_teams

# get_duplicate_entries_stand: Finds any entries that have the same match number and team number.
# Returns a dataframe filled with all of these entries.
@st.cache_data
def get_duplicate_entries_stand():
    # Make an empty dataframe with the same columns as our stand_DF dataframe
    duplicate_entries = pd.DataFrame(columns=stand_DF.columns.to_list())
    # Loop through all entries for each match number, and if any of the team numbers match, add them to our
    # dataframe of duplicate entries
    for match_num in range(st.session_state.mostRecentMatchScout):
        # Get all the entries with the given match number
        cur_match_df = stand_DF.loc[stand_DF['Match Number'] == match_num + 1]
        # Look at all entries in cur_match_df, and if we have any duplicate values in 
        # 'Team Number', add those entries to the duplicate_entries dataframe
        duplicate_entries = pd.concat([duplicate_entries, cur_match_df[cur_match_df.duplicated(['Team Number'], keep=False)]])
    return duplicate_entries

# get_duplicate_entries_pit: Finds any entries that have the same team number.
# Returns a dataframe filled with all of these entries.
@st.cache_data
def get_duplicate_entries_pit():
    # Make an empty dataframe with the same columns as our stand_DF dataframe
    duplicate_entries = pd.DataFrame(columns=pit_DF.columns.to_list())
    # Collect all entries with a duplicate team number
    duplicate_entries = pd.concat([duplicate_entries, pit_DF[pit_DF.duplicated(['Team Number'], keep=False)]])
    return duplicate_entries

# get_teams_w_wrong_match_count: Compares the FIRST API to the scouting data to determine
# if a team has more or less matches scouted than they should have.
# Returns a dictionary of these teams and the number of matches they should have entries for and
# the number of matches they do have entries for.
@st.cache_data
def get_teams_w_wrong_match_count():
    # Get a sorted dictionary of each team number and how many of their matches we have data for
    matches_per_team_dict_scout = stand_DF['Team Number'].value_counts().to_dict()
    matches_per_team_dict_scout = dict(sorted(matches_per_team_dict_scout.items()))

    # Use the FIRST API to know how many entries each team should have
    # Make a dictionary with each team number as a key and their values set to 0
    matches_per_team_dict_api = {}
    for team in st.session_state.teamsAtEvent:
        matches_per_team_dict_api[team] = 0
    # Loop through each team in each match from the API and tally the matches played
    for match_ind in range(st.session_state.mostRecentMatchAPI):
        # Loop through all 6 teams in the current match
        for team_ind in range(6):
            cur_team = matches_quals_dict['Matches'][match_ind]['teams'][team_ind]['teamNumber']
            matches_per_team_dict_api[cur_team] += 1
    
    # Compare the two dictionaries (scout data vs. API data) and find teams that don't have the correct
    # number of matches
    missing_data = {}
    # First, check the lengths of the dictionaries to see if a team is missing completely
    missing_teams = set(matches_per_team_dict_api) - set(matches_per_team_dict_scout)
    # If a team is missing completely, return the empty dictionary
    # TODO: clean this up so missing teams don't just break stuff. Or only call this function
    # if all teams are present?
    if len(missing_teams) != 0:
        pass
    # We know we have at least one entry for all teams, so continue
    else: 
        # Loop through all the teams from the API's dictionary and compare values
        for team in matches_per_team_dict_api:
            api_matches = matches_per_team_dict_api.get(team)
            scout_matches = matches_per_team_dict_scout.get(team)
            # If the match counts aren't equal, return a dictionary with the key as the team's
            # number and the values as the number of matches in the API and number of scouted
            # matches
            if api_matches != scout_matches:
                missing_data[team] = [api_matches, scout_matches]
    return missing_data

# check_six_entries_per_match: Finds matches with less/more than 6 total entries. 
# Returns a dictionary with keys as the match number and values as the number of teams we
# have for that match.
# TODO: tell us which teams are missing from FIRST API
@st.cache_data
def check_six_entries_per_match():
    matches_missing_teams = {}
    entries_per_match_series = stand_DF['Match Number'].value_counts()
    # TODO: make sure index doesn't need to be index+1 anywhere in here
    for index, value in entries_per_match_series.items():
        if value != 6:
            matches_missing_teams[index] = value
    return matches_missing_teams

# get_invalid_alliances: Finds matches with alliances that do not have 3 red and 3 blue teams.
# Returns a dictionary with keys as the match number and values as the list of [red, blue]
# teams in the match.
@st.cache_data
def get_incomplete_alliances():
    invalid_alliances = {}
    for i in range(st.session_state.mostRecentMatchScout):
        cur_match_df = stand_DF.loc[stand_DF['Match Number'] == i+1]
        count_red = len(cur_match_df.loc[cur_match_df['Alliance Color'] == 'Red'])
        count_blue = len(cur_match_df.loc[cur_match_df['Alliance Color'] == 'Blue'])
        if count_red != 3 or count_blue != 3:
            invalid_alliances[i+1] = [count_red, count_blue]
    return invalid_alliances

# get_rescout_requests: Finds matches with rescout requests and adds the entry to a dataframe.
# Returns the dataframe.
@st.cache_data
def get_rescout_requests():
    # Fastest and least memory intensive way is to add all rows to a list and use that list to create
    # a dataframe at the end of the function.
    rescouts_list = []
    # We don't use index, but we need it here because iterrows returns two values
    for index, row in stand_DF.iterrows():
         if row['Rescout Request'] == "Yes":
               rescouts_list.append(row[["Scouter Name",
                                        "Match Number",
                                        "Team Number",
                                        "Rescout Request"]])
    rescouts_DF = pd.DataFrame(rescouts_list)
    return rescouts_DF
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# GUI Output
st.title("Data Cleaning")
st.write("Teams at Event: %s" % teamsAtEvent)
st.write("Pit Scouted Teams: %s" % pitScoutedTeamsList)
st.write("Teams Left to Pit Scout: %s" % get_missing_pit_entries())
photosTakenList = get_photos_taken_list()
st.write("Team Photos: %s" % photosTakenList)
st.write("Teams Missing Photo: %s" % get_missing_photos(photosTakenList))
st.write("Invalid Team Numbers (Pit Scouting): %s" % get_wrong_team_numbers_pit())
st.write("Invalid Team Numbers (Photos): %s" % get_wrong_team_numbers_photos(photosTakenList))
# st.write("Illegal Perimeters: %s" % get_illegal_perimeters())
if not stand_DF.empty:
    st.write("Invalid Team Numbers (Stand Scouting): %s" % get_wrong_team_numbers_stand())
    st.write("Teams with Wrong Number of Matches: %s" % get_teams_w_wrong_match_count())
    st.write("Matches Without 6 Entries: %s" % check_six_entries_per_match())
# st.write("get_incomplete_alliances: %s" % get_incomplete_alliances())
st.write("Duplicate Entries (Pit Scouting):")
st.dataframe(get_duplicate_entries_pit())
if not stand_DF.empty:
    st.write("Duplicate Entries (Stand Scouting):")
    st.dataframe(get_duplicate_entries_stand())
    rescouts_DF = get_rescout_requests()
    st.write("Rescout Requests: %s" % len(rescouts_DF.index))
    st.dataframe(rescouts_DF)
# -----------------------------------------------------------------------------------