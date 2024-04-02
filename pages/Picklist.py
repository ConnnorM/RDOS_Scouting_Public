# Picklist
    # This page will display our picklist and a streamlined view of relevant stats.
# -----------------------------------------------------------------------------------
# Imports
# streamlit: creates our GUI: https://docs.streamlit.io/library/api-reference
import streamlit as st
# pandas: allows easy manipulation of a dataset by loading into dataframes
import pandas as pd
# altair: lets us make nice charts and graphs
import altair as alt
# st_aggrid: lets us make editable charts using Streamlit (pip install streamlit-aggrid)
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Global Variables
# Set the default configuration for our GUI
st.set_page_config(page_title="RDOS Scouting", layout="wide", page_icon=":handshake:")
# Keep track of the next rank to add when adding a team
if 'rank_overall' not in st.session_state:
    st.session_state.rank_overall = 1
# The list of columns for the overall picklist
overall_cols = ['Rank',
                'Team', 
                'A| M_Spk', 
                'A| Avg_Spk',
                'T| M_Spk', 
                'T| Avg_Spk',
                'T| M_Amp', 
                'T| Avg_Amp',
                'Avg Cycles',
                'Climb',
                'Trap',
                'No Show',
                'Broke',
                'Drive',
                'Motor']
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Functions
# create_overall_df: Creates a dataframe for the overall picklist. Returns the dataframe.
# This is in a function so that we can use the st.cache_data decorator on it, which
# makes sure that we don't recreate our dataframe every time we add/remove a team
@st.cache_data
def create_overall_df():
    gryffingear = [[0,
                    5012, 
                    9,
                    9,
                    45,
                    45,
                    45,
                    45,
                    90,
                    '10/10',
                    '10/10',
                    '0/10',
                    '0/10',
                    'I am Speed',
                    'Kachoww']]
    pl_overall_df = pd.DataFrame(data=gryffingear, columns=overall_cols)
    return pl_overall_df

# reorder_ranks: Reassigns ranks to the teams on our picklist
# Made this a function since we need this more than once in our code.
def reorder_ranks():
    for val in range(st.session_state.pl_overall_df.shape[0]):
            st.session_state.pl_overall_df.loc[val, 'Rank'] = val

# -----------------------------------------------------------------------------------
# Main Code
# NEEDS SOME SORT OF TEXTBOX FOR COMMENTS TOO!!!!
pl_overall_df = create_overall_df()

# Add the dataframe to our session state so we don't keep deleting it
if 'pl_overall_df' not in st.session_state:
    st.session_state.pl_overall_df = pl_overall_df

add_team_overall, remove_team_overall, empty_col = st.columns([0.15, 0.15, 0.7])
with add_team_overall:
    # Make a selection box to add a team
    add_team = st.selectbox(
        label="**Add a Team**", options=st.session_state.teamsAtEvent, index=None
    )

    # If the team isn't already on the list, add it to the dataframe
    if add_team != None:
        team = st.session_state.FRC_Teams_dict[add_team]
        if team.num not in st.session_state.pl_overall_df['Team'].unique():
            # Don't divide by 0 if they haven't played a match
            avg_total_cycles = 0
            if len(team.matches) != 0:
                avg_total_cycles = round(sum(team.cycles) / len(team.cycles), 2)

            row = [[st.session_state.pl_overall_df.shape[0],
                team.num, 
                team.a_max_speaker,
                round(team.a_avg_speaker, 2),
                team.t_max_speaker,
                round(team.t_avg_speaker, 2),
                team.t_max_amp,
                round(team.t_avg_amp, 2),
                avg_total_cycles,
                str(len(team.climb_matches)) + '/' + str(len(team.matches)),
                str(len(team.trap_matches)) + '/' + str(len(team.matches)),
                str(len(team.no_show_matches)) + '/' + str(len(team.matches)),
                str(len(team.broken_matches)) + '/' + str(len(team.matches)),
                team.drivetrain,
                team.drive_motors]]
            
            # Create a temporary dataframe for the data and add it to the main dataframe
            temp_df = pd.DataFrame(row, columns=overall_cols)
            st.session_state.pl_overall_df = pd.concat([st.session_state.pl_overall_df, temp_df], axis=0, ignore_index=True)
            # st.session_state.rank_overall += 1
            reorder_ranks()
        
with remove_team_overall:
    # Add a selection box to remove a team
    remove_team = st.selectbox(
        label="**Remove a Team**", options=st.session_state.teamsAtEvent, index=None
    )

    # If the team is on the list, remove it
    if remove_team in st.session_state.pl_overall_df['Team'].unique():
        st.session_state.pl_overall_df = st.session_state.pl_overall_df[st.session_state.pl_overall_df['Team'] != remove_team]
        # Since we removed a team, reset the index (we base the rankings off of index)
        st.session_state.pl_overall_df.reset_index(drop=True, inplace=True)
        # Since we removed a team, recalculate rankings
        reorder_ranks()

# Print the overall picklist dataframe
# st.dataframe(st.session_state.pl_overall_df)
        
# Create GridOptionsBuilder object. This allows us to specify certain options for
# our picklist's AgGrid
gb = GridOptionsBuilder()

# Set default attributes for all columns
gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,

)

#Configure each column individually
gb.configure_column(field="Rank", width=90, type=["numericColumn"], rowDrag=True)
gb.configure_column(field="Team", width=70, type=["numericColumn"])
gb.configure_column(field="A| M_Spk", width=90, type=["numericColumn"])
gb.configure_column(field="A| Avg_Spk", width=100, type=["numericColumn"])
gb.configure_column(field="T| M_Spk", width=90, type=["numericColumn"])
gb.configure_column(field="T| Avg_Spk", width=100, type=["numericColumn"])
gb.configure_column(field="T| M_Amp", width=95, type=["numericColumn"])
gb.configure_column(field="T| Avg_Amp", width=105, type=["numericColumn"])
gb.configure_column(field="Avg Cycles", width=100, type=["numericColumn"])
gb.configure_column(field="Climb", width=75)
gb.configure_column(field="Trap", width=70)
gb.configure_column(field="No Show", width=90)
gb.configure_column(field="Broke", width=75)
gb.configure_column(field="Drive", width=110)
gb.configure_column(field="Motor", width=80)

#makes tooltip appear instantly
gb.configure_grid_options(tooltipShowDelay=0, rowDragManaged=True)
gb.configure_selection(selection_mode = 'multiple', use_checkbox=True)
go = gb.build()

st.write(st.session_state.pl_overall_df)
# output_grid = AgGrid(st.session_state.pl_overall_df, 
                    #  gridOptions=go,
                    # #  As far as I can tell, setting GridUpdateMode to Manual is the only way to save
                    # # the state of the grid when we reorder rows in the GUI
                    #  update_mode=GridUpdateMode.MANUAL,
                    # #  Not entirely sure if this option is necessary.
                    #  data_return_mode=DataReturnMode.FILTERED_AND_SORTED)

# Create a button to save any changes made to the grid via the GUI to our
# session state so that it persists
# if st.button(label=":blue[Save and Fix Ranks]"):
#     # This saves the grid's changes to our session_state so when we update we see the new grid
#     st.session_state.pl_overall_df = output_grid.data
#     # Reassigns values to the Rank column based on order in the grid
#     reorder_ranks()
#     # Not sure why, but it doesn't rerun unless we call it manually here.
#     st.rerun()

# st.info("NOTE 1: After reordering teams, press 'Update' above the chart AND THEN press 'Save and Fix Ranks'")
# st.info("NOTE 2: After removing a team, erase the team number from the selection box.")

