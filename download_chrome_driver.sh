#!/bin/bash

LATEST_VERSION=`curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE`
URL=https://chromedriver.storage.googleapis.com/$LATEST_VERSION/chromedriver_linux64.zip

wget $URL

mkdir -p driver
unzip -o chromedriver_linux64.zip -d driver
rm chromedriver_linux64.zip
