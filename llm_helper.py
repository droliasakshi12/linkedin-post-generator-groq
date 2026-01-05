from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os 

load_dotenv("api_key.env")

llm = ChatGroq(groq_api_key = os.getenv("groq_api_key"), model_name ="llama-3.1-8b-instant")


if __name__== "__main__" :  

    response = llm.invoke("give me the ingredients used in making samosa")
    print(response.content)
