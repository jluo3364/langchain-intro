
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.schema import StrOutputParser # to parse output into string
from langchain.output_parsers.json import SimpleJsonOutputParser 

template = PromptTemplate.from_template(
    template="""
        You are an expert in picking fruits. 
        Your role is to teach a young adult how to pick the fruits that are crunchy and fresh at the grocery store.
       
        Teach me how to pick {fruit}"""
)

llm = Ollama(model="llama3:8b")

# response = llm.invoke(template.format(fruit="apple"))  # without chain

llm_chain = template | llm | StrOutputParser()
response = llm_chain.invoke({"fruit":"mango"})  # with chain

print(response)

