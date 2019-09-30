# TCR Analysis Tool Suite

This Python script was created as a GUI-graphical wrapper for command-line tools
used to visualize TCR repertoire data. Currently this software supports MEME, Circos,and 
TCR-dist.

# REQUIREMENTS

## Operating System:
 - This software has only been tested on Ubuntu and OSX (with 2010 Mac models or newer).
   The Tool Suite should be compatible with most Linux systems.

## Package dependencies
 - Before actually running the software Docker and xQuartz both need to be installed. Installation of these two
   additional software is automatically performed by the `run.sh` script.

*Note: xQuartz is not necessary on Linux systems.*

## SOFTWARE INSTALLATION

### Mac Users

1) Open the Terminal app and download the GitHub repository by using the following command: `git clone https://github.com/seespinoza/TCR_GUI_Suite.git`

2) Enter the folder by using this command `cd TCR_GUI_Suite.git`.

3) Run the software by typing `./run.sh`. This command may take a while to finish running the first time 
   since all software dependencies, such as Docker, will need to be downloaded. The Tool Suite should boot
   up much faster the second time it is launched.

## Ubuntu Users
 1) Download the GitHub repository: `git clone https://github.com/seespinoza/TCR_GUI_Suite.git`
 2) Run `./run.sh`.


# Docker Page
https://hub.docker.com/r/seespinoza/memecos
