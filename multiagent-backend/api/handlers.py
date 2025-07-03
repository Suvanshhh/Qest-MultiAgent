from fastapi import APIRouter
from schemas.query_request import QueryRequest  # <-- import your new schema
from tools.mongodb_tool import MongoDBTool
from tools.external_api import CreateOrderTool, CreateClientTool
from agents.support_agent import SupportAgent
from agents.dashboard_agent import DashboardAgent

router = APIRouter()

mongo_tool = MongoDBTool("mongodb://localhost:27017", "mydb")
create_order_tool = CreateOrderTool()
create_client_tool = CreateClientTool()

support_agent = SupportAgent(mongo_tool, create_order_tool, create_client_tool)
dashboard_agent = DashboardAgent(mongo_tool)

@router.post("/support/query")
async def support_query(request: QueryRequest):
    return support_agent.handle_query(request.query)

@router.post("/dashboard/query")
async def dashboard_query(request: QueryRequest):
    return dashboard_agent.handle_query(request.query)
