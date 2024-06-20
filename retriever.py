from langchain.chains import RetrievalQA
from langchain_community.graphs import Neo4jGraph
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Neo4jVector
from langchain_community.embeddings import OllamaEmbeddings
import numpy as np

# Custom embedding model class to adjust the dimensions of embeddings
class CustomEmbeddingModel:
    def __init__(self, model, target_dim):
        self.embedding_model = OllamaEmbeddings(model=model)
        self.target_dim = target_dim

    def embed_query(self, text):
        original_embedding = self.embedding_model.embed_query(text)
        adjusted_embedding = self.adjust_embedding(original_embedding, self.target_dim)
        return adjusted_embedding

    def adjust_embedding(self, embedding, target_dim):
        current_dim = len(embedding)
        if current_dim > target_dim:
            # Truncate the embedding
            adjusted_embedding = embedding[:target_dim]
        elif current_dim < target_dim:
            # Pad the embedding with zeros
            adjusted_embedding = np.pad(embedding, (0, target_dim - current_dim), 'constant')
        else:
            # No adjustment needed
            adjusted_embedding = embedding
        return adjusted_embedding

llm = ChatOllama(model="llama3")

# Initialize the custom embedding model with the desired target dimensions
target_dim = 1536  # Example target dimension size
custom_embedding_provider = CustomEmbeddingModel(model="llama3", target_dim=target_dim)

# Configure Neo4j graph connection
graph = Neo4jGraph(
    url="bolt://3.83.146.2:7687",
    username="neo4j",
    password="linen-searches-compensations"
)

# Use the custom embedding provider to create the vector store
movie_plot_vector = Neo4jVector.from_existing_index(
    custom_embedding_provider,
    graph=graph,
    index_name="moviePlots",
    embedding_node_property="plotEmbedding",
    text_node_property="plot",
)

plot_retriever = RetrievalQA.from_llm(llm=llm, retriever=movie_plot_vector.as_retriever(), verbose = True, return_source_documents = True)

response = plot_retriever.invoke("A movie where aliens land and attack earth.")

print(response)

# Perform a similarity search using the vector store
# result = movie_plot_vector.similarity_search("A movie where aliens land and attack earth.")
# for doc in result:
#     print(doc.metadata["title"], "-", doc.page_content)
