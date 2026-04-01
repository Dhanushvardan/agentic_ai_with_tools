from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
from pymongo import ReturnDocument
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS


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
    input = state["input"]
    qn = state["qn"]
    doc = Document(page_content=input,metadata={id:1})
    embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(doc,embeddings)
    retriever = vectorstore.as_retriever()
    dddd = retriever.get_relevant_documents(qn)
    context = "\n".join([d.page_content for d in dddd])
    return {"qn":qn,"ct":context}


def ragNode(state):
    ct = state["ct"]
    qn = state["qn"]
    res = llm.invoke("the context is " + ct +" now answer for " + an)
    return {"response":res.content}
    

    

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["mydatabase"]
collections = db["t"]

class t(BaseModel):
    id : int
    bio:str

class tt(BaseModel):
    msg : str

async def get_next_id():
    counter = await db.counters.find_one_and_update(
        {"_id": "user_id"},
        {"$inc": {"sequence_value": 1}},
        return_document=ReturnDocument.AFTER,
        upsert=True
    )
    return counter["sequence_value"]
class state(dict):
    pass


@app.get("/")
async def startFun():
    try:
        res = await client.admin.command("ping")
        d =  collections.find()
        dt = []
        async for dc in d:
            dc["_id"] = str(dc["_id"])
            dt.append(dc)

        for dd in dt:
            print(dd)
        return {"response":"connection established"}
        
    except Exception as e:
        return {"response":str(e)}
    



@app.post("/adduser")
async def Adduser(user:t):
    data = user.model_dump()
    data["id"] = await get_next_id()
    res = await collections.insert_one(data)
    return {"response":"user inserted successfully"}


graph = StateGraph(state)
graph.add_node("startNode", startNode)
graph.set_entry_point("startNode")


app_graph = graph.compile()

@app.get("/getdata")
async def getData():
    try:
        res = await collections.find_one({"id":3})
        print(res)
        return {"response":str(res["bio"])}
    except Exception as e:
        return {"response":str(e)}



@app.post("/askai")
async def askai(msg : tt):
    res =await collections.find_one({"id":3})
    res = str(res["bio"])
    
    op = app_graph.invoke({"input":res,"qn":msg})
    return {"response":op["response"]}
    

