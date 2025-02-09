#!/bin/bash

# Check if virtualenv is installed
if ! command -v virtualenv &> /dev/null
then
    echo "Error: virtualenv is not installed. Please install it first."
    exit 1
fi

# Create virtual environment
virtualenv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment."
    exit 1
fi

# Install dependencies
venv/bin/python -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Generate Prisma client
venv/bin/python -m prisma generate
if [ $? -ne 0 ]; then
    echo "Error: Prisma generate failed."
    deactivate
    exit 1
fi

# Push Prisma database changes
prisma db push
if [ $? -ne 0 ]; then
    echo "Error: Prisma db push failed."
    deactivate
    exit 1
fi

# Run AddNewStatement.py with message
echo "Running Utils/AddNewStatement.py. This may take some time..."
Utils/AddNewStatement.py
if [ $? -ne 0 ]; then
    echo "Error: AddNewStatement.py execution failed."
    deactivate
    exit 1
fi

# Deactivate virtual environment
deactivate

echo "Script execution completed successfully."

