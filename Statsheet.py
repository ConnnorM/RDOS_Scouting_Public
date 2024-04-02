# -----------------------------------------------------------------------------------
# Imports
# streamlit: creates our GUI: https://docs.streamlit.io/library/api-reference
import streamlit as st
# pandas: allows easy manipulation of a dataset through objects called dataframes
import pandas as pd
# numpy: brings in math functions
import numpy as np
# os: used to find locally stored files and open them
import os
# FRC_Team: helps us store each team's information in separate objects
from Helpers import FRC_Team
# Data_Setup: stores functions for accessing/loading our data from various sources
from Helpers import Data_Setup
# image: lets us change the size of our images
from PIL import Image
# altair: lets us make nice charts and graphs
import altair as alt
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Global Variables
# !! WARNING: You must remember to change the URL variables to match the event info you want to pull !!
# FIRST API: Gives general match info, but the key is that it has Team Numbers
url_qual_matches = "https://frc-api.firstinspires.org/v3.0/2024/matches/CAOC?tournamentLevel=Qualification&teamNumber=&matchNumber=&start=&end="
# FIRST API: More specific match info, but no associated Team Numbers
url_qual_scores = "https://frc-api.firstinspires.org/v3.0/2024/scores/CAOC/Qualification?matchNumber=&start=&end="
# FIRST API: Lets you get all the teams at an event very easily
url_teams_list = "https://frc-api.firstinspires.org/v3.0/2024/teams?teamNumber=&eventCode=CAOC&districtCode=&state=&page="
# FIRST API: Lets you get a list of teams and their current ranking stats
url_rankings = "https://frc-api.firstinspires.org/v3.0/2024/rankings/CAOC?teamNumber=&top="
# # Authentication required to access FIRST API
#     # To get your own authorization: https://frc-api-docs.firstinspires.org/#authorization
# auth_unique = 'Basic YzdtYXJ0aW5kYWxlOjM2OTcwY2ExLTdiYzQtNGVkMy1hZTMxLWZhNDUzNmU3NDNhMg=='
# # Name of the credentials JSON file that is required to access Google Sheets
# google_creds = './Setup/scout_creds.json'
# Title of the Google Sheet that contains the responses to your stand scouting Google Form
stand_responses_gs_name = "2024 OC - Stand Scouting (Responses)"
# Title of the Google Sheet that contains the responses to your pit scouting Google Form
pit_responses_gs_name = "2024 OC - Pit Scouting (Responses)"
# Set the default configuration for our GUI
st.set_page_config(page_title="RDOS Scouting", layout="wide", page_icon=":dolphin:")
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Functions
# get_team_photo_filenames: Create a dictionary with keys as team numbers and values as the
# corresponding filename for that team's photo in the Team_Photos folder. This allows us to use
# different image file types (JPG, jpeg, etc.) without issues.
# Returns the dictionary
@st.cache_data
def get_team_photo_filenames():
  team_photo_filenames = {}
  teamPhotosFolderPath = './Team_Photos/OC/'
  for file in os.listdir(teamPhotosFolderPath):
    # Get the file name
    filename = os.fsdecode(file)
    # Extract only the integer value corresponding to the team's number
    # Mac does weird stuff and creates invisible files. This will ignore one of those files if
    # it weasled its way into your Team_Photos folder like it did to mine.
    if filename != '.DS_Store':
      team_num = int(filename.split('.')[0])
      team_photo_filenames[team_num] = filename 
  return team_photo_filenames

# create_FRC_Teams_dict: creates an FRC_Team object for each team and puts them in a dictionary
@st.cache_data
def create_FRC_Teams_dict(teamsAtEvent):
    teams_dict = {}
    for team_cur in teamsAtEvent:
        teams_dict[team_cur] = FRC_Team.FRC_Team(team_cur)
    return teams_dict

# populate_team_data: Use the pit/stand scouting data + data from the FRC API to fill in the stats for each team
@st.cache_data
def populate_team_data(standScoutedTeamsList, _teams_dict):
    # Let python know we want to edit our global variable FRC_Teams_dict instead of creating
    # a new variable of the same name inside this function
    for team in _teams_dict:
        # Only attempt to populate info for teams that we have stand scouting data for
        # if team in standScoutedTeamsList:
        _teams_dict[team].set_team_attributes()
    return _teams_dict

# assign_ranking_stats: Uses FIRST API to assign each FRC_Team object their ranking stats
@st.cache_data
def assign_ranking_stats(rankings_dict, _teams_dict):
    for rank_obj in rankings_dict["Rankings"]:
        rank = rank_obj["rank"]
        team = int(rank_obj["teamNumber"])
        avg_rp = rank_obj["sortOrder1"]
        coop = rank_obj["sortOrder2"]
        if team in _teams_dict.keys():
            _teams_dict[team].rank = rank
            _teams_dict[team].avg_rp = avg_rp
            _teams_dict[team].coop = coop
    return _teams_dict

# open_and_resize_image: takes the path to an image, opens it, and resizes it to fit our app's GUI.
# Returns the resized image
@st.cache_data
def open_and_resize_image(photo_path):
    im = Image.open(photo_path)
    new_im = im.resize((350, 300))
    # Not sure if we need to close this to be honest. Better safe than sorry.
    im.close()
    return new_im

# generate_rankings_df: creates a new dataframe of each team and the stats we would
# want to graph (max auto points, teleop speaker average, etc.)
# Returns the dataframe
@st.cache_data
def generate_rankings_df():
    # Initialize empty dataframe of attributes we'd want to graph
    cols_list = ['Team Number', 
                'Auto Max Speaker', 
                'Auto Avg Speaker',
                'Auto Max Amp', 
                'Auto Avg Amp',
                'Tele Max Speaker', 
                'Tele Avg Speaker',
                'Tele Acc Speaker',
                'Tele Max Amp', 
                'Tele Avg Amp',
                'Total Cycles',
                'Climbs',
                'Traps',
                'No Show',
                'Broken',
                'Auto Max Points',
                'Auto Avg Points',
                'Tele Max Points',
                'Tele Avg Points']
    rankings_df = pd.DataFrame(columns=cols_list)
    
    # For each team number in the teams dictionary, grab that FRC_Team object,
    # then add each stat to a list. Add that list to our dataframe as a row
    for key in st.session_state.FRC_Teams_dict:
        team = st.session_state.FRC_Teams_dict[key]

        # If we have no data, just use default values
        if len(team.cycles) != 0:
            avg_total_cycles = sum(team.cycles) / len(team.cycles)
        else:
            avg_total_cycles = 0
        if len(team.auto_pts) != 0:
            max_a_pts = max(team.auto_pts)
        else:
            max_a_pts = 0
        if len(team.tele_pts) != 0:
            max_t_pts = max(team.tele_pts)
        else:
            max_t_pts = 0


        row = [[team.num, 
               team.a_max_speaker,
               team.a_avg_speaker,
               team.a_max_amp,
               team.a_avg_amp,
               team.t_max_speaker,
               team.t_avg_speaker,
               team.t_acc_speaker,
               team.t_max_amp,
               team.t_avg_amp,
               avg_total_cycles,
               len(team.climb_matches),
               len(team.trap_matches),
               len(team.no_show_matches),
               len(team.broken_matches),
               max_a_pts,
               team.avg_auto_pts,
               max_t_pts,
               team.avg_tele_pts]]
        
        # Create a temporary dataframe for the data
        temp_df = pd.DataFrame(row, columns=cols_list)
        
        # Add the row to our dataframe
        rankings_df = pd.concat([rankings_df, temp_df], axis=0, ignore_index=True)
    
    # sort the dataframe by team number
    rankings_df = rankings_df.sort_values(by=["Team Number"], ascending=True)

    # Create an additional row that just stores average values to plot against
        # Averages DO NOT INCLUDE teams with a value of 0 in that category
    avg_row = [[0]]
    for col_name in cols_list:
        if col_name != 'Team Number':
            avg_row[0].append(rankings_df[rankings_df[col_name] != 0][col_name].mean())
    
    # Create a temporary dataframe for the data
    temp_df = pd.DataFrame(avg_row, columns=cols_list)
        
    # Add the row to our dataframe
    rankings_df = pd.concat([rankings_df, temp_df], axis=0, ignore_index=True)

    # return the full dataframe
    return rankings_df
# progranning goes here^^^^^^^^^^^^^^^

# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Main Code

# 1. Grab data from our various sources and make it accessible
# Connect to the FIRST API and grab the event's data. Make sure to update your URL variables above to match the event
matches_quals_dict = Data_Setup.first_api_request(url_qual_matches)
scores_quals_dict = Data_Setup.first_api_request(url_qual_scores)
teams_list_dict = Data_Setup.first_api_request(url_teams_list)
rankings_dict = Data_Setup.first_api_request(url_rankings)

# Connect to our Google Sheet that stores the scouting form responses and receive a dataframe with the scouting entries
stand_DF = Data_Setup.get_google_sheet_records(stand_responses_gs_name)
pit_DF = Data_Setup.get_google_sheet_records(pit_responses_gs_name)
# Sort our pit scouting responses by team number
if not pit_DF.empty:
    pit_DF = pit_DF.sort_values(by=['Team Number'])
    pit_DF = pit_DF.reset_index(drop=True)

# Use the FIRST API to get a list of all of the teams at the event
teamsAtEvent = []
for team in teams_list_dict['teams']:
    teamsAtEvent.append(team['teamNumber'])

# Change the format of the FIRST API teams_list_dict to be more usable and just store team names
team_names_dict = {}
for team in teams_list_dict['teams']:
    team_names_dict[team['teamNumber']] = [team['nameShort'], team['robotName']]

# Get a sorted list of all the teams we have already pit scouted
if not pit_DF.empty:
    pitScoutedTeamsList = pit_DF['Team Number'].drop_duplicates().sort_values().to_list()
else:
    pitScoutedTeamsList = []

if not stand_DF.empty:
    # Get a sorted list of all the teams we have at least one stand scouting entry for
    standScoutedTeamsList = stand_DF['Team Number'].drop_duplicates().sort_values().to_list()
    # Get match number of the latest match in our scouting data
    mostRecentMatchScout = stand_DF['Match Number'].max()
else:
    standScoutedTeamsList = []
    mostRecentMatchScout = 0

# Get match number of the latest match according to the FIRST API
mostRecentMatchAPI = len(matches_quals_dict['Matches'])

# Create a dictionary with team numbers as keys and paths to their bot's photo as values
photo_filenames_dict = get_team_photo_filenames()

# Add our important objects to the session state so that other pages can access them
if 'matches_quals_dict' not in st.session_state:
    st.session_state.matches_quals_dict = matches_quals_dict
if 'scores_quals_dict' not in st.session_state:
    st.session_state.scores_quals_dict = scores_quals_dict
if 'teams_list_dict' not in st.session_state:
    st.session_state.teams_list_dict = teams_list_dict
if 'team_names_dict' not in st.session_state:
    st.session_state.team_names_dict = team_names_dict    
if 'rankings_dict' not in st.session_state:
    st.session_state.rankings_dict = rankings_dict
if 'pit_DF' not in st.session_state:
    st.session_state.pit_DF = pit_DF
if 'stand_DF' not in st.session_state:
    st.session_state.stand_DF = stand_DF
if 'teamsAtEvent' not in st.session_state:
    st.session_state.teamsAtEvent = teamsAtEvent
if 'pitScoutedTeamsList' not in st.session_state:
    st.session_state.pitScoutedTeamsList = pitScoutedTeamsList
if 'standScoutedTeamsList' not in st.session_state:
    st.session_state.standScoutedTeamsList = standScoutedTeamsList
if 'mostRecentMatchScout' not in st.session_state:
    st.session_state.mostRecentMatchScout = mostRecentMatchScout
if 'mostRecentMatchAPI' not in st.session_state:
    st.session_state.mostRecentMatchAPI = mostRecentMatchAPI
if 'photo_filenames_dict' not in st.session_state:
    st.session_state.photo_filenames_dict = photo_filenames_dict

# Create an empty FRC_Team object for all of our teams and place them in a dictionary. 
# Keys: team number, values: FRC_Team object
if 'FRC_Teams_dict' not in st.session_state:
    st.session_state.FRC_Teams_dict = create_FRC_Teams_dict(teamsAtEvent)
    # Add ranking information to our teams
    st.session_state.FRC_Teams_dict = assign_ranking_stats(rankings_dict, st.session_state.FRC_Teams_dict)
    # Use the pit/stand scouting data + data from the FRC API to fill in the stats for each team
    st.session_state.FRC_Teams_dict = populate_team_data(standScoutedTeamsList, st.session_state.FRC_Teams_dict)

# Generate a dataframe of calculated stats for each team that we can use to graph
# Add the completed rankings DF to the streamlit session state so that
# all our pages can access this data
if 'rankings_df' not in st.session_state:
    st.session_state.rankings_df = generate_rankings_df()
    # Make a copy of the rankings DF that we can mutate and filter
    st.session_state.chart_data = st.session_state.rankings_df


# 3. Use Streamlit to nicely display our Statsheet
st.title("Statsheet")

# Make 2 columns on our page
left_column, right_column = st.columns(2)

with left_column:
    choose_team = st.selectbox(
        label="**Choose a Team**", options=teamsAtEvent
    )

    names_col, music_col = st.columns([0.7, 0.3])
    with names_col:
        st.write("**%s** | %s" % (st.session_state.FRC_Teams_dict[choose_team].name,
                              st.session_state.FRC_Teams_dict[choose_team].robot_name))
        st.write("Current Rank: %s | Avg. RP: %s | Co-op: %s" % (st.session_state.FRC_Teams_dict[choose_team].rank,
                                                     st.session_state.FRC_Teams_dict[choose_team].avg_rp,
                                                     st.session_state.FRC_Teams_dict[choose_team].coop))

    with music_col:
        try:
            audio_file = open(st.session_state.FRC_Teams_dict[choose_team].music,'rb') #enter the filename with filepath
            audio_bytes = audio_file.read() #reading the file
            st.audio(audio_bytes, format='audio/ogg') #displaying the audios
        except:
            print("Audio file not found: %s -music_col exception" % st.session_state.FRC_Teams_dict[choose_team].music)

    st.divider()

    l_left_column, l_mid_column, l_right_column, l_extra = st.columns(4)
    # How many matches they actually played: excludes no-show matches from count. Used to make
    # averages useful if a team missed a match or two
    matches_count_wo_no_show = len(st.session_state.FRC_Teams_dict[choose_team].matches) - len(st.session_state.FRC_Teams_dict[choose_team].no_show_matches)
    with l_left_column:
        st.write("#### Metric")
        st.write("Max Speaker:")
        st.write("Avg Speaker:")
        st.write("Acc Speaker:")
        st.write("Max Amp:")
        st.write("Avg Amp:")
        # st.write("Acc Amp:")
        st.write("Climb %:")
        st.write("Trap Count:")
        st.write("Multi-Trap Count:")
        st.write("Max Cycles:")
        st.write("Avg Cycles:")
        st.write("Max Pts:")
        st.write("Avg. Pts:")
    with l_mid_column:
        st.write("#### Auton")
        st.write("%s" % st.session_state.FRC_Teams_dict[choose_team].a_max_speaker)
        st.write("%s" % round(st.session_state.FRC_Teams_dict[choose_team].a_avg_speaker, 2))
        st.write("--")
        st.write("%s" % st.session_state.FRC_Teams_dict[choose_team].a_max_amp)
        st.write("%s" % round(st.session_state.FRC_Teams_dict[choose_team].a_avg_amp, 2))
        # st.write("--")
        st.write("--")
        st.write("--")
        st.write("--")
        st.write("--")
        st.write("--")
        if len(st.session_state.FRC_Teams_dict[choose_team].matches) != 0:
            st.write("%s" % max(st.session_state.FRC_Teams_dict[choose_team].auto_pts))
        else:
            st.write("N/A")
        avg_auto_pts = round(st.session_state.FRC_Teams_dict[choose_team].avg_auto_pts, 2)
        st.write("%s" % avg_auto_pts)
    with l_right_column:
        st.write("#### Teleop")
        st.write("%s" % st.session_state.FRC_Teams_dict[choose_team].t_max_speaker)
        st.write("%s" % round(st.session_state.FRC_Teams_dict[choose_team].t_avg_speaker, 2))
        tele_acc_speaker = st.session_state.FRC_Teams_dict[choose_team].t_acc_speaker
        st.write("%s%%" % round(tele_acc_speaker, 2))
        st.write("%s" % st.session_state.FRC_Teams_dict[choose_team].t_max_amp)
        st.write("%s" % round(st.session_state.FRC_Teams_dict[choose_team].t_avg_amp, 2))
        # st.write("%s%%" % round(st.session_state.FRC_Teams_dict[choose_team].t_acc_amp, 2))
        if choose_team in standScoutedTeamsList:
            climb_perc = len(st.session_state.FRC_Teams_dict[choose_team].climb_matches) / len(st.session_state.FRC_Teams_dict[choose_team].matches)
        else:
            climb_perc = 0
        st.write("%s%%" % (round(100 * climb_perc, 2)))
        st.write("%s" % len(st.session_state.FRC_Teams_dict[choose_team].trap_matches))
        st.write("%s" % len(st.session_state.FRC_Teams_dict[choose_team].multi_trap_matches))
        if len(st.session_state.FRC_Teams_dict[choose_team].matches) != 0:
            st.write("%s" % max(st.session_state.FRC_Teams_dict[choose_team].cycles))
        else:
            st.write("N/A")
        if choose_team in standScoutedTeamsList:
            st.write("%s" % (round(sum(st.session_state.FRC_Teams_dict[choose_team].cycles) / len(st.session_state.FRC_Teams_dict[choose_team].cycles), 2)))
        else:
            st.write("N/A")
        if len(st.session_state.FRC_Teams_dict[choose_team].matches) != 0:
            st.write("%s" % max(st.session_state.FRC_Teams_dict[choose_team].tele_pts))
        else:
            st.write("N/A")
        st.write("%s" % round(st.session_state.FRC_Teams_dict[choose_team].avg_tele_pts, 2))

with right_column:
    r_left_column, r_right_column = st.columns(2)
    with r_left_column:
        team_photo = open_and_resize_image(st.session_state.FRC_Teams_dict[choose_team].photo_path)
        st.image(image=team_photo, caption=st.session_state.FRC_Teams_dict[choose_team].important)

    with r_right_column:
        st.write("**Robot Info**")
        st.write("%s lbs. | " % st.session_state.FRC_Teams_dict[choose_team].weight, 
                 "%s: " % st.session_state.FRC_Teams_dict[choose_team].drivetrain,
                 "%s | " % st.session_state.FRC_Teams_dict[choose_team].drive_motors,
                 "Batteries: %s" % st.session_state.FRC_Teams_dict[choose_team].batteries)
        st.write("L: %s in. | W: %s in. | H: %s in. | " % (st.session_state.FRC_Teams_dict[choose_team].length, 
                                                        st.session_state.FRC_Teams_dict[choose_team].width,
                                                        st.session_state.FRC_Teams_dict[choose_team].height),
                 "Under Stage: %s" % st.session_state.FRC_Teams_dict[choose_team].under_stage)
        st.write("Scores In: %s | " % st.session_state.FRC_Teams_dict[choose_team].scoring_type,
                 "Vision: %s" % st.session_state.FRC_Teams_dict[choose_team].vision)
        st.write("Pref. Intake: %s | " % st.session_state.FRC_Teams_dict[choose_team].pref_intake,
                 "Can Intake: %s" % st.session_state.FRC_Teams_dict[choose_team].can_intake)
        st.write("Climb: %s | " % st.session_state.FRC_Teams_dict[choose_team].can_climb,
                 "Trap: %s | " % st.session_state.FRC_Teams_dict[choose_team].can_trap,
                 "Multi-Trap: %s" % st.session_state.FRC_Teams_dict[choose_team].can_multi_trap)

    # Holds the titles of each tab in the match selector
    matches_tabs_str = ['-'] * len(st.session_state.FRC_Teams_dict[choose_team].matches)
    # Holds the streamlit tabs
    st_tabs_maps = []
    # For each match, show the necessary info for the map
    if len(matches_tabs_str) != 0:
        for ind, match in enumerate(st.session_state.FRC_Teams_dict[choose_team].matches):
            # Set the tab's title
            matches_tabs_str[ind] = ('M' + str(match))
        st_tabs_maps = st.tabs(matches_tabs_str)
        
        for ind in range(len(st.session_state.FRC_Teams_dict[choose_team].matches)):
            with st_tabs_maps[ind]:
                auto_locs, tele_locs = st.columns(2)
                with auto_locs:
                    st.write("**Notes Used in Auto**")
                    auto_map = open_and_resize_image("./Field_Maps/auto_map.png")
                    st.image(image=auto_map)
                    st.write("%s" % st.session_state.FRC_Teams_dict[choose_team].auto_notes[ind])
                    # st.pyplot(st.session_state.FRC_Teams_dict[choose_team].auto_maps[ind])
                    st.write("Speaker: %s | Amp: %s | Taxi: %s" % (st.session_state.FRC_Teams_dict[choose_team].a_speaker_counts[ind], 
                                                        st.session_state.FRC_Teams_dict[choose_team].a_amp_counts[ind],
                                                        st.session_state.FRC_Teams_dict[choose_team].taxis[ind]))

                with tele_locs:
                    st.write("**Teleop Shooting Locations**")
                    tele_map = open_and_resize_image("./Field_Maps/teleop_map.png")
                    st.image(image=tele_map, caption=st.session_state.FRC_Teams_dict[choose_team].tele_shooting_locs)
                    # st.pyplot(st.session_state.FRC_Teams_dict[choose_team].shooting_locs_map[0])

st.divider()

if len(matches_tabs_str) != 0:
    charts_column, extras_column = st.columns([0.6, 0.4])
    # good altair walkthrough https://huppenkothen.org/data-visualization-tutorial/13-walkthrough-altair/index.html
    with charts_column:
        tele_shooting_chart_tab, points_chart_tab = st.tabs(["Teleop Shots", "Total Points"])
        with tele_shooting_chart_tab:
            chart = (
                alt.Chart(st.session_state.FRC_Teams_dict[choose_team].shots_DF)
                .mark_bar()
                .encode(
                    alt.Column("Match Number"), 
                    alt.X("Type", title=""),
                    alt.Y("Shots Made", axis=alt.Axis(grid=False), title="Teleop Shots Made"),
                    alt.Color("Type", legend=None)
                )
            )
            st.altair_chart(chart, use_container_width=False)

        with points_chart_tab:
            chart = (
                alt.Chart(st.session_state.FRC_Teams_dict[choose_team].points_DF)
                .mark_bar()
                .encode(
                    x = "Match Number:O",
                    y = "Points:Q"
                )
            )
            st.altair_chart(chart, use_container_width=True)

    with extras_column:
        st.write("#### Matches")
        matches_l, matches_m, matches_r = st.columns(3)
        with matches_l:
            st.write("Broken: %s" % st.session_state.FRC_Teams_dict[choose_team].broken_matches)
            st.write("No-Show: %s" % st.session_state.FRC_Teams_dict[choose_team].no_show_matches)
        with matches_m:
            st.write("Trap: %s" % st.session_state.FRC_Teams_dict[choose_team].trap_matches)
            st.write("Multi-Trap: %s" % st.session_state.FRC_Teams_dict[choose_team].multi_trap_matches)
        with matches_r:
            st.write("Climb: %s" % st.session_state.FRC_Teams_dict[choose_team].climb_matches)
            
        # Output all of our (serious) comments
        comms = ""
        for line in st.session_state.FRC_Teams_dict[choose_team].comments:
            comms += "- " + line + "\n"
        st.text_area(label="#### Comments", value=comms, height = 220)

st.divider()

# Create a button that clears the cache (which automatically reruns the app)
# Pressing this button will make the requests to our Google Sheet and the
# FIRST API again, allowing you to look for new data without the developer
# having to clear the cache themselves.
if st.button(label=":red[Refresh Data]"):
    # Clear all cached data from functions
    st.cache_data.clear()
    # Clear our our session state as well
    for key in st.session_state.keys():
        if key != 'pl_overall_df':
            del st.session_state[key]