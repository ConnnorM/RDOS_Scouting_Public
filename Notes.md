# RDOS Scouting System 2024
**Todo-List:**
- get my frc authorization key into the authorization.txt file so i can make the repo public
- just change event code in one place and have it read it everywhere
- gotta do all the data cleaning first or stuff breaks :(
- teams w/ wrong num matches isn't accurate, says it should always be 9 (I think i hard coded that in to be fair)
- make separate branch or version for dev and what everyone can see (remove picklist mostly)
- need a picklist tab, we give it the numbers in order and it gives us some output idk what yet
    - drag and drop rows
    - save changes to session state (not super important tho)
    - need somewhere to add in comments
    - cross off teams as they're picked (add check column)
    - it tries to remove/add teams when you do the other command cuz the whole thing runs again
        - ignore this for now, i need to think about how to do this more
    - picklist only dies on reboot... which should be ok?
- toggle all off button on graphs
- Try median and mode for some stats
    - Average just isn't very good here. Lots of teams have matches where they only do speaker or amp. looking at avg. cycles (either speaker or amp) helps
    - Research when to use these stats instead of averages and max/min
- Filter on last 4 matches
    - Excluding broken matches?
- Fix auto and teleop shooting maps
    - No idea how to as of right now :/
- Add red/blue side stats (auto and tele, since vision tracking seems to be wonky for lots of people)
- add cycles data to head-to-head
    - take another look at stuff for this page
- Make match summary page
    - see to-do list on that page
- Clean up all the code and comment it more etc.
    - ALL calculations need to be done in FRC_Team. Nothing elsewhere. cuts down on divide by 0 checks and stuff
        - i think the only one left is cycles actually
    - need to try to populate data for all teams at event, then in frc team if they have no entries, use default values
- CSS for streamlit to pretty it up
- Create the scouting form with a separate, locally downloaded phone app
    - barcode scanner seems dumb, but the more I think about it the more I like it
        - https://www.geeksforgeeks.org/how-to-make-a-barcode-reader-in-python/
- Homepage before we give it to other teams
    - This app has to be 110% ready and tested before we give it to other people
    - It's gotta be really really good and clean if people are gonna rely on it
- Guide on how to use it and read it all
    - youtube videos might be better than a doc
- Discord server they can join to ask questions and give feedback?
    - QR codes we pass out at events that link to homepage
- Add to public github RDOS
**Setup Virtual Environment:**
- Instructions from Streamlit: https://docs.streamlit.io/get-started/installation/command-line
- Once it has been set up, use this command to activate the virtual environment
    - Mac: source .venv/bin/activate
**FRC API Docs**
- https://frc-api-docs.firstinspires.org/#authorization
**Altair Links**
- https://altair-viz.github.io/user_guide/encodings/index.html#encoding-data-types
**Streamlit Links**
- API: https://docs.streamlit.io/library/api-reference
- Emoji Shortcodes: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
**Connect Python to Google Sheets**
- Tutorial: https://www.youtube.com/watch?v=82DGz7IxW7c
    - Don't forget to share your Google Sheets with the Google Cloud service
**Switching Events**
- Change the event code in Statsheet:
    - In the 4 url global variables
    - In the stand/pit responses google sheet names
    - Photo filepath in get_team_photo_filenames
- Change the event code in FRC_Team:
    - Photo filepath in self.photo_path
- Change the event code in Data_Cleaning:
    - teamPhotosFolderPath in get_photos_taken_list
- Don't forget to share the new Google Sheets with: 
    - google-drive-scouting-24@scouting-form-413106.iam.gserviceaccount.com
        - NOTE: This email is different for each person. See "Connect Python to Google Sheets" tutorial above.