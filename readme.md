# Adaptive Rainbird Irrigation
## Quickstart

To get started with the Adaptive Rainbird Irrigation system, follow these steps:

### Download the Repository
1. Go to the GitHub page of the project.
2. Navigate to the 'Releases' section.
3. Find the latest release and download the `.zip` file available under 'Assets'.
4. Extract the contents of the zip file to a folder of your choice.

### Configuration
1. Inside the extracted folder, locate the `config.py` file.
2. Open `config.py` with a text editor and configure the following:
   - **MAC Address**: Enter the MAC address of your Netatmo rain gauge.
   - **Rainbird Controller IP**: Specify the local IP address of your Rainbird controller.
   - **Rainbird Password**: Enter the password for your Rainbird controller.
3. Personalize the base irrigation times, zone schedules, and seasonal adjustments in the `config.py` file according to your irrigation setup.

### Install Python and Prerequisites
1. Download and install Python 3.12.2 from the official [Python website](https://www.python.org/downloads/). During installation, make sure to select the option to "Add Python to PATH".
2. Open a terminal or command prompt in the directory where you extracted the repository:
   - **Windows**: You can open a command prompt in the folder by typing 'cmd' in the folder's address bar and pressing Enter.
   - **macOS/Linux**: Right-click in the folder and select 'Open in Terminal' or 'Open in Terminal here'.
3. Install the required Python packages by running the following command:
```bash
python -m pip install -r requirements.txt
```
### Running the Script
To run the script, use the terminal or command prompt to navigate to the directory containing script.py, and execute the following command:
```bash 
python script.py
```