from fastapi import APIRouter
from schemas.query_request import QueryRequest
from tools.mongodb_tool import MongoDBTool
from tools.external_api import CreateOrderTool, CreateClientTool
from agents.support_agent import SupportAgent
from agents.dashboard_agent import DashboardAgent

router = APIRouter()

# Define your MongoDB URI and DB name
MONGO_URI = "mongodb+srv://Suvanshh:bB632221010@cluster0.pkiya.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "mydb"

# Initialize mongo_tool BEFORE using it
mongo_tool = MongoDBTool(MONGO_URI, DB_NAME)

# Initialize other tools
create_order_tool = CreateOrderTool()
create_client_tool = CreateClientTool()

# Now create your agents using the initialized tools
support_agent = SupportAgent(mongo_tool, create_order_tool, create_client_tool)
dashboard_agent = DashboardAgent(mongo_tool)

@router.post("/support/query")
async def support_query(request: QueryRequest):
    return support_agent.handle_query(request.query)

@router.post("/dashboard/query")
async def dashboard_query(request: QueryRequest):
    return dashboard_agent.handle_query(request.query)
