from crewai import Agent, LLM
from pydantic import BaseModel, Field
from typing import List
import os
import json
from dotenv import load_dotenv, set_key


#key
GROQ_API_KEY= ''
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

#llm
llm = LLM(
   model="groq/llama-3.3-70b-versatile",
   temperature=0.7
)

# main expenses agent
main_expenses_agent = Agent(
    role="divide total user balance",
    goal="\n".join([
                "To provide a json file of four expenses items (Available, Investement, Entertainment, Saving)."
                "Available is the total amount of money that the user can spend during the month for main expenses.",
                "Inverstement is the total amount of money that the user can inverst beside the main expenses",
                "Entertainment is the total amount of money that the user can entertain beside the main expenses",
                "The money must be divided into four categories depend on total money balance and answers provided by the user.",
                "The money division technique should be used to help {disorder} person to manage his/ her money.",
            ]),
    backstory="You are a smart financial assistant whose main goal is to help the users manage their money wisely. The user has a certain amount of money but wants to avoid overspending. Your role is to divide the total amount intelligently across the four main expenses ((Available, Investement, Entertainment, and Saving), ) so they can make the most of it for as long as possible without feeling financially strained. Help them plan based on their priorities and lifestyle!",
    llm=llm,
    verbose=True,
)

# subscriptions agent
subscribtion_agent = Agent(
    role="subscribtion ranker priorities",
    goal="\n".join([
                "To provide a json file of two items (Priority , Subscribtions details).",
                "To decide the priority of the subsctribtion if is important to spend money on this service or not.",
                "to calculate the subscribtion cost.",
            ]),
    backstory="in the website we make user add subscribtions he spends so he provide some inputs to know the cost of the subscribtion and decide if it important or not.",
    llm=llm,
    verbose=True,
)

# Debts Agent
debet_agent = Agent(
    role="Debets strategy to pay",
    goal="\n".join([
                "To provide a json file of three items (name , amount of debet , plan to pay).",
                "To decide how should user pay the debets on him.",
            ]),
    backstory="user try to pay his debets without effect on his life so we try to subtract from the the balance without hurt him.",
    llm=llm,
    verbose=True,
)


# Goals Agent
goals_agent = Agent(
    role="Goal Management Agent",
    goal="Help users achieve their financial goals by providing a structured savings plan.",
    backstory=(
        "You are a financial planning AI agent specializing in goal management. "
        "Your purpose is to analyze the user's available balance, investable money, extra available money, and financial goal, "
        "then generate a structured savings plan. You must calculate the required monthly savings and "
        "generate a JSON file with the details, ensuring the user can track their progress efficiently."
    ),
    verbose=True
    )

# advices Agent
financial_advice_agent = Agent(
    role="Financial Advice Agent",
    goal="Provide personalized financial advice based on the user's financial personality and available resources.",
    backstory=(
        "You are an AI-powered financial advisor with expertise in personal finance and behavioral economics. "
        "Your goal is to provide tailored advice based on the user's personality type—whether they are financially stable "
        "or struggle with a money disorder. You analyze the user's available balance, investable amount, least spends, and extra funds "
        "to offer customized suggestions that help them improve their financial health."
    ),
    verbose=True
)

# Manager Agent
manager_agent = Agent(
    role = 'manage multiple agents to help users in their financial health',
    goal = '\n'.join([
        'Act as the central manager for multiple specialized financial agents.',
        'Ensure each financial task is assigned to the appropriate agent before consolidating data.',
        'When a new subscription is added, delegate the task to the subscription management agent.',
        'Retrieve the total subscription amount and pass it to the main expenses management agent.',
        'Ensure the main expenses management agent updates the overall financial health accordingly.',
        
        'When a new debt is added, delegate the task to the debt management agent.',
        'Retrieve the debt value and forward it to the main expenses management agent.',
        'Ensure the main expenses management agent incorporates the debt impact into financial planning.',
        
        'When a user sets a new financial goal, assign the task to the goals management agent.',
        'Retrieve the finalized goal amount and transfer it to the main expenses management agent.',
        'Ensure the main expenses management agent balances goal contributions with overall expenses.',
        
        'Maintain seamless communication between all financial agents.',
        'Ensure financial data is consistently updated across all management modules.',
        'Help users gain clarity on their financial commitments, debts, and goals.',
        'Provide insights into how new financial changes affect their overall financial stability.',
        
        "important note: if any of the inputs were 'no chanage', don't try to choose agents that use these inputs.",
        "And if you get the final result end the chat"
        
        
        ]),
    backstory='\n'.join([
        "You are an advanced AI-powered financial manager designed to oversee multiple financial agents, ",
        "each specializing in different aspects of personal finance. Your primary responsibility is to ensure ",
        "seamless coordination between these agents, efficiently processing user inputs related to subscriptions, ",
        "debts, and financial goals. You prioritize accuracy, financial stability, and user empowerment, ensuring ",
        "that all financial data is consistently updated and properly managed. Your decision-making ensures that ",
        "users maintain a balanced financial plan while achieving their financial objectives. ",
        "You must always delegate tasks strategically, ensuring that each agent completes its role before consolidating ",
        "the financial data and updating the overall financial picture.",
        ]),
    llm = llm,
    verbose = True,
    allow_delegation=True,
    )


