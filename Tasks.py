from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from pydantic import BaseModel, Field
from typing import List
import os
import json
from Agents import main_expenses_agent, subscribtion_agent, goals_agent, financial_advice_agent, debet_agent, manager_agent

output_dir = "./ai-agent-output"

# main expenses tast
class DashBoardResult(BaseModel):
  Available: float
  Investement: float
  Entertainment: float
  Saving: float
  
  
main_expenses_task = Task(
    description="\n".join([
        "The total amount of money that the user have is {total_money} EGP",
        "our website is trying to divide the money for a person has to save it and do not waste it.",
        "the website wants to make priorities to the important thing that is the 'expenses' and you should choose the best amount to him to make him lives in confartable zone.",
        "you should to substract {percetage}% from total money of the user and get it in json format with other values.",
        "the data will be displaied in dashboard of a user to see how much he can spend from each category.",
        "i want at the end to get four categories:",
        "1. Expenses (Basic expenses like food and school expenses and electric bill and water bill and gas bill).",
        "2. Investment (is the limit of money to use it in investment).",
        "3. Entertainment expenses (is the limit of money to use it in entertainment).",
        "4. saving money (the amount of money the user can save from the total money)."
        
    ]),
    expected_output="A JSON object containing a list of four categories (Available,Investement,Entertainment,and Saving).",
    output_json=DashBoardResult,
    output_file=os.path.join(output_dir, "step_1_main_expenses.json"),
    agent=main_expenses_agent
)

# subscription agent task
class SubBoard(BaseModel):
  priority: str = Field(..., title="must be low or medium or high.")
  susbscribtion_amount: float
  comp_sub_name : str = Field(..., title="the name of subscribtion")
  type_of_sub: str = Field(..., title="the type of subscribtion")
  
subscribtion_task = Task(
    description="\n".join([
        "our website is try to divide the money the the person has to save it and do not waste it in somethings like investments or entertainment.",
        "in this agent i want to know if the priority of the subscribtion if it is (low or medium or high).",
        "i put the subscribtion to make you change it in the futuer if the price of the subscribtion is changed.",
        "also return name of company i enterd in with the json file",
        "also add in the json file the type of the subsctibtion"
        "the data you will get is :",
        "1. name of company that is subscribed to (the name is {sub_company_name}) i need also to add it in the json file",
        "2. type of susbscribtion monthly , weakly , 3 months , yearly (the type is {subscribtion_type}) i want you also to return this in the json file.",
        "3. the initation amount the user will decide it (the amount is {subscribtion_amount}EGP).",
        "4. the job of the person (the job is {user_job}).",
        "5. Age of the person (the age is '{user_age}').",

    ]),
    expected_output="A JSON object containing a list of two keys (priority,susbscribtion amout).",
    output_json=SubBoard,
    output_file=os.path.join(output_dir, "step_1_subscribtions.json"),
    agent=subscribtion_agent
)

# debt_agent task
class DebtsPlan(BaseModel):
  pay_amount : float
  pay_type : str = Field(..., title="pay will be monthly or weekly or every three months or what.")

class DebtsBoard(BaseModel):
  name_of_creditor: str = Field(..., title="must be low or medium or high.")
  debet_amount: float
  debet_plan : List[DebtsPlan]
  
debet_task = Task(
    description="\n".join([
        "our website is try to divide the money the the person has to save it and do not waste it in somethings like investments or entertainment.",
        "after agent know about user from his balance in three categories (basic expenses: {Availble_money} , Investment : {invest_money} , extra money : {extra_money})",
        "i put the subscribtion to make you change it in the futuer if the price of the subscribtion is changed.",
        "the debet the user had is {deb_amount}",
        "the name of debet is {name_deb}"
    ]),
    expected_output="A JSON object containing a list of two keys (debet name,amount of debet, plan to pay (pay 'amout should pay every period of time', type if it monthly or what)).",
    output_json=DebtsBoard,
    output_file=os.path.join(output_dir, "step_1_Debets.json"),
    agent=debet_agent
)
# goals_agent task
class goals(BaseModel):
  goal_name: str = Field(..., title="must be meaningful.")
  monthly_saving: float = Field(..., title="the monthy total amount of money need to acheive the goal.")
 
goal_management_task = Task(
    description=(
        "Analyze the user's available balance, investable amount, extra available money, and desired financial goal. "
        "Calculate the monthly savings needed to reach the goal:({goal_desc}) within the given timeframe. "
        "Generate a JSON file with the goal name and required monthly savings."
    ),
    expected_output="A JSON file containing the goal name and required monthly savings amount.",
    output_json= goals,
    output_file=os.path.join(output_dir, "step_1_goals.json"),
    agent=goals_agent
)

# advisor_agent task
class advice(BaseModel):
  advice: str = Field(...)
 
financial_advice_task = Task(
    description=(
        "Analyze the user's financial situation, including available balance, investable money, least spends, and extra funds. "
        "Determine if the user is a normal spender or has a money disorder. Provide tailored financial advice accordingly."
    ),
    expected_output="A personalized financial advice report based on the user's financial personality.",
    output_json= advice,
    output_file=os.path.join(output_dir, "step_1_advice.json"),
    agent=financial_advice_agent
)


