# import os
# from crewai import Agent, Task, Crew, Process
#
# from textwrap import dedent
# from langchain.llms import OpenAI, Ollama
# from langchain_openai import ChatOpenAI
# from langchain.tools import DuckDuckGoSearchRun
#
# # Install duckduckgo-search for this example:
# # !pip install -U duckduckgo-search
#
# search_tool = DuckDuckGoSearchRun()
#
#
# # This is an example of how to define custom agents.
# # You can define as many agents as you want.
# # You can also define custom tasks in tasks.py
# class CustomAgents:
#     def __init__(self):
#         self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
#
#     def agent_1_name(self):
#         return Agent(
#             role="Define agent 1 role here",
#             backstory=dedent(f"""Define agent 1 backstory here"""),
#             goal=dedent(f"""Define agent 1 goal here"""),
#             # tools=[tool_1, tool_2],
#             allow_delegation=False,
#             verbose=True,
#             llm=self.OpenAIGPT35,
#         )
#
#     def agent_2_name(self):
#         return Agent(
#             role="Define agent 2 role here",
#             backstory=dedent(f"""Define agent 2 backstory here"""),
#             goal=dedent(f"""Define agent 2 goal here"""),
#             # tools=[tool_1, tool_2],
#             allow_delegation=False,
#             verbose=True,
#             llm=self.OpenAIGPT35,
#         )
#
#
# # This is an example of how to define custom tasks.
# # You can define as many tasks as you want.
# # You can also define custom agents in agents.py
# class CustomTasks:
#     def __tip_section(self):
#         return "If you do your BEST WORK, I'll give you a $10,000 commission!"
#
#     def task_1_name(self, agent, var1, var2):
#         return Task(
#             description=dedent(
#                 f"""
#             Do something as part of task 1
#
#             {self.__tip_section()}
#
#             Make sure to use the most recent data as possible.
#
#             Use this variable: {var1}
#             And also this variable: {var2}
#         """
#             ),
#             agent=agent,
#         )
#
#     def task_2_name(self, agent):
#         return Task(
#             description=dedent(
#                 f"""
#             Take the input from task 1 and do something with it.
#
#             {self.__tip_section()}
#
#             Make sure to do something else.
#         """
#             ),
#             agent=agent,
#         )
#
#
# class CustomCrew:
#     def __init__(self, var1, var2):
#         self.var1 = var1
#         self.var2 = var2
#
#     def run(self):
#         # Define your custom agents and tasks in agents.py and tasks.py
#         agents = CustomAgents()
#         tasks = CustomTasks()
#
#         # Define your custom agents and tasks here
#         custom_agent_1 = agents.agent_1_name()
#         custom_agent_2 = agents.agent_2_name()
#
#         # Custom tasks include agent name and variables as input
#         custom_task_1 = tasks.task_1_name(
#             custom_agent_1,
#             self.var1,
#             self.var2,
#         )
#
#         custom_task_2 = tasks.task_2_name(
#             custom_agent_2,
#         )
#
#         # Define your custom crew here
#         crew = Crew(
#             agents=[custom_agent_1, custom_agent_2],
#             tasks=[custom_task_1, custom_task_2],
#             verbose=True,
#         )
#
#         result = crew.kickoff()
#         return result
#
#
# # This is the main function that you will use to run your custom crew.
# def execute(user_input, clarifications=None):
#     print("## Welcome to Crew AI Template")
#     print("-------------------------------")
#     var1 = input(dedent("""Enter variable 1: """))
#     var2 = input(dedent("""Enter variable 2: """))
#
#     custom_crew = CustomCrew(var1, var2)
#     result = custom_crew.run()
#     print("\n\n########################")
#     print("## Here is you custom crew run result:")
#     print("########################\n")
#     print(result)