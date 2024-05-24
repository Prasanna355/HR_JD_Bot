from crewai import Agent
from textwrap import dedent
from logs import store_agent_output
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain_groq import ChatGroq

# Load variables from the .env file into the environment
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="mixtral-8x7b-32768", verbose=True, temperature=0.5, groq_api_key=api_key)

class Agents():
    def JD_agent(self):
        return Agent(
            role='HR - Senior Job Description Writer',
            goal="""Generate job description based on requirements provided""",
            backstory=dedent("""\
            You are a HR executive working company, you are master at synthesizing a variety of Job descriptions
            that will address the requirements mentioned."""),
            llm=llm,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
            memory=True,
            step_callback=lambda x: store_agent_output(x, "HR - Senior Job Description Writer"),
        )

    def Modify_agent(self):
        return Agent(
            role='HR - Job Description Modifier',
            goal="""Modify existing job description based on new requirements provided""",
            backstory=dedent("""\
            You are a HR executive responsible for making necessary modifications to the existing job descriptions
            to align with the updated requirements."""),
            llm=llm,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
            memory=True,
            step_callback=lambda x: store_agent_output(x, "HR - Job Description Modifier"),
        )
