from Agents import main_expenses_agent, subscribtion_agent, goals_agent, financial_advice_agent, debet_agent, manager_agent
from Tasks import main_expenses_task, subscribtion_task, debet_task, goal_management_task, financial_advice_task
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from pydantic import BaseModel, Field
from typing import List
import os
import json
from dotenv import load_dotenv, set_key


# load_dotenv()
# set_key(dotenv_path=".env", key_to_set="GEMINI_API_KEY", value_to_set="")

# ----------- LLM test ----------
# file_path = './final.json'

# # Load the JSON file
# with open(file_path, 'r') as file:
#     vertex_credentials = json.load(file)

# # Convert the credentials to a JSON string
# vertex_credentials_json = json.dumps(vertex_credentials)

# llm = LLM(
#     model="gemini/gemini-1.5-pro-latest",
#     temperature=0.7,
#     vertex_credentials=vertex_credentials_json
# )


#key
GROQ_API_KEY=''
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

#llm
llm = LLM(
   model="groq/gemma2-9b-it	",
   temperature=0.7
)

crew = Crew(
    agents=[
        main_expenses_agent, 
        subscribtion_agent, 
        goals_agent, 
        financial_advice_agent, 
        debet_agent,
    ],
    tasks=[
        main_expenses_task,
        subscribtion_task,        
        debet_task,
        goal_management_task,
        financial_advice_task
    ],
    manager_agent = manager_agent,
    process=Process.hierarchical,
)

# ----------- kickoffs ------------
crew_results = crew.kickoff(
    inputs={
      "total_money": 8000,
      'percetage': 10,
      'disorder': 'financial denial',
      
      'sub_company_name':'no chanage',
      'subscribtion_type':'no chanage',
      "subscribtion_amount": 'no chanage',
      "user_job" : "no chanage",
      "user_age" : 'no chanage',
      
      "Availble_money" : 'no chanage',
      "invest_money": 'no chanage',
      "extra_money": 'no chanage',
      "deb_amount" : 'no chanage',
      "name_deb" : "no chanage",
      
      'goal_desc': 'no chanage'
    }
)