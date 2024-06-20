from langchain_community.graphs import Neo4jGraph
from langchain_community.chat_message_histories import Neo4jChatMessageHistory

graph = Neo4jGraph(
    url="bolt://3.83.146.2:7687",
    username="neo4j",
    password="linen-searches-compensations"
)

def get_memory(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)

result = graph.query(
    query="""
    MATCH (m:Movie {title: 'Toy Story'}) 
    RETURN m.title, m.plot, m.poster
    """
)

print(result)
