#! /bin/bash

HubScript="hub.py"
InterfaceScript="interface.py"
ClassificationScript="class.py"

ptyHubToInterface_in=".ptyHubToInterface_in"
ptyHubToInterface_out=".ptyHubToInterface_out"
ptyInterfaceToHub_in=".ptyInterfaceToHub_in"
ptyInterfaceToHub_out=".ptyInterfaceToHub_out"
ptyHubToClass_in=".ptyHubToClass_in"
ptyHubToClass_out=".ptyHubToClass_out"
ptyClassToHub_in=".ptyClassToHub_in"
ptyClassToHub_out=".ptyClassToHub_out"

# Setup sockets
socat -d pty,raw,echo=0,link=$ptyHubToInterface_in pty,raw,echo=0,link=$ptyHubToInterface_out &
P1=$!
sleep 0.25

socat -d pty,raw,echo=0,link=$ptyInterfaceToHub_in pty,raw,echo=0,link=$ptyInterfaceToHub_out &
P2=$!
sleep 0.25

socat -d pty,raw,echo=0,link=$ptyHubToClass_in pty,raw,echo=0,link=$ptyHubToClass_out &
P3=$!
sleep 0.25

socat -d pty,raw,echo=0,link=$ptyClassToHub_in pty,raw,echo=0,link=$ptyClassToHub_out &
P4=$!
sleep 0.25

# Start Interface script
./$InterfaceScript $ptyHubToInterface_out $ptyInterfaceToHub_in &
P5=$!

# Start Classification script
./$ClassificationScript $ptyHubToClass_out $ptyClassToHub_in &
P6=$!

# Start Hub
./$HubScript $ptyHubToClass_in $ptyClassToHub_out $ptyHubToInterface_in $ptyInterfaceToHub_out

kill $P6
kill $P5
kill $P4
kill $P3
kill $P2
kill $P1
