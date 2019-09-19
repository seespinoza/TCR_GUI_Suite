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

 1) Open the Terminal app and download the GitHub repository by using the following command: `git clone https://github.com/seespinoza/TCR_GUI_Suite.git`

## Ubuntu Users
 1) Install Docker: https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/#set-up-the-repository

 2) `sudo docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v ~:/home/developer/ seespinoza/memecos`


# Docker Page
https://hub.docker.com/r/seespinoza/memecos
