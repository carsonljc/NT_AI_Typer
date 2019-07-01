# automated_typer

This is an AI for NitroType and similar browser games.
The script reads in WS messages and filters it for the typing text.
It will automatically type the text out based on user input speed.

Speed and accuracy can be randomized using a standard deviation to avoid detection.

Script is meant to be a proof of concept and not a means to actively gain the system.

## Setup
Python plugins needed:
    pyautogui
    pychome

### Windows:

#### Installing required python modules:
    1. Open cmd line
    2. Run:
    > pip install <module_name>
    3. If pip does not work that means it may not be part of path variable.
    4. Run in cmd line:
    > setx PATH "%PATH%;<path to pip.exe>



#### Chrome will also have to be configured:
    1. Open cmdline and cd to directory with chrome.exe
    2. Ensure that no other chrome windows are open.
    3. Run
> start chrome --remote-debugging-port=9222
    4. If this chrome instance is ever closed you will have to restart the steps from beginning. 




#### Instructions to run:
    1. Execute program typer.py
    2. As soon as page is loaded, click the window so it becomes your active window
    3. You are all done, moving mouse may cause a failsafe to activate - and stopping the system.s
