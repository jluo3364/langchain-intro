from langchain_community.graphs import Neo4jGraph
from langchain_community.chat_message_histories import Neo4jChatMessageHistory
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
import time
from langchain_core.runnables.history import RunnableWithMessageHistory
from uuid import uuid4

llm = ChatOllama(model="llama3")

SESSION_ID = str(uuid4())
print(f"Session ID: {SESSION_ID}")

graph = Neo4jGraph(
    url="bolt://3.83.146.2:7687",
    username="neo4j",
    password="linen-searches-compensations"
)

def get_memory(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)


memory = ChatMessageHistory()


prompt = ChatPromptTemplate.from_messages([
    (
        "system","You are a frugal person, discussing expenses with acquaintances and speaking briefly because you don't like to talk much. You only speak about what you're certain about."
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

    question = input("> ")
    if question.lower() == "exit":
        break
    response = chat_with_msg_history.invoke({
        "context": stores_context,
        "question": question
        },
        config={"configurable": {"session_id": SESSION_ID}}
    )
    end_time = time.time()
    print(response)
    print(f"Time taken: {end_time - start_time:.2f} seconds")
print(graph.schema)
# "How can I save money at Costco?"
# "What other tips do you have for other stores?"


