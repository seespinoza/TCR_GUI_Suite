# TCR Analysis Tool Suite

This Python script was created as a GUI-graphical wrapper for command-line tools
used to analyze TCR data. Currently this software supports MEME, Circos,and 
TCR-dist.

# REQUIREMENTS

## Operating System:
 - This software has only been tested on Ubuntu and OSX (with 2010 Mac models or newer).
   The Tool Suite should work on other Linux systems.

## Package dependencies
 - This project requires the user install Docker in order to ensure that all package
   dependencies are dealt with before launching the software.

## SOFTWARE INSTALLATION

### Mac Users
1) First you need to install Docker to be able to run the tool suite. Follow
   the steps found on the official Docker website and install Docker: 
   https://docs.docker.com/docker-for-mac/install/

2) Download the github repository. You can do this by runnning `git clone https://github.com/seespinoza/TCR_GUI_Suite.git`

3) Install socat using brew: `brew install socat`. And run this command `socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\"`.
   Install Xquartz using `brew install xquartz` and login and logout of OSX to make sure everything is working correctly.
   Open Xquartz using `open -a Xquartz` and go into the security tab and check "Allow connections from network clients"
   
4) Run the command `ifcongfig en0` and copy the network interface IP. 
   Now run `sudo docker run -e DISPLAY=NETWORK_INTERFACE:0 -v /tmp/.X11-unix:/tmp/.X11-unix -v ~:/home/developer/ seespinoza/memecos:2` and make sure to replace
   NETWORK_INTERFACE with the IP address obtained above.

These steps are better outlined in the following article.
https://cntnr.io/running-guis-with-docker-on-mac-os-x-a14df6a76efc
## Ubuntu Users
 1) Install Docker: https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/#set-up-the-repository

 2) `sudo docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v ~:/home/developer/ seespinoza/memecos:2`
