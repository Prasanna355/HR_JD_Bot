import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from typing import Union, List, Tuple, Dict
from langchain.schema import AgentFinish
from urllib.parse import quote_plus

# Load variables from the .env file into the environment
load_dotenv()

username = ""
password = ""
MONGO_URI = f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@hr-bot.eranirj.mongodb.net/?retryWrites=true&w=majority&appName=HR-BOT"

client = MongoClient(MONGO_URI)

db = client["JD_demo"]
collection = db["JD_collection"]

agent_finishes = []  # List to store AgentFinish objects

call_number = 0

def store_agent_output(agent_output: Union[str, List[Tuple[Dict, str]], AgentFinish], agent_name: str = 'Generic call'):
    global call_number  # Declare call_number as a global variable
    call_number += 1

    # Prepare data to store in MongoDB
    data = {
        "call_number": call_number,
        "agent_name": agent_name
    }

    # Try to parse the output if it is a JSON string
    if isinstance(agent_output, str):
        try:
            agent_output = json.loads(agent_output)  # Attempt to parse the JSON string
        except json.JSONDecodeError:
            pass  # If there's an error, leave agent_output as is

    # Check if the output is a list of tuples as in the first case
    if isinstance(agent_output, list) and all(isinstance(item, tuple) for item in agent_output):
        for action, description in agent_output:
            # Add attributes to data
            data["tool_used"] = getattr(action, 'tool', 'Unknown')
            data["tool_input"] = getattr(action, 'tool_input', 'Unknown')
            data["action_log"] = getattr(action, 'log', 'Unknown')
            data["description"] = description
            # Insert data into MongoDB
            collection.insert_one(data)

    # Check if the output is an AgentFinish object as in the second case
    elif isinstance(agent_output, AgentFinish):
        # Extracting 'output' and 'log' from the nested 'return_values' if they exist
        output = agent_output.return_values.get('output', 'Unknown')
        # Add AgentFinish output to data
        data["agent_finish_output"] = output
        # Insert data into MongoDB
        collection.insert_one(data)
        agent_finishes.append(agent_output)

    # Handle unexpected formats
    else:
        # If the format is unknown, store the input directly
        data["unknown_format"] = agent_output
        # Insert data into MongoDB
        collection.insert_one(data)

