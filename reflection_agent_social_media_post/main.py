""" Main module for the project"""
from typing import List, Sequence
from dotenv import load_dotenv
import os
load_dotenv()

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph

from chains import generate_chain, reflect_chain


REFLECT = "reflect"
GENERATE = "generate"

# defining nodes
def generation_node(state: Sequence[BaseMessage]):
    return generate_chain.invoke({"messages": state})

def reflection_node(state: Sequence[BaseMessage]):
    res = reflect_chain.invoke({"messages": state})
    return [HumanMessage(content=res.content)] # response is a human message to frame it with the role of human, to trick LLM so it thinks a human is sending this message.


# adding nodes
builder = MessageGraph()
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(GENERATE) # tells graph what node to start with in the graph

# building edges
def should_continue(state: Sequence[BaseMessage]):
    if len(state) > 6:
        return END
    return REFLECT 

builder.add_conditional_edges(GENERATE, should_continue) # if the condition is met, it will go to the next node, else it will END.
builder.add_edge(REFLECT, GENERATE) # creates an edge from reflect to generate

# compile the graph
graph = builder.compile()

print(graph.get_graph().draw_mermaid())


if __name__ == "__main__":
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  
