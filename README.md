# unifiedcopypasteserver
Python implementation of the server for Unified Copy Paste (daemon included as submodule) - I originally started with Rust's rocket, but realized the pain of development far outweighed the cool factor, so I re-wrote it in Python. Features nice websocket connections to each clipboard, and a nicer looking interface than before. See the readme for the daemon for more information.

# Compatibility
Currently, the daemon only works with Linux machines running the X11 windowing system.

The web page has been written with touch-screen devices in mind, which was the original use case - I wanted to write a program that would let me send links back and forth between my phone and my computer without having to email myself everytime. 

# Installation
Clone this repository, install python and create a virtual enviornment with `python -m venv env`. Activate the virtual enviornment with `source env/bin/activate`. Install of the required libraries for the python server with `pip install -r requirements.txt`. The frontend code is already built.

An example systemd unit is included in `scripts/`. 

# TODO
- Desktop notifications from webpage
- Windows support
- Mac support (don't count on it)
- Authentication / password protection
- Some strings cannot be copied, figure that out
- Install script
