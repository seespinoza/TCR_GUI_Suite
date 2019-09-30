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
 1) Download the GitHub repository by pressing the green button in the upper right-hand corner that says `Clone or download`.
    Choose `Download ZIP`.

 2) Once you have opened the folder, double click on OSX_run.command to run the Tool Suite.

*The software may take some time to finish running the first time since some additional software dependencies need to be installed
 Docker, xQuartz, etc)*
## Ubuntu Users
 1) Download the GitHub repository: `git clone https://github.com/seespinoza/TCR_GUI_Suite.git`
 2) Run `./Linux_run.sh`.


# Docker Page
https://hub.docker.com/r/seespinoza/memecos
