#!/bin/bash

# Ensure backend setup script is executable and run it
if [ -f "backend/setup.sh" ]; then
    chmod +x backend/setup.sh
    cd ./backend 
    ./setup.sh
    if [ $? -ne 0 ]; then
        echo "Error: Backend setup script failed."
        exit 1
    fi
else
    echo "Error: backend/setup.sh not found."
    exit 1
fi

cd ../

echo "Dependencies installed for backend!"

# Ensure frontend setup script is executable and run it
if [ -f "frontend/setup.sh" ]; then
    chmod +x frontend/setup.sh
    cd ./frontend
    ./setup.sh
    if [ $? -ne 0 ]; then
        echo "Error: Frontend setup script failed."
        exit 1
    fi
else
    echo "Error: frontend/setup.sh not found."
    exit 1
fi

cd ../

echo "Dependencies installed for frontend!"

# Resolve values dynamically
USER=$(whoami)
WORKING_DIR=$(pwd)
PYTHON_BIN=$(which python3)
NPM_BIN=$(which npm)

cat <<EOF > "findash_backend.service"
[Unit]
Description=Findash Service
After=network.target

[Service]
User=$USER
WorkingDirectory=$WORKING_DIR/backend
ExecStart=$WORKING_DIR/backend/venv/bin/python $WORKING_DIR/backend/main.py

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF


cat <<EOF > "findash_frontend.service"
[Unit]
Description=findash Backend Service
After=network.target

[Service]
User=$USER
WorkingDirectory=$WORKING_DIR/frontend
ExecStart=$NPM_BIN run start
Restart=always
RestartSec=5
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF

# Move the service file to systemd directory
sudo mv "findash_backend.service" /etc/systemd/system/
sudo mv "findash_frontend.service" /etc/systemd/system/

# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable findash_backend.service
sudo systemctl enable findash_frontend.service
sudo systemctl start findash_backend.service
sudo systemctl start findash_frontend.service

echo "financial dashboard installed and started successfully."
