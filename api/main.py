from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_headers = ["*"],
    allow_methods = ["*"]
)

llm = ChatOpenAI(
   
    base_url = "https://api.groq.com/openai/v1",
    model = "llama-3.3-70b-versatile",
)


def startNode(state):
    input = state["qn"]
    res = llm.invoke(input)
    return {"response":res}

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["mydatabase"]
collections = db["users"]

class User(BaseModel):
    bio:str

class state(dict):
    pass


@app.get("/")
async def startFun():
    try:
        res = await client.admin.command("ping")
        res = await collections.delete_many({})
        
    except Exception as e:
        return {"response":str(e)}
    



@app.post("/adduser")
async def Adduser(user:User):
    res = await collections.insert_one(user.model_dump())
    return {"response":"user inserted successfully"}


graph = StateGraph(state)
graph.add_node("startNode", startNode)
graph.set_entry_point("startNode")


app_graph = graph.compile()

@app.get("/getdata")
async def getData():
    try:
        res = await collections.find_one({"id":1})
        return {"response":str(res)}
    except Exception as e:
        return {"response":str(e)}
    