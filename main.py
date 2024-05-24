import os
from dotenv import load_dotenv
from crewai import Crew, Process
from Agents import Agents
from Tasks import Tasks
from logs import store_agent_output
from langchain_groq import ChatGroq

# Load variables from the .env file into the environment
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="mixtral-8x7b-32768", verbose=True, temperature=0.5, groq_api_key=api_key)

# STATIC VARIABLE DECLARATION
company_details = '''
                  Name : KoworkerAI,
                  Location : Dubai,AE,
                  website : www.kowrokerai.com,
                  contact mail : desmondmarshall@gmail.com
                  '''

# object creation
agents = Agents()
tasks = Tasks()

JDAgent = agents.JD_agent()
ModifyAgent = agents.Modify_agent()

# get the requirements from the user for candidate
requirements = input("What are the requirements for the role? :")
Jd_task = tasks.draft_JD_task(JDAgent, requirements, company_details)

# Create a Job object for initial JD creation
crew_initial = Crew(
    agents=[JDAgent],
    tasks=[Jd_task],
    verbose=True,
    process=Process.sequential,
    full_output=True,
    share_crew=False,
    step_callback=lambda x: store_agent_output(x, "MasterCrew Agent")
)

# Kick off the initial JD creation work
results_initial = crew_initial.kickoff()

# Ask if modifications are needed
modify = input("Do you need to change any requirements? (yes/no) :")
if modify.lower() == 'yes':
    new_requirements = input("Provide new requirements to modify: ")
    Modify_task = tasks.modify_JD_task(ModifyAgent, new_requirements, company_details)

    # Create a Job object for modification
    crew_modify = Crew(
        agents=[ModifyAgent],
        tasks=[Modify_task],
        verbose=True,
        process=Process.sequential,
        full_output=True,
        share_crew=False,
        step_callback=lambda x: store_agent_output(x, "ModifyCrew Agent")
    )

    # Kick off the modification work
    results_modify = crew_modify.kickoff()

