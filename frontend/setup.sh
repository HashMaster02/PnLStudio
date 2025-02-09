#!/bin/bash

# Check if npm is installed
if ! command -v npm &> /dev/null
then
    echo "Error: npm is not installed. Please install Node.js and npm first."
    exit 1
fi

# Install dependencies
npm install
if [ $? -ne 0 ]; then
    echo "Error: npm install failed."
    exit 1
fi

# Build the project
npm run build
if [ $? -ne 0 ]; then
    echo "Error: npm run build failed."
    exit 1
fi

echo "Build completed successfully."
