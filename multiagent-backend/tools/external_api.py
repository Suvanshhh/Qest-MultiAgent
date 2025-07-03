from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class CreateOrderInput(BaseModel):
    client_id: str
    service: str

class CreateOrderTool(BaseTool):
    name: str = "Create Order Tool"
    description: str = "Creates an order via external API."
    args_schema: Type[BaseModel] = CreateOrderInput

    def _run(self, client_id: str, service: str):
        return {"status": "success", "order_id": "new_order_id"}

class CreateClientInput(BaseModel):
    name: str

class CreateClientTool(BaseTool):
    name: str = "Create Client Tool"
    description: str = "Creates a client via external API."
    args_schema: Type[BaseModel] = CreateClientInput

    def _run(self, name: str):
        return {"status": "success", "client_id": "new_client_id"}
