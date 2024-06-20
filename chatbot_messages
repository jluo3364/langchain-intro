
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatOllama
import time

llm = ChatOllama(model="llama3")
instructions = SystemMessage(content="""
                             You are a pastry chef, having a conversation about healthy ingredients. 
                             Respond using pastry chef knowledge and terminology but limit response to 100 words.
                             """)
question = HumanMessage(content="What are some healthy ingredients that can be used in baking?")
start_time = time.time()
response = llm.invoke([instructions, question])
end_time = time.time()
print(response.content)
print(f"Response time: {end_time - start_time:.2f} seconds")