# Project Structure

The project includes 2 main directories:

-   **frontend**: Contains the frontend code which is built in Next.js
-   **backend**: Contains the backend code which is built in Python

The root folder also contains a few shell scripts:

-   **install.sh**: Installs the dependencies for the frontend and backend and creates a systemd service for the application. This is done by creating a _findash_frontend.service_ and _findash_backend.service_ file in the "/etc/systemd/system" directory.
-   **remove.sh**: Removes the _findash_frontend.service_ and _findash_backend.service_ scripts from the "/etc/systemd/system" directory. It does NOT remove the dependencies within the **frontend** and **backend** directories.
-   **restart.sh**: Restarts the systemd service for both the frontend and backend.

For Mac users, the scripts are prefixed with "MAC" and uses launchd instead of systemd for the services

# Installation Instructions

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

At this point, the application should work. However, we need to add your data to the database before you'll see anything on the frontend. The next steps will require you to have a folder in the backend called **trades** that includes the CSV files that has your data in it. The directory structure within the **backend** directory should look like this:

```
backend
|     Core/
|     database.db
|     main.py
|     requirements.txt
|     schema.prisma
|     setup.sh
|---- trades/
        | realized_total.csv
        | total.csv
        | unrealized_total.csv
     Utils/
     venv/
```

7. run the command below to add the data in the **trades** directory to the database. This may take some time.

```bash
python -m Utils.AddNewStatement
```

8. run the command below to start the server:

```bash
python main.py
```

**The application should now be available via link: http://localhost:3000**
