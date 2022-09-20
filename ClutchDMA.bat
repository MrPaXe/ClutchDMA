@echo off

cd /D %~dp0

echo Downloading ClutchDMA files.

md ClutchDMA
cd .\ClutchDMA\

curl -O "http://clutch.paxe.at/ClutchDMA/dma.zip"
tar -xf dma.zip
del dma.zip

cls
start .
start .\dma.bat -v runAs
del %0