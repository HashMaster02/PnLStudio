# Project Overview

This is a full-stack financial dashboard application designed for a client to analyze their trading performance data from Excel/CSV spreadsheets provided to them by their investment firm. The system processes financial statements and presents them through an interactive web dashboard.

The core technologies used include:

-   FastAPI
-   Pandas
-   SQLite
-   Prisma
-   Next.js
-   Recharts

# Project Structure

The project includes 2 main directories:

-   **frontend**: Contains the frontend code which is built in Next.js
-   **backend**: Contains the backend code which is a REST API built in Python

There are 3 ways to start the application:

-   **Using Docker (Highly recommended for all platforms)**
-   Shell scripts (for Linux users)
-   Manual installation

Successful setup should deploy the frontend to http://localhost:3000 and backend to http://localhost:8000.

# Installation Instructions

## Docker

The easiest way to build the project. Ensure you have the latest version of:

-   **Docker**
-   **Docker Compose**

1. Ensure you are in the main directory containing the **docker-compose.yaml** file
2. run the command below to build the frontend and backend images and deploy them as Docker containers:

```bash
docker-compose up
```

## Automatic Installation (via shell scripts)

Ensure the packages below are available on your system:

-   Node (version 21 or later)
-   NPM

### Linux Systems

1. Ensure you are in the main directory containing the **frontend** and **backend** directories
2. run the command below to give execution permissions to the install.sh script:

```bash
chmod +x install.sh
```

3. run the command below to install the frontend and backend on your system as a systemd service:

```bash
./install.sh
```

## Manual Installation

### Frontend

Ensure the packages below are available on your system:

-   Node (version 21 or later)
-   NPM

To build and run the frontend:

1. change directories into the **frontend** directory
2. run the command below to install dependencies:

```bash
npm install
```

3. run the command below to build the project using Next.js:

```bash
npm run build
```

4. run the command below to start the server:

```bash
npm start
```

The frontend should now be hosted on http://localhost:3000

### Backend

Ensure the packages below are available on your system:

-   python3 (version 10 or later)
-   pip
-   virtualenv

To build and run the backend:

1. change directories into the **backend** directory
2. run the command below to create a python virtual environment:

```bash
virtualenv venv
```

3. run the command below to activate the virtual environment:

```bash
source venv/bin/activate
```

4. run the command below to install dependencies:

```bash
pip install -r requirements.txt
```

5. run the command below to generate a prisma client:

```bash
prisma generate
```

6. run the command below to generate a SQLite database from the prisma schema:

```bash
prisma db push
```

7. run the command below to add the data in the <RELATIVE_PATH> directory to the database. Use **trades/synthetic** to load preview data. This step may take some time.

```bash
python -m Utils.AddNewStatement <RELATIVE_PATH>
```

8. run the command below to start the server:

```bash
python main.py
```

**The application should now be available via link: http://localhost:3000**
