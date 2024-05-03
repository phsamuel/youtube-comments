Name: Annie Vu
Code File: gephi_cocommenter_network
Date: 05/01/2024


DESCRIPTION:

The following instructions will help you setup, run, and operate the "gephi_cocommenter_network" 
script for the project
__________________________________________________________________________________________________________

INSTALL PYTHON:

If Python isn't already installed on your system
1. Download Python from python.org
2. Run the installer. Ensure you check "Add Python to PATH" before clicking "Install Now"
__________________________________________________________________________________________________________

INSTALL AND SET UP VISUAL STUDIO CODE:

1. Follow the following link to download Visual Studio Code and all of the necessary extensions
	a. https://code.visualstudio.com/docs/python/python-quick-start
__________________________________________________________________________________________________________

INSTALL GEPHI:

1. Follow the following link to download Gephi
	a. https://gephi.org/users/download/
__________________________________________________________________________________________________________

RUN THE PROGRAM:

1. Open Visual Studio Code
2. Open the script "gephi_cocommenter_network" from your File Explorer and open in VS Code
3. Define the number of videos to process on Line 75
4. Run the script by pressing the play button ▷ on the top right 
__________________________________________________________________________________________________________

VISUALIZE THE GRAPH IN GEPHI:

1. Open Gephi and Create a New Project:
	a. Launch Gephi and select File > New Project to start a new graph project
2. Import the CSV Files by going to the Data Laboratory tab at the top
	a. Import Nodes:
		i. Go to the Nodes tab at the top left and then click the Import Spreadsheet tab
		ii. Navigate to the YouTube Files folder and select .csv as file type
		iii. Choose cocommenter_nodes.csv as the file to import
		iv. Configure the import settings if necessary (usually, default is good)
		v. Select "Append to existing workspace" and the Graph Type "Undirected"
	b. Import Edges:
		Repeat the import process for cocommenter_edges.csv
3. View the graph by going to the Overview tab at the top
4. Configure the Graph:
	a. Apply a layout. Go to the Layout section and choose an algorithm (Force Atlas 2 or Yifan Hu) to 
	   spatially distribute nodes in a visually pleasing manner
	b. Adjust the settings such as gravity, repulsion, and distances to get a clear visualization
5. Style the Graph:
	a. Use the Appearance panel to change the color of the nodes and edges 
	b. You can color nodes differently for videos and commenters, adjust sizes, and more to enhance 
	   readability and insights
	c. Under Appearance -> Nodes -> Unique: 
		a. Click on the color box and drag top the color you want the nodes to be
		b. Click "Apply"
6. Explore and Analyze:
	a. Utilize Gephi's tools like Statistics to calculate network metrics like betweenness centrality, 
	   modularity, etc
	b. Explore the graph interactively in the overview and preview panes


