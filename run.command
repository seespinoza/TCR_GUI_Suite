#!/bin/bash

# Change working directory to where this file is located
cd -- "$(dirname "$BASH_SOURCE")"

# Check if OS type is linux
if [[ "$OSTYPE" == "linux-gnu" ]]; then
	echo $OSTYPE

	docker -v 2> /dev/null
	if [[ $? != 0 ]] ; then
		sudo apt install docker.io
	else
		echo "docker already installed"
	fi

	# update docker image
	sudo docker pull seespinoza/memecos:latest

	sudo ./TCR_tool_suite_gui.py

# Check if OS type is OSX
elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo $OSTYPE

	# Download command line tools for OSX
	if type xcode-select >&- && xpath=$( xcode-select --print-path ) && test -d "${xpath}" && test -x "${xpath}" ; then
   		echo "xcode already installed"
	else
		code-select --install
	fi

	# Download and install brew
	which -s brew 2> /dev/null
	if  [[ $? != 0 ]]; then
		echo "installing Homebrew"
		/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	else
		echo "Brew is already installed. Checking for updates."
		brew update
	fi
	
	# Download and install cask
	brew info brew-cask 2> /dev/null
	if [[ $? != 0 ]]; then
		echo "installing Homebrew Cask"
		brew install caskroom/cask/brew-cask
	else
		echo "cask is already installed"
	fi

	# Download and install docker
	docker -v 2> /dev/null
	if [[ $? != 0 ]]; then
		echo "installing Docker"
		brew cask install docker
	else
		echo "docker is already installed"
	fi

	# Download and install python dependencies
	python3 --version 2> /dev/null
	if [[ $? != 0 ]]; then
		echo "installing python3"
		cp -f python-with-tcl.rb /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/python.rb
		HOMEBREW_NO_AUTO_UPDATE=1 brew install --build-from-source python
	else
		echo "Python already installed."

	fi 
	
	# Check to see if tkinter is properly installed
	python3.8 -c "import tkinter; tkinter.Tcl().eval('info patchlevel')"
	if [[ $? != 0 ]]; then
		echo "Tkinter not properly installed."
	else
		echo "Tkinter properly installed."
	fi


        # Check to see if PIL is installed
	python3 -c "import PIL"
        if [[ $? != 0 ]]; then
		echo "installing Pillow module."
	        pip3 install Pillow
	else
		echo "Pillow already installed."
	fi	
	
	open /Applications/Docker.app
	
	# Update docker image (Change this to a try and catch statement in-case software is being
        # run offline.
	docker pull seespinoza/memecos:latest

	./TCR_tool_suite_gui.py


fi

