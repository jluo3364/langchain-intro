from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
import time
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = ChatOllama(model="llama3")

memory = ChatMessageHistory()

def get_memory(session_id):
    return memory

prompt = ChatPromptTemplate.from_messages([
    (
        "system","You are a frugal person, discussing expenses with acquaintances and speaking briefly because you're in a rush. You only speak about what you're certain about."
    ),
    ("system", "{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

chat_chain = prompt | llm | StrOutputParser()

chat_with_msg_history = RunnableWithMessageHistory(
    chat_chain, get_memory, 
    input_messages_key="question", 
    history_messages_key="chat_history")

stores_context = """
{
    "stores": [
        {"name": "Costco", "location": "20 miles away", "sales": "every 1st of the month, "best_deals": "bread"},
        {"name": "Walmart", "location": "10 miles away", "sales": "every 15th of the month", "best_deals": "produce"}
    ]}"""

while True:
    start_time = time.time()
    # response = chat_chain.invoke({
    #     "context": stores_context,
    #     "question": "How can I save money at Costco?"
    #     })
    question = input("> ")
    response = chat_with_msg_history.invoke({
        "context": stores_context,
        "question": question
        },
        config={"configurable": {"session_id": "none"}}
    )
    end_time = time.time()
    print(response)
    print(f"Time taken: {end_time - start_time:.2f} seconds")

# "How can I save money at Costco?"
# "What other tips do you have for other stores?"
