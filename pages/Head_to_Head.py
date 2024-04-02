# Head_to_Head
    # This page will allow you to compare the stats of up to 3 teams at once in
    # a less comprehensive view of the individual team Statsheet page
# -----------------------------------------------------------------------------------
# Imports
# streamlit: creates our GUI: https://docs.streamlit.io/library/api-reference
import streamlit as st
# image: lets us change the size of our images
from PIL import Image
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Global Variables
# Set the default configuration for our GUI
st.set_page_config(page_title="RDOS Scouting", layout="wide", page_icon=":crossed-swords:")
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Functions
# open_and_resize_image: takes the path to an image, opens it, and resizes it to fit our app's GUI.
# Returns the resized image
@st.cache_data
def open_and_resize_image(photo_path):
    im = Image.open(photo_path)
    new_im = im.resize((350, 250))
    # Not sure if we need to close this to be honest. Better safe than sorry.
    im.close()
    return new_im
# -----------------------------------------------------------------------------------
# GUI Output
st.title("Head to Head")

t1, t2, t3 = st.columns(3)

with t1:
    # Select which team to view
    choose_t1 = st.selectbox(
        label="**Choose a Team**", options=st.session_state.teamsAtEvent, key='t1'
    )

    # Display team's photo
    team_photo = open_and_resize_image(st.session_state.FRC_Teams_dict[choose_t1].photo_path)
    st.image(image=team_photo)

    # Display most relevant pit scouting stats
    st.write("%s lbs. | D-Train: %s | D-Motors: %s" % (st.session_state.FRC_Teams_dict[choose_t1].weight,
                                                       st.session_state.FRC_Teams_dict[choose_t1].drivetrain,
                                                       st.session_state.FRC_Teams_dict[choose_t1].drive_motors))
    # Display most relevant stand scouting stats
    st.write("Auto: Max Speaker: %s | Max Amp: %s" % (st.session_state.FRC_Teams_dict[choose_t1].a_max_speaker,
                                                      st.session_state.FRC_Teams_dict[choose_t1].a_max_amp))
    st.write("Auto: Avg Speaker: %s | Avg Amp: %s" % (round(st.session_state.FRC_Teams_dict[choose_t1].a_avg_speaker, 2),
                                                      round(st.session_state.FRC_Teams_dict[choose_t1].a_avg_amp, 2)))
    st.write("Tele: Max Speaker: %s | Max Amp: %s" % (st.session_state.FRC_Teams_dict[choose_t1].t_max_speaker,
                                                      st.session_state.FRC_Teams_dict[choose_t1].t_max_amp))
    st.write("Tele: Avg Speaker: %s | Avg Amp: %s" % (round(st.session_state.FRC_Teams_dict[choose_t1].t_avg_speaker, 2),
                                                      round(st.session_state.FRC_Teams_dict[choose_t1].t_avg_amp, 2)))
    st.write("Climbs: %s/%s | Traps: %s/%s" % (len(st.session_state.FRC_Teams_dict[choose_t1].climb_matches),
                                len(st.session_state.FRC_Teams_dict[choose_t1].matches),
                                len(st.session_state.FRC_Teams_dict[choose_t1].trap_matches),
                                len(st.session_state.FRC_Teams_dict[choose_t1].matches)))
    

with t2:
    # Select which team to view
    choose_t2 = st.selectbox(
        label="**Choose a Team**", options=st.session_state.teamsAtEvent, key='t2'
    )

    # Display team's photo
    team_photo = open_and_resize_image(st.session_state.FRC_Teams_dict[choose_t2].photo_path)
    st.image(image=team_photo)

    # Display most relevant pit scouting stats
    st.write("%s lbs. | D-Train: %s | D-Motors: %s" % (st.session_state.FRC_Teams_dict[choose_t2].weight,
                                                       st.session_state.FRC_Teams_dict[choose_t2].drivetrain,
                                                       st.session_state.FRC_Teams_dict[choose_t2].drive_motors))
    # Display most relevant stand scouting stats
    st.write("Auto: Max Speaker: %s | Max Amp: %s" % (st.session_state.FRC_Teams_dict[choose_t2].a_max_speaker,
                                                      st.session_state.FRC_Teams_dict[choose_t2].a_max_amp))
    st.write("Auto: Avg Speaker: %s | Avg Amp: %s" % (round(st.session_state.FRC_Teams_dict[choose_t2].a_avg_speaker, 2),
                                                      round(st.session_state.FRC_Teams_dict[choose_t2].a_avg_amp, 2)))
    st.write("Tele: Max Speaker: %s | Max Amp: %s" % (st.session_state.FRC_Teams_dict[choose_t2].t_max_speaker,
                                                      st.session_state.FRC_Teams_dict[choose_t2].t_max_amp))
    st.write("Tele: Avg Speaker: %s | Avg Amp: %s" % (round(st.session_state.FRC_Teams_dict[choose_t2].t_avg_speaker, 2),
                                                      round(st.session_state.FRC_Teams_dict[choose_t2].t_avg_amp, 2)))
    st.write("Climbs: %s/%s | Traps: %s/%s" % (len(st.session_state.FRC_Teams_dict[choose_t2].climb_matches),
                                len(st.session_state.FRC_Teams_dict[choose_t2].matches),
                                len(st.session_state.FRC_Teams_dict[choose_t2].trap_matches),
                                len(st.session_state.FRC_Teams_dict[choose_t2].matches)))

with t3:
    # Select which team to view
    choose_t3 = st.selectbox(
        label="**Choose a Team**", options=st.session_state.teamsAtEvent, key='t3'
    )

    # Display team's photo
    team_photo = open_and_resize_image(st.session_state.FRC_Teams_dict[choose_t3].photo_path)
    st.image(image=team_photo)

    # Display most relevant pit scouting stats
    st.write("%s lbs. | D-Train: %s | D-Motors: %s" % (st.session_state.FRC_Teams_dict[choose_t3].weight,
                                                       st.session_state.FRC_Teams_dict[choose_t3].drivetrain,
                                                       st.session_state.FRC_Teams_dict[choose_t3].drive_motors))
    # Display most relevant stand scouting stats
    st.write("Auto: Max Speaker: %s | Max Amp: %s" % (st.session_state.FRC_Teams_dict[choose_t3].a_max_speaker,
                                                      st.session_state.FRC_Teams_dict[choose_t3].a_max_amp))
    st.write("Auto: Avg Speaker: %s | Avg Amp: %s" % (round(st.session_state.FRC_Teams_dict[choose_t3].a_avg_speaker, 2),
                                                      round(st.session_state.FRC_Teams_dict[choose_t3].a_avg_amp, 2)))
    st.write("Tele: Max Speaker: %s | Max Amp: %s" % (st.session_state.FRC_Teams_dict[choose_t3].t_max_speaker,
                                                      st.session_state.FRC_Teams_dict[choose_t3].t_max_amp))
    st.write("Tele: Avg Speaker: %s | Avg Amp: %s" % (round(st.session_state.FRC_Teams_dict[choose_t3].t_avg_speaker, 2),
                                                      round(st.session_state.FRC_Teams_dict[choose_t3].t_avg_amp, 2)))
    st.write("Climbs: %s/%s | Traps: %s/%s" % (len(st.session_state.FRC_Teams_dict[choose_t3].climb_matches),
                                len(st.session_state.FRC_Teams_dict[choose_t3].matches),
                                len(st.session_state.FRC_Teams_dict[choose_t3].trap_matches),
                                len(st.session_state.FRC_Teams_dict[choose_t3].matches)))

# -----------------------------------------------------------------------------------
# To-Do List
# - maybe make it a chart at the bottom? kinda messy looking right now
# - open and resize image should go into its own file