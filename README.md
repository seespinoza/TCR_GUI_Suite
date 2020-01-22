# TCR Analysis Tool Suite

This Python script was created as a GUI-graphical wrapper for command-line tools
used to visualize TCR repertoire data. Currently this software supports MEME, Circos,and 
TCR-dist.

# REQUIREMENTS

## Operating System:
 - This software has only been tested on Ubuntu and OSX (with 2010 Mac models or newer).
   The Tool Suite should be compatible with most Linux systems.

## Package dependencies
 - This software requires installing several different software packages in order to run as intended.
   For OSX this includes Xcode, Homebrew, and Homebrew Cask. Python libraries tkinter and Pillow will also
   be installed.

*Note: The program itself will download all the packages necessary to run.*

## SOFTWARE INSTALLATION

### Mac Users
 1) Download the GitHub repository by pressing the green button in the upper right-hand corner that says `Clone or download`.
    Choose `Download ZIP`.

 2) Once you have opened the folder, right click on the `run.command` file and click `Open` to run the Tool Suite.
    Make sure you have a stable internet connection the first time running the software.

*The software may take some time to finish running the first time since some additional software dependencies need to be installed
 Docker, Homebrew, etc)*
## Ubuntu Users
 1) Download the GitHub repository: `git clone https://github.com/seespinoza/TCR_GUI_Suite.git`
 2) Run `./run.command`.


# Docker Page
https://hub.docker.com/r/seespinoza/memecos
