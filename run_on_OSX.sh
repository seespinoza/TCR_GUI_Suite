#!/bin/bash

if type xcode-select >&- && xpath=$( xcode-select --print-path ) &&
   test -d "${xpath}" && test -x "${xpath}" ; then
   echo "xcode already installed"
else
   xcode-select --install
fi

which -s brew
if [[ $? != 0 ]] ; then
    # Install Homebrew
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
    brew update
fi

socat -v
if [[ $? != 0 ]] ; then
    # Install Homebrew
    brew install socat
else
    echo "socat already installed"
fi

open -a Xquartz
if [[ $? != 0]] ; then
    brew install xquartz
else
    echo "xquartz already installed"
fi
socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\"

defaults write org.macosforge.xquartz.X11.plist nolisten_tcp 0

IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')


sudo docker run -e DISPLAY=${IP}:0 -v ~:/home/developer/ seespinoza/memecos
