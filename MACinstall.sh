#!/bin/bash

# Resolve dynamic values
USER=$(whoami)
WORKING_DIR=$(pwd)
PYTHON_BIN=$(which python3)
NPM_BIN=$(which npm)

# Create LaunchAgent directory if it doesn't exist
mkdir -p ~/Library/LaunchAgents

# Backend Service
cat <<EOF > ~/Library/LaunchAgents/com.findash.backend.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.findash.backend</string>
    <key>ProgramArguments</key>
    <array>
        <string>$WORKING_DIR/backend/venv/bin/python</string>
        <string>$WORKING_DIR/backend/main.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$WORKING_DIR/backend</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Frontend Service
cat <<EOF > ~/Library/LaunchAgents/com.findash.frontend.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.findash.frontend</string>
    <key>ProgramArguments</key>
    <array>
        <string>$NPM_BIN</string>
        <string>run</string>
        <string>start</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$WORKING_DIR/frontend</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>NODE_ENV</key>
        <string>production</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Load the services
launchctl load ~/Library/LaunchAgents/com.findash.backend.plist
launchctl load ~/Library/LaunchAgents/com.findash.frontend.plist

echo "Financial dashboard installed and started successfully."

