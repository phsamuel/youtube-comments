Name: Annie Vu
Code File: Scheduled YouTube Video Comments
Date: 05/01/2024


DESCRIPTION:

The following instructions will help you setup, run, and operate the "Scheduled YouTube Video Comments" 
script for the project
__________________________________________________________________________________________________________

SET UP GOOGLE API ACCESS:

1. Create a Google Cloud Project:
	a. Go to the Google Cloud Console
	b. Sign in with your Google account
	c. Click on "Select a project" at the top, then "New Project", and follow the prompts to create a 
	   new project
2. Enable the YouTube Data API v3:
	a. In your new project, navigate to "Library" in the left sidebar
	b. Search for "YouTube Data API v3" and select it
	c. Click "Enable" to activate the API for your project
3. Create Credentials:
	a. In the API dashboard, go to "Credentials" on the left sidebar
	b. Click "Create Credentials" at the top
	c. Choose "API key". This will create a new API key you can use to access the YouTube API
	d. Note down the API key; you'll need to insert this into your script
__________________________________________________________________________________________________________

INSTALL PYTHON:

If Python isn't already installed on your system:
1. Download Python from python.org
2. Run the installer. Ensure you check "Add Python to PATH" before clicking "Install Now"
__________________________________________________________________________________________________________

INSTALL AND SET UP VISUAL STUDIO CODE:

1. Follow the following link to download Visual Studio Code and all of the necessary extensions
	a. https://code.visualstudio.com/docs/python/python-quick-start
__________________________________________________________________________________________________________

RUN THE PROGRAM:

1. Open Visual Studio Code
2. Open the script "Scheduled YouTube Video Comments" from your File Explorer and open in VS Code
3. Install Google API Python Client and Other Libraries. In the terminal, run:
	a. pip install google-api-python-client pytz
4. Replace the placeholder in your script with your actual API key where it says api_key = "YOUR_API_KEY"
   in line 31
5. Edit the Search Phrase, Max Search Results, and results order under line 84
6. Install Google API Python Client and Other Libraries. In the terminal, run:
	a. pip install google-api-python-client pytz
7. Run the script by pressing the play button ▷ on the top right 

** The script does not sleep consistently. If it catches the API limit and sleeps, let it continue to run 
   until it stops. Once the script has reached the daily  API limit and stops running, run the script the 
   next day. YouTube API Limit resets everyday at 2:00 AM CDT.
