# Tapioca

Tapioca enables right click on linux touchscreen devices using technologies like python-evedev, pymouse (PyUserInput) and xdotool.

# Available Gestures

Long press right click and two finger tap right click.

# Installation 

Tapioca has been tested to work on Ubuntu 17.04. Run commands below to install dependencies.

    sudo apt install python-evdev xinput xdotool python-pip 
    sudo pip install PyUserInput  

Download Tapioca from [here](https://github.com/nitg16/tapioca/archive/master.zip) and extract  to a folder.

# Running Tapioca 

Find out your touch panel make by running `xinput` command.

Now run the command below to launch Tapioca. 

    sudo python tapioca.py --device ""

Add the name of your touch panel make within the quotes.

# Configuring Tapioca 

`tapioca.conf` file is located in `~/.config/tapioca/` folder. 

It is automatically created when you run Tapioca for the first time. Your device name is also automatically added to the config file if you use the command mentioned above to run the application.

You can edit settings in `User Settings` in config file. All config options are well commented. 

**It is highly recommended that you review config file at least once.**

# Wayland  support?

Not possible as of now.

# Credits

  * All the developers behind Linux kernel, python-evdev, PyUserInput, pymouse, xdotool and xinput.

  * [Python-Touchscreen-RightClick](https://github.com/Zyell/Python-Touchscreen-RightClick)