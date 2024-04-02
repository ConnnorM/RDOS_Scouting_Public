# Graphs
    # This page will display graphs that compare all of the teams at the event.
# -----------------------------------------------------------------------------------
# Imports
# streamlit: creates our GUI: https://docs.streamlit.io/library/api-reference
import streamlit as st
# pandas: allows easy manipulation of a dataset by loading into dataframes
import pandas as pd
# altair: lets us make nice charts and graphs
import altair as alt
# math: lets us do... math
import math
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Global Variables
# Set the default configuration for our GUI
st.set_page_config(page_title="RDOS Scouting", layout="wide", page_icon=":bar-chart:")
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Functions
@st.cache_data
def filter_teams(rankings_df, team_checkboxes):
    # copy the original dataset
    filtered_df = rankings_df.copy()
    # loop through each index in team_checkboxes list. If that checkbox is false,
    # remove that entry from our filtered dataframe
    i = 0
    while i < len(team_checkboxes):
        if team_checkboxes[i] == False:
            filtered_df.drop(index=[i], inplace=True)
        i = i + 1
    return filtered_df

# -----------------------------------------------------------------------------------
# GUI Output
st.title("Graphs")

filter_col_1, filter_col_2, graphs_col = st.columns([.1, .1, .8])

with filter_col_1:
    st.write("**Filter Teams**")

# Create a checkbox for each team so we can filter it out if it gets deselected
team_checkboxes = []
# Figure out what indexes we stop at for each column
col_2_max = len(st.session_state.standScoutedTeamsList)
col_1_max = math.ceil(col_2_max / 2)

# Make all our checkboxes, once we show half our teams, put the checkboxes in column 2
cb_ind = 0
for team in sorted(st.session_state.standScoutedTeamsList):
    if cb_ind < col_1_max:
        with filter_col_1:
            cbox = st.checkbox(label=str(team), value=True)
            team_checkboxes.append(cbox)
    else:
        with filter_col_2:
            cbox = st.checkbox(label=str(team), value=True)
            team_checkboxes.append(cbox)
    cb_ind = cb_ind + 1

# If a team has been deselected, don't show them in the data
st.session_state.chart_data = filter_teams(st.session_state.rankings_df, team_checkboxes)

with graphs_col:
    choose_y_axis_1 = st.selectbox(
        label="**Choose Metric**", options=list(st.session_state.rankings_df.columns), index=1, key='y1'
    )
    # Create our first graph
    chart = (
            alt.Chart(st.session_state.chart_data)
            .mark_bar()
            .encode( 
                alt.X("Team Number:O", sort='y'),
                alt.Y(choose_y_axis_1, axis=alt.Axis(grid=False)),
                color=alt.condition(alt.datum['Team Number'] == 0, alt.value('red'), alt.value('blue'))
            )
    )
    # Display the graph
    st.altair_chart(chart, use_container_width=True)

    choose_y_axis_2 = st.selectbox(
        label="**Choose Metric**", options=list(st.session_state.rankings_df.columns), index=2, key='y2'
    )

    # Create our second graph
    chart = (
            alt.Chart(st.session_state.chart_data)
            .mark_bar()
            .encode( 
                alt.X("Team Number:O", sort='y'),
                alt.Y(choose_y_axis_2, axis=alt.Axis(grid=False)),
                color=alt.condition(alt.datum['Team Number'] == 0, alt.value('red'), alt.value('blue'))
            )
    )
    # Display the graph
    st.altair_chart(chart, use_container_width=True)

st.info("Note: Team 0 represents the competition average. This average does not include teams with a 0 value. We only want to compare teams that have data for the task in question.")

# -----------------------------------------------------------------------------------
# To-Do List
# - maybe add more stats to compare? i think it's fine for right now though
# - so uh. altair can filter data: https://altair-viz.github.io/user_guide/transform/filter.html
    # - so maybe get rid of my filter and do it this way :/