# Power-Tracker

This Python script monitors the power state of a computer and sends email notifications to a specified email address upon power on, power off, restart, graceful shutdown, forced shutdown, and abnormal termination.

## Features:

- Monitors the power state of the computer and sends email notifications on state changes
- Detects if the computer was restarted or shut down gracefully or forcefully
- Logs the start and end time of the script in a text file
- Sends the text file as an attachment in the email notifications
- Handles graceful and forced shutdowns, as well as abnormal termination of the script
- Uses the Gmail and Mail.ru SMTP servers to send email notifications

## Usage:

1. Download and install Python on your computer using the [official Python website](https://www.python.org/downloads/). Make sure that Python is installed by opening the command prompt (WIN + R, type cmd) and typing `python`.

2. Install the required packages by opening the terminal in the script folder and running the command: 

```python 
python -m pip install -r requirements.txt
```

3. Convert the script to an executable file without console using the command: 

```python
pyinstaller --noconsole --onefile script.py
```

4. Navigate to the "Dist" folder and find the executable file. To add the script to the autostart, follow these steps:

   1. Press WIN + R and type "shell:startup".
   2. Copy the executable file to the opened directory.
   3. Right-click on the file, select "Properties", click on the "Security" tab, click on "Edit", click on "Add", type "Default User" and click "Check Names", click "OK", select "Full Control", click "Apply", click "OK", and then click "OK" again.


## About:

This script is designed to help you monitor the power state of your computer and receive email notifications when the state changes. If you have any questions or feedback, please feel free to open an issue or pull request on the project's GitHub page.
