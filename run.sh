#!/bin/bash

# If Ubuntu install and run docker
if [[ "$OSTYPE" == "linux-gnu" ]]; then
	echo $OSTYPE

	docker -v 2> /dev/null
	if [[ $? != 0 ]] ; then
		sudo apt install docker.io
	else
		echo "docker already installed"
	fi

	sudo docker run -e DISPLAY=$DISPLAY --net=host -v ~:/home/developer/ seespinoza/memecos > /dev/null

# If UBuntu install and run docker
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
		echo "updating brew"
		brew update
	fi

	socat -v 2> /dev/null
	if [[ $? != 0 ]]; then
		echo "installing socat"
		brew install socat
	else
		echo "socat is already installed."
	fi
	
	# Install xquartz
	open -a Xquartz
	if [[ $? != 0 ]]; then
		echo "installing xquartz"
		brew install xquartz
		open -a Xquartz
	else
		echo "xquartz already installed"
	fi

	brew info brew-cask 2> /dev/null
	if [[ $? != 0 ]]; then
		echo "installing Homebrew Cask"
		brew install caskroom/cask/brew-cask
	else
		echo "cask is already installed"
	fi

	docker -v 2> /dev/null
	if [[ $? != 0 ]]; then
		echo "installing Docker"
		brew cask install docker
	else
		echo "docker is already installed"
	fi
	
	socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\" &

	defaults write org.macosforge.xquartz.X11.plist nolisten_tcp 0

	IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
	
	open /Applications/Docker.app

	sudo docker run -e DISPLAY=${IP}:0 -v ~:/home/developer/ seespinoza/memecos > /dev/null
fi

