#!/bin/bash

# Unload services
launchctl unload ~/Library/LaunchAgents/com.findash.frontend.plist
launchctl unload ~/Library/LaunchAgents/com.findash.backend.plist

# Remove plist files
rm ~/Library/LaunchAgents/com.findash.backend.plist
rm ~/Library/LaunchAgents/com.findash.frontend.plist

echo "Financial dashboard services removed successfully."

