'''a simple AI LLM Chatbot using OpenAI gpt'''

from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START,END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages : List [HumanMessage]
    
llm = ChatOpenAI(model = "o4-mini") # pik any model you want

def process (state : AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print (f"\nAI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()


user_input = input("Enter: ")
while user_input.lower() != "exit":
    agent.invoke({"messages" : [HumanMessage(content = user_input)]})
    user_input = input("Enter: ")
    

# currently this agent has no memory unit

    