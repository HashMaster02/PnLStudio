'''
To run the server:
    1. ensure you have a virtual environment activated
    2. run the command: pip install -r requirements.txt
    3. run the command: python main.py
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Utils.DataframeLoader import load_dataframes
from Core.middleware import format_filters
from Core.server import router
import asyncio
import uvicorn
import sys

async def main():

    try:

        # Load dataframes from the database
        dataframes = await load_dataframes()
        router.dataframes = dataframes

        # Run the FastAPI application
        app = FastAPI()

        origins = ["http://localhost", "http://localhost:3000"]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        app.middleware('http')(format_filters)
	
        app.include_router(router)
        config = uvicorn.Config(app, host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        await server.serve()
    except Exception as e: 
        print(f"Something went wrong while initializing the server: {e}")
 

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Handle graceful shutdown
        asyncio.run(sys.exit(0))
