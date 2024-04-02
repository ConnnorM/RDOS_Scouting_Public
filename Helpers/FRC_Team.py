# streamlit: creates our GUI: https://docs.streamlit.io/library/api-reference
import streamlit as st
# pandas: allows easy manipulation of a dataset by loading into dataframes
import pandas as pd
# image: allows us to load images into a plot
from matplotlib import image 
# pyplot: allows us to make charts with our data
from matplotlib import pyplot as plt 
# random: lets us pick random numbers
import random
# numpy: does some funky number stuff
import numpy as np

# -----------------------------------------------------------------------------------
# Global Variables
photo_path_folder = './Team_Photos/OC/'
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# FRC_Team: a class that stores all the relevant information pertaining to a team
class FRC_Team:
    def __init__(self, team_num):
        # Initialize default values in the constructor
        self.num = team_num
        self.name = "Electromechanical Porpoises from the Upper Atmosphere"
        self.robot_name = "Pew Pew Shooty Bot"
        self.music = "./Music/Bewegen_is_Gezond.mp3"
        # Pit Scouting Data
        self.weight = 0
        self.length = 0
        self.width = 0
        self.height = 0
        self.under_stage = "No"
        self.scoring_type = "None"
        self.can_intake = "Ground"
        self.pref_intake = "No Intake"
        self.can_climb = "No"
        self.photo_path = photo_path_folder + '5199.jpg'
        self.drivetrain = "Tank"
        self.drive_motors = "Falcon"
        self.batteries = 0
        self.vision = 'No'
        self.important = ""
        self.can_trap = "No"
        self.can_multi_trap = "No"
        # Stand Scouting Data
        self.a_speaker_counts = []
        self.a_max_speaker = 0
        self.a_avg_speaker = 0
        self.a_amp_counts = []
        self.a_max_amp = 0
        self.a_avg_amp = 0
        self.t_speaker_counts = []
        self.t_max_speaker = 0
        self.t_avg_speaker = 0
        self.t_acc_speaker = 0
        self.t_amp_counts = []
        self.t_max_amp = 0
        self.t_avg_amp = 0
        self.t_acc_amp = 0
        self.cycles = []
        self.climb_matches = []
        self.trap_matches = []
        self.multi_trap_matches = []
        self.avg_speed = 0
        self.broken_matches = []
        self.no_show_matches = []
        self.comments = []
        self.entries = pd.DataFrame()
        self.pit_entry = pd.DataFrame()
        self.entries_wo_no_shows = pd.DataFrame()
        self.tele_shooting_locs = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "Total": 0}
        self.auto_notes = []
        self.start_locs = []
        self.taxis = []
        self.auto_pts = []
        self.avg_auto_pts = 0
        self.tele_pts = []
        self.avg_tele_pts = 0
        self.auto_maps = []
        self.shooting_locs_map = []
        self.shots_DF = pd.DataFrame()
        self.points_DF = pd.DataFrame()
        # Stats from API data
        self.matches = []
        self.rank = 1
        self.avg_rp = 0
        self.coop = 0
    # ---------------------------------------------------------------------------------------------
        
    # set_team_attributes: Using the data from stand scouting, pit scouting, and the API, update
    # the FRC_Team object's attributes
    def set_team_attributes(self):
        # Set team name if the team number is valid
        if self.num in st.session_state.team_names_dict:
            # rstrip removes spaces at the end of the string. If there's a space, the
            # bold printing in Streamlit doesn't work :(
            self.name = st.session_state.team_names_dict[self.num][0].rstrip()
            # Assign the robot their actual name
            self.robot_name = self.assign_robot_name()
        else:
            self.name = "I don\'t think that\'s a valid number"
        
        # Assign a music file to the team
        self.music = self.pick_music()
        # First, use defaults if the stand scouting dataframe is empty
        if not st.session_state.stand_DF.empty:
            # Get all scouting entries for this team
            self.entries = st.session_state.stand_DF.loc[st.session_state.stand_DF['Team Number'] == self.num].reset_index(drop = True)
            # Now use defaults if this team has no stand scouting data
            if not self.entries.empty:
                # Get all scouting entries for this team in which they actually showed up to the match.
                    # Makes averages a lot more useful of a statistic
                self.entries_wo_no_shows = self.entries.loc[self.entries['No Show'] == 'No'].reset_index(drop = True)
                # A list of how many speaker shots were made during each autonomous period
                self.a_speaker_counts = self.entries['A: Notes in Speaker'].to_list()
                # The max number of speaker shots made during autonomous
                self.a_max_speaker = max(self.a_speaker_counts)
                # The average number of speaker shots made during autonomous (excludes no-show matches)
                self.a_avg_speaker = self.entries_wo_no_shows.loc[:, 'A: Notes in Speaker'].mean()
                # A list of how many amp shots were made during each autonomous period
                self.a_amp_counts = self.entries['A: Notes in Amp'].to_list()
                # The max number of amp shots made during autonomous
                self.a_max_amp = max(self.a_amp_counts)
                # The average number of amp shots made during autonomous (excludes no-show matches)
                self.a_avg_amp = self.entries_wo_no_shows.loc[:, 'A: Notes in Amp'].mean()
                # A list of how many speaker shots were made during each teleop period
                self.t_speaker_counts = self.entries['T: Speaker Shots Made'].to_list()
                # The max number of speaker shots made during teleop
                self.t_max_speaker = self.entries.loc[:, 'T: Speaker Shots Made'].max()
                # The average number of speaker shots made during teleop (excludes no-show matches)
                self.t_avg_speaker = self.entries_wo_no_shows.loc[:, 'T: Speaker Shots Made'].mean()
                # A list of how many amp shots were made during each teleop period
                self.t_amp_counts = self.entries['T: Amp Shots Made'].to_list()
                # The max number of amp shots made during teleop
                self.t_max_amp = self.entries.loc[:, 'T: Amp Shots Made'].max()
                # The average number of amp shots made during teleop (excludes no-show matches)
                self.t_avg_amp = self.entries_wo_no_shows.loc[:, 'T: Amp Shots Made'].mean()
                # The accuracy of the bot's speaker shots during teleop
                self.set_speaker_tele_acc(self.entries)
                # The accuracy of the bot's amp shots during teleop
                self.set_amp_tele_acc(self.entries)
                # The average drive speed of the robot
                self.avg_speed = self.entries.loc[:, 'Robot Speed'].mean()
                # Determines the bot's preferred intake method (source/ground/etc)
                self.set_pref_intake()
                # Creates of lists of which matches in which the robot performed certain actions
                self.set_matches_lists()
                # A list of the number of cycles the robot made in each match teleop
                self.set_cycles()
                # Creates a dictionary of the robot's preferred shooting locations in teleop
                self.set_tele_shooting_locs()
                # Creates a dictionary of each match played and what notes the bot picked up in auton
                self.set_auto_notes()
                # Creates a list of the robot's starting locations for each match
                self.set_start_locs()
                # Creates a list of the amount of points scored in auto in each match
                self.set_auto_pts(self.entries_wo_no_shows)
                # Creates a list of the amount of points scored in teleop in each match
                self.set_tele_pts(self.entries_wo_no_shows)
                # The average points scored in auto and teleop, respectively. Excludes no-show matches
                self.avg_auto_pts = self.calc_list_average(self.auto_pts)
                self.avg_tele_pts = self.calc_list_average(self.tele_pts)
                # For each match, add a map of what the team did in auton to the self.auto_maps list
                # TODO: self.create_auto_maps()
                # Create a map of the robot's preferred shooting locations
                # TODO: self.create_shooting_locs_map()
                # Create the dataframe of teleop shots used for graphing
                self.create_shots_DF()
                # Create the dataframe of points used for graphing
                self.create_points_DF()

        # Get the pit scouting data:
        # Add the path to the robot's photo if we have a photo for it, otherwise it uses the default 5199 photo
        if self.num in st.session_state.photo_filenames_dict.keys():
            self.photo_path = photo_path_folder + st.session_state.photo_filenames_dict[self.num]
        # First, use defaults if the whole pit scouting dataframe is empty
        if not st.session_state.pit_DF.empty:
            self.pit_entry = st.session_state.pit_DF.loc[st.session_state.pit_DF['Team Number'] == self.num]
            # Use defaults if this particular team doesn't have pit scouting data
            if not self.pit_entry.empty:
                self.weight = self.pit_entry['Weight'].values[0]
                self.length = self.pit_entry['Robot Length'].values[0]
                self.width = self.pit_entry['Robot Width'].values[0]
                self.height = self.pit_entry['Robot Height'].values[0]
                # Can the robot drive under the stage?
                self.under_stage = self.pit_entry['Drive Under Stage'].values[0]
                # Can the robot score in the speaker, amp, both, neither?
                self.scoring_type = self.pit_entry['Can Score Notes'].values[0]
                # Does the bot intake from the ground, source, neither, or both?
                self.can_intake = self.pit_entry['Intake Location'].values[0]
                # Can the bot climb and where?
                self.can_climb = self.pit_entry['Climb'].values[0]
                self.can_trap = self.pit_entry['Can Trap'].values[0]
                self.can_multi_trap = self.pit_entry['Multiple Trap'].values[0]
                self.drivetrain = self.pit_entry['Drivetrain Type'].values[0]
                self.drive_motors = self.pit_entry['Drive Motors'].values[0]
                self.batteries = self.pit_entry['Batteries'].values[0]
                self.vision = self.pit_entry['Vision Tracking'].values[0]
                self.important = self.pit_entry['Most Important'].values[0]
    # ---------------------------------------------------------------------------------------------

    # set_speaker_tele_acc: Sets the bot's accuracy in teleop at the speaker
        # We pass in a generic dataframe instead of accessing its own member 
        # in case we want to filter out outliers and pass that new dataframe in
    def set_speaker_tele_acc(self, entries):
        t_speaker_make = entries.loc[:, 'T: Speaker Shots Made'].sum()
        t_speaker_miss = entries.loc[:, 'T: Speaker Shots Missed'].sum()
        t_speaker_taken = t_speaker_make + t_speaker_miss
        if t_speaker_taken != 0:
            self.t_acc_speaker = (t_speaker_make / t_speaker_taken) * 100
        else:
            self.t_acc_speaker = 0

    # set_amp_tele_acc: Sets the bot's accuracy in teleop at the amp
        # We pass in a generic dataframe instead of accessing its own member 
        # in case we want to filter out outliers and pass that new dataframe in
    def set_amp_tele_acc(self, entries):
        t_amp_make = entries.loc[:, 'T: Amp Shots Made'].sum()
        t_amp_miss = entries.loc[:, 'T: Amp Shots Missed'].sum()
        t_amp_taken = t_amp_make + t_amp_miss
        if t_amp_taken != 0:
            self.t_acc_amp = (t_amp_make / t_amp_taken) * 100
        else:
            self.t_acc_amp = 0

    # set_cycles: Makes of list of the number of teleop cycles made in each match
    def set_cycles(self):
        for ind in range(len(self.matches)):
            self.cycles.append(self.t_amp_counts[ind] + self.t_speaker_counts[ind])

    # set_pref_intake: Sets the bot's preferred method of intaking
    def set_pref_intake(self):
        # Uses exception handling because value_counts()['Location'] returns null if 
        # no match is found
        # Get the frequency of each value's appearance as a percentage
        try:
            ground_intake = self.entries['Intake Notes'].value_counts()['Ground'] / self.entries * 100
        except:
            ground_intake = 0
        try:
            source_intake = self.entries['Intake Notes'].value_counts()['Source'] / self.entries * 100
        except:
            source_intake = 0
        try:
            both_intake = self.entries['Intake Notes'].value_counts()['Both'] / self.entries * 100
        except:
            both_intake = 0
        try:
            no_intake = self.entries['Intake Notes'].value_counts()['No Intake'] / self.entries * 100
        except:
            no_intake = 0
        # Create a dictionary of our locations and frequencies
        intake_dict = {'Ground': ground_intake, 'Source': source_intake, 'Both': both_intake, 'No Intake': no_intake}
        # Sort the dictionary in descending order
        intake_dict = dict(sorted(intake_dict.items(), key=lambda item: item[1], reverse = True))
        # Set the highest value as the preferred method
        self.pref_intake = next(iter(intake_dict))
    
    # set_matches_lists: Creates lists of the matches in which a robot performed certain actions
    def set_matches_lists(self):
        # Get all the matches we have entries for in an ordered list
        self.matches = self.entries['Match Number'].to_list()
        self.matches.sort()

        # Get a list of Yes/No values for each match's taxi value
        self.taxis = self.entries['A: Exit Starting Zone'].to_list()

        # Get lists of which matches the bot played, climbed, trapped, broke, etc.
        for i in range(len(self.entries)):
            cur_entry = self.entries.loc[i]
            # Climb
            if cur_entry['S: Climb Locations'] != 0:
                self.climb_matches.append(cur_entry['Match Number'])
            # Trap
            if cur_entry['S: Trap'] != 0:
                self.trap_matches.append(cur_entry['Match Number'])
            # Multi Trap Matches
            if type(cur_entry['S: Trap']) != np.int64:
                self.multi_trap_matches.append(cur_entry['Match Number'])
            # Broken matches
            if cur_entry['Broke'] == 'Yes':
                self.broken_matches.append(cur_entry['Match Number'])
            # No Show matches
            if cur_entry['No Show'] == 'Yes':
                self.no_show_matches.append(cur_entry['Match Number'])
            # Comments
            self.comments.append(cur_entry['Comments'])
    
    # set_tele_shooting_locs: # Creates a dictionary of the robot's preferred shooting locations in teleop
    def set_tele_shooting_locs(self):
        # Loop through each match
        for i in range(len(self.entries)):
            cur_entry = self.entries.loc[i]
            shoot_locs_string = cur_entry['Shooting Locations']
            # If only one location was selected, increment the right location's value
            if type(shoot_locs_string) == int:
                self.tele_shooting_locs[str(shoot_locs_string)] += 1
                self.tele_shooting_locs["Total"] += 1
            # If multiple locations were selected, parse them out and increment each location's value
            else:
                shoot_locs_string = shoot_locs_string.replace(" ", "")
                shoot_locs_list = shoot_locs_string.split(',')
                for loc in shoot_locs_list:
                    if loc != 0:
                        self.tele_shooting_locs[loc] += 1
                        self.tele_shooting_locs["Total"] += 1

    # set_auto_notes: Creates a list of each match played and what notes the bot picked up in auton
    def set_auto_notes(self):
        # Loop through all entries
        for i in range(len(self.entries)):
            # Each match is a new index in the list, and each index stores a list of notes picked up
            cur_entry = self.entries.loc[i]
            # Add the new index as an empty list
            self.auto_notes.append([])
            auto_notes_string = str(cur_entry['A: Notes Picked Up'])
            # Split the string by character and add each one to our list
            for char in auto_notes_string:
                self.auto_notes[i].append(char)
    
    # set_start_locs: Creates a list of the robot's starting locations for each match
    def set_start_locs(self):
        # Loop through all entries
        for i in range(len(self.entries)):
            cur_entry = self.entries.loc[i]
            # If a value was selected, add it to our list
            if type(cur_entry['Starting Location']) == int:
                self.start_locs.append(cur_entry['Starting Location'])
            # The value was left blank, so append 0 instead
            else:
                self.start_locs.append(0)
    
    # set_auto_pts: Creates a list of the amount of points scored in auto in each match
    def set_auto_pts(self, entries):
        # Loop through each match
        for i in range(len(entries)):
            cur_pts = 0
            cur_entry = entries.loc[i]
            # Taxi/Starting line +2
            if cur_entry['A: Exit Starting Zone'] == 'Yes':
                cur_pts += 2
            # Speaker +5
            cur_pts += 5 * cur_entry['A: Notes in Speaker']
            # Amp +2
            cur_pts += 2 * cur_entry['A: Notes in Amp']
            self.auto_pts.append(cur_pts)

    # set_tele_pts: Creates a list of the amount of points scored in teleop in each match
    def set_tele_pts(self, entries):
        # Loop through each match
        for i in range(len(entries)):
            cur_pts = 0
            cur_entry = entries.loc[i]
            # Speaker +2 (assuming no amplification bonus)
            cur_pts += 2 * cur_entry['T: Speaker Shots Made']
            # Amp +1
            cur_pts += 1 * cur_entry['T: Amp Shots Made']
            # Trap +5
            if cur_entry['S: Trap'] != 0:
                # If only one value was input, only 1 trap was scored
                if isinstance(cur_entry['S: Trap'], np.integer):
                    trap_count = 1
                else:
                    # Count the digits in the input (input ex: 2, 1)
                    trap_count = sum(c.isdigit() for c in cur_entry['S: Trap'])
                cur_pts += 5 * trap_count
            # Climb +3 (not including bonus for Spotlight or Harmony)
            if cur_entry['S: Climb Locations'] != 0:
                cur_pts += 3
            # Park +1
            elif cur_entry['S: Park'] == 'Yes':
                cur_pts += 1
            # Add this match's point total to the list
            self.tele_pts.append(cur_pts)

    # calc_list_average: Returns the average value of a list of ints
    def calc_list_average(self, int_list):
        return sum(int_list) / len(int_list)
    
    # creat_auto_maps: Uses the team's starting locations and notes picked up in auto to create plots. 
    # Each chart shows data on one match and is added to the auto_maps list
    # TODO: split this to red/blue side since teams like us might only have one side that is good?
    def create_auto_maps(self):
        # Create the lists of colors and coordinates for starting positions and auton notes
        colors = ['red', 'orange', 'yellow', 'green', 'aqua', 'blue', 'violet', 'purple', 'white']
        starting_positions = [[0, 0],
                            [105, 90],
                            [140, 145],
                            [105, 200],
                            [125, 300]]

        notes_list = [[0, 0],
                    [220, 71],
                    [220, 145],
                    [220, 217],
                    [496, 48],
                    [496, 133],
                    [496, 217],
                    [496, 304],
                    [496, 387]]
        # Read in the blank map image
        data = image.imread('./Field_Maps/auto_map.png') 
    
        # Get how many matches to loop through
        match_count = len(self.start_locs)

        for cur_match in range(match_count):
            # A list that stores each point to plot on the map as a list: [x, y]
            points = []
            # Set up the chart we will make
            fig = plt.figure()
            # Add the coordinates of their starting position
            points.append([starting_positions[self.start_locs[cur_match]][0], 
                    starting_positions[self.start_locs[cur_match]][1]])
        
            # Plot the starting point as a circle first
            plt.plot(starting_positions[self.start_locs[cur_match]][0], 
                starting_positions[self.start_locs[cur_match]][1],
                marker='o', color = 'springgreen', markersize=15)
        
            # For each note they picked up, add that note's coordinates
            for note in self.auto_notes[cur_match]:
                if note != '0':
                    points.append(notes_list[int(note)])
            # Make the map for this match
            next_i = 1
            max_i = len(points)
            for point in points:
                if next_i < max_i:
                    plt.arrow(x=point[0],
                        y=point[1],
                        dx=(points[next_i][0] - point[0]),
                        dy=(points[next_i][1] - point[1]),#cowabunga babyyyyyy
                        width=7, facecolor=colors[next_i-1],linestyle='-',linewidth=2, length_includes_head=True)
                next_i += 1
            plt.imshow(data) 
            plt.axis("off")
            self.auto_maps.append(fig)
            # Close the matplotlib figure. If you don't do this, the program keeps the plot open even though
            # we are done with it, which wastes a ton of memory.
            plt.close()
    
    # create_shooting_locs_map: Creates a plot of the team's preferred shooting locations
    # TODO: this loads really slowly :(
    def create_shooting_locs_map(self):
        text_locs = [[80, 205],
                   [165, 120],
                   [165, 280],
                   [165, 400],
                   [360, 400],
                   [80, 40]]
        colors = ['red', 'orange', 'lime', 'yellow', 'aqua', 'white']
        # Read in the blank map image
        data = image.imread('./Field_Maps/teleop_map.png') 
        # Set up the chart we will make
        fig = plt.figure()
        for ind in range(6):
            plt.text(text_locs[ind][0], text_locs[ind][1], self.tele_shooting_locs[str(ind)], fontsize='xx-large', color=colors[ind], fontweight='extra bold')
        plt.imshow(data) 
        plt.axis("off")  
        self.shooting_locs_map.append(fig)
        # Close the matplotlib figure. If you don't do this, the program keeps the plot open even though
        # we are done with it, which wastes a ton of memory.
        plt.close()

    # create_shots_DF: Creates a dataframe of a team's shots. Mostly just reformats data
    # to make it easier to graph
    def create_shots_DF(self):
        shots = []
        for index, row in self.entries.iterrows():
            shots.append(["Speaker", row["Match Number"], row["T: Speaker Shots Made"]])
            shots.append(["Amp", row["Match Number"], row["T: Amp Shots Made"]])
        self.shots_DF = pd.DataFrame(shots,
                            columns=["Type", "Match Number", "Shots Made"])
        
    # create_points_DF: Creates a dataframe of a team's points per match. Mostly just reformats data
    # to make it easier to graph
    def create_points_DF(self):
        # self.tele_pts self.auto_pts
        pts = []
        for ind in range(len(self.tele_pts)):
            pts.append([self.tele_pts[ind] + self.auto_pts[ind], self.matches[ind]])
        self.points_DF = pd.DataFrame(pts,
                                      columns=["Points", "Match Number"])
    
    # assign_robot_name: sets the team's robot's name
    def assign_robot_name(self):
        # Get the robot name according to the FRC API
        robo_name = st.session_state.team_names_dict[self.num][1]
        # If no name was given:
        if robo_name == "":
            # NOTE: Can't use match and case (switch statements) with 
            # Streamlit Cloud because Streamlit Cloud uses Python 3.9
            # and that syntax came in 3.11 :(
            if self.num == 5199:
                robo_name = "Siren:microphone::mermaid:"
            elif self.num == 5012:
                robo_name = "GryffinGODS"
            elif self.num == 5500:
                robo_name = "Double-Depot"
            elif self.num == 1967:
                robo_name = "We Miss Teddy:pleading_face:"
            elif self.num == 1622:
                robo_name = ":safety_vest::spider:"
            elif self.num == 6833:
                robo_name = "Goated with the sauce"
            else:
                robo_name = self.pick_silly_robot_name()
        return robo_name

    # pick_silly_robot_name: Since nobody actually inputs their robot's name into the FIRST API,
    # we just randomly assign a silly name from a list made by ChatGPT and Josh "Big J" Duncan
    # Returns the silly robot name
    def pick_silly_robot_name(self):   
        names_list = ['BeepBoop Boombox',
                    'Whirligig Whiz',
                    'Clankity Clutz',
                    'Gizmo Galore',
                    'Dynamo Dizzy',
                    'BuzzBot Boogie',
                    'Sparky Shuffle',
                    'Jitterbug Jolt',
                    'Circuitry Clown',
                    'FlutterBot Funk',
                    'WobbleWidget Waltz',
                    'TinkerTwist Tango',
                    'Zappy Zigzag',
                    'Not a Useless Piece of Luggage',
                    'Deadzone',
                    'xXxSharpshooterxXx',
                    'Chug Jug Guzzler',
                    'Amazon TV Firestick',
                    'Martin Shkreli',
                    'SizzleSprint Shuffle',
                    'Gigglebot 3000',
                    'Chuckletron',
                    'Bleepy Blunder',
                    'Sir Bots-a-Lot',
                    'Fumbletron 9000',
                    'Ankle-Biter',
                    'Apriltag ID#4',
                    'Jarius Gladius the 3rd, supreme leader of the jankterian empire',
                    'Alexi Georgiades',
                    'ShkreliBot-Pharma Kingpin Edition',
                    'Kitty Purry',
                    'BARBAQUE BACON BURGER',
                    'Evius the Devious',
                    '*REDACTED*',
                    'Robert Goll',
                    'Quokkas v1.2',
                    'Quokkas v2.5',
                    'Quokkas v4.0',
                    'Quokkas v6.8',
                    'Quokkas v9.3'] 
        
        pre_or_suf_fix_list = ['Maybe it\'s \"$\"',
                               'Probably \"$\" or something',
                               '\"$\"...? Kinda sounds like Fortnite tho:pinata:',
                               'My vote is for \"$\"',
                               'How about \"$\"',
                               '\"$\"...?',
                               'Go! \"$\"!',
                               'I choose you, \"$\"!',
                               '\"$\" would be tough:muscle:',
                               '\"$\"? Nah that was bad',
                               ':fire::fire:\"$\":fire::fire:',
                               '\"$\" is so fire :fire::fire::fire:',
                               '\"$\":skull::skull::skull:',
                               '\"$\":man_in_motorized_wheelchair:',
                               '\"$\" sounds baller:basketball:',
                               '\"$\" mmm yes:pinched_fingers:',
                               'If \"$\" got hit by a bus, I would be driving the bus',
                               'Are you \"$\"? cus I don\'t think you work properly',
                               'Watch out for \"$\"\'s big arms:muscle::muscle::muscle:',
                               'Somebody call 911 \"$\" got that fire burning on the dance florr owowowo',
                               '\"$\" van links naar rechts on van links naar rechts! want bewegend is gezond',
                               '\"$\" just won a Fortnite tournament, let\'s see how they robot',
                               '\"$\" is boutta drop out the Battle Bus',
                               'Winner Winner \"$\" Dinner',
                               '\"$\" puts the double in double depot',
                               '\"$\" is goated with the sauce:spaghetti:',
                               '\"$\" is gonna touch the sky (Heaven cus they are going to break prob:headstone::angel:)',
                               ':speaking_head_in_silhouette::100::speaking_head_in_silhouette:\"$\":fire::fire::speaking_head_in_silhouette:',
                               'You would not believe your eyes, if ten million \"$\" flies',
                               '\"$\" knows Bill Nye',
                               '\"$\" is better than milk',
                               '\"$\" is not in the AutoZone\u2122',
                               '\"$\" is Stryker\'s girlfriend',
                               '\"$\" got waterboarded by Noah',
                               '\"$\" ate a Snickle after AVR',
                               '\"$\" sent Nico to the hospital',
                               'It\'s \"$\". Scott said so']
        name = random.sample(names_list, 1)[0]
        # Grab one random item from the given list. 1 is how many items to return, 0 means get
        # the first item in the list that is returned
        pre_or_suf_fix = random.sample(pre_or_suf_fix_list, 1)[0]
        full_name = pre_or_suf_fix.replace('$', name)
        return full_name
        
    # pick_music: Assigns a music file to the team. Either picks a random song or
    # assigns a predetermined song depending on team number
    def pick_music(self):   
        # Song List
        song_file_path_list = ['Bewegen_is_Gezond.mp3',
                               'Home_Depot.mp3',
                               'Hakuna_Matata.mp3',
                               'Hedwig_Theme.mp3',
                               'Wabbit_Season.mp3']
        # If we have a specific song for that team, assign it:
        if self.num == 5199:
            music_file_path = './Music/' + song_file_path_list[0]
        elif self.num == 5500:
            music_file_path = './Music/' + song_file_path_list[1]
        elif self.num == 6560:
            music_file_path = './Music/' + song_file_path_list[2]
        elif self.num == 5012:
            music_file_path = './Music/' + song_file_path_list[3]
        elif self.num == 7042:
            music_file_path = './Music/' + song_file_path_list[4]
        else:
            # Play the default song
            music_file_path = './Music/' + song_file_path_list[0]
        return music_file_path