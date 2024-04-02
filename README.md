# RDOS Scouting System 2024
## View the App
- WARNING: This repo as is will not run the app. There is no FRC API key, Google Cloud credentials file, or virtual environment in this repo. You'll have to make your own using the instructions in this README file.
- Visit: https://rdos-scouting-2024.streamlit.app/ to view the current version of the app
    - NOTE: This repo will only be updated before competitions or when requested. So, it may be outdated compared to what you see at the link above
## Getting the App Running Locally
- Clone the repo from GitHub
- Use Google Cloud services to allow you to access your Google Drive account via code
    - Instruction Video: https://www.youtube.com/watch?v=82DGz7IxW7c
- In the Helpers/Data_Setup.py file, replace this email "google-drive-scouting-24@scouting-form-413106.iam.gserviceaccount.com" with the one you got from the video above.
- Open your Google Sheets file and share the sheet with that same email (you probably already did this while watching the video)
- In the video, you also downloaded a credentials.json file (or named something similar)
    - Add that file to the Setup folder and rename it to "scout_creds.json"
- See "Switching Events" in Notes.md file for all of the locations where you need to change a variable when reading in data from a different Google Sheet
- Make an account with the FRC API and get your authorization code
    - https://frc-api-docs.firstinspires.org/#authorization
    - Read ALL of the instructions here. They are weird.
- Create an "authorization.txt" file in the root directory (in the main folder created when you cloned from GitHub. Probably called RDOS_Scouting) 
- Add your full FRC API authorization key to this file (and nothing else.)
    - This file should just have one line that looks like: basic EASgsdlkfjlekEfldkjalkdgkjselio==
- Create a virtual environment in the root directory
    - Instructions: https://docs.streamlit.io/get-started/installation/command-line
- Activate the virtual environment
    - Type the following command into your terminal (while in the root directory of the app)
    - source .venv/bin/activate
        - This command is for Mac/Linux, Windows is slightly different. See the instructions above
- Use the requirements.txt file to install all of the Python packages and libraries you need
    - pip install -r requirements.txt
    - When you try to run the program, the terminal output will tell you which packages you are missing (shouldn't ever happen thanks to the virtual environment)
## Running the App
- Open the folder you cloned from GitHub and type the following command in the command line:
    - source .venv/bin/activate
        - starts the virtual environment
    - streamlit run Statsheet.py
        - runs the app
- Statsheet is the sort of main function of the app. You need to run this file first, and Streamlit will look in the /pages folder for other .py files and add them to the app's sidebar
## Running the App on Streamlit Cloud
- Deploying the app to Streamlit cloud is what allows other people to access the app by just clicking a link
- Create an account with Streamlit, login with your GitHub on Streamlit, run your app locally, click "Deploy" in the hamburger menu in the top right, and follow the instructions
    - Just a warning, random stuff will work perfectly fine locally but not work when deployed to the cloud, so you'll need to be ready to find work arounds for certain things
## NOTE
- This repo contains the final version of the app that we used at the OC Regional in 2024. More changes to come!
- P.S. We built this in about 4 weeks during competition season, so please excuse all of the TODO items and hacky solutions to certain problems