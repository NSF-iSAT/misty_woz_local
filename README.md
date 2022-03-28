# misty_woz_local
Lightweight, offline Misty II controller for iSAT wizard-of-Oz experiment setups.

## usage
`python3 misty_ui.py`

or, from the home directory on the iSAT Linux machine:
`python3 Desktop/misty_woz_local/misty_ui.py`

Running the script will launch a window to scan for Mistys on the local network --- you can click on the profile that comes up after the scan completes. Alternatively, if you know Misty's IP already, you can enter it in the text box. You can get the IP on the local network by connecting to Misty via the Misty app (requires Bluetooth and location services) on iOS or Android.

__Note__: if the scan window cannot find Misty after 1-2 scans, try restarting Misty.

Note that your computer must be on the same network as Misty (**UCB Wireless** by default; this can also be changed via the Misty app if necessary).
