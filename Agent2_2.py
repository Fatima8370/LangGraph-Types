import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages : List[Union[HumanMessage, AIMessage]] 
    
    
llm = ChatOpenAI(model = "o4-mini")

def process (state: AgentState) -> AgentState:
    '''will solve input request'''
    response = llm.invoke(state["messages"])
    print (f"\nAI: {response.content}")
    state["messages"].append(AIMessage(content= response.content))
    
    return state    


graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge('process',END)

app = graph.compile()


conversation_history = [] # history list / memory


user_input = input ("Enter Prompt: ")
while user_input.lower() != "exit":
    
    conversation_history.append(HumanMessage(content = user_input))
    result = app.invoke({"messages": conversation_history}) # enter context
    conversation_history = result["messages"] # reassign the conversation history with the AI response
    user_input = input("Enter Prompt: ")
    

# has now a memory unit BUTTTTTTTTTT
# cannot retain data
# meaning if i run the chatbot again
# the history for the previous conversation will be gone

# problem -> temporary memory

# you're also supposed to restore the conversation too

''' the code below will allow us to store the conversation history in a text file
    so when the conversation finishes, the History is preserved'''

with open("conversation_history.txt", "w") as f:
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            f.write(f"Human: {message.content}\n")
        elif isinstance(message, AIMessage):
            f.write(f"AI: {message.content}\n")
    f.write("End of Conversation\n")


print ("\n conversation stored in text file")


# yet another problem
# as the we keep storing the the history, it gets lengthy
# this uses up input tokens and will cost alot
# we can add a condition if human texts exceeds 5, remove the first 3 messages
# this saves costs 