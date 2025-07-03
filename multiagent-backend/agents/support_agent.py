from crewai import Agent
from tools.mongodb_tool import MongoDBTool
from tools.external_api import CreateOrderTool, CreateClientTool
from pydantic import PrivateAttr
from utils import fix_mongo_ids  # <-- Make sure this import works
import re

class SupportAgent(Agent):
    _mongo: MongoDBTool = PrivateAttr()
    _create_order_tool: CreateOrderTool = PrivateAttr()
    _create_client_tool: CreateClientTool = PrivateAttr()

    def __init__(self, mongo_tool: MongoDBTool, create_order_tool: CreateOrderTool, create_client_tool: CreateClientTool):
        super().__init__(
            role="Support Specialist",
            name="SupportAgent",
            goal="Support service-related queries like course/class details, order/payment status, and client enquiries.",
            backstory="A helpful support agent for managing client and order queries.",
            tools=[mongo_tool, create_order_tool, create_client_tool]
        )
        object.__setattr__(self, "_mongo", mongo_tool)
        object.__setattr__(self, "_create_order_tool", create_order_tool)
        object.__setattr__(self, "_create_client_tool", create_client_tool)

    def handle_query(self, query: str):
        query_lower = query.lower()

        # 1. Class Discovery
        if "class" in query_lower and ("available" in query_lower or "this week" in query_lower):
            classes = self._mongo.find("classes", {"status": "scheduled"})
            return {"classes": fix_mongo_ids(classes)}

        # 2. Order Payment Status
        elif "order" in query_lower and "paid" in query_lower:
            match = re.search(r'#(\d+)', query)
            if not match:
                return {"error": "Order ID not found in query"}
            order_id = match.group(1)
            payment = self._mongo.find("payments", {"order_id": order_id, "status": "paid"})
            return {"order_id": order_id, "paid": bool(payment)}

        # 3. Create Order
        elif "create order" in query_lower:
            match = re.search(r'for (.+) for client (.+)', query, re.IGNORECASE)
            if not match:
                return {"error": "Could not parse client or service from query"}
            service = match.group(1).strip()
            client_name = match.group(2).strip()
            client = self._mongo.find("clients", {"name": client_name})
            if client and isinstance(client, list) and len(client) > 0:
                client_id = client[0]["_id"]
                result = self._create_order_tool._run(client_id=client_id, service=service)
                return {"result": result}
            else:
                return {"error": f"Client '{client_name}' not found"}

        # 4. Client Data Search
        elif "client" in query_lower and ("search" in query_lower or "find" in query_lower):
            email_match = re.search(r'email\s+([\w\.-]+@[\w\.-]+)', query, re.IGNORECASE)
            phone_match = re.search(r'phone\s+(\d+)', query, re.IGNORECASE)
            name_match = re.search(r'name\s+([a-zA-Z ]+)', query, re.IGNORECASE)
            if email_match:
                email = email_match.group(1)
                clients = self._mongo.find("clients", {"email": email})
            elif phone_match:
                phone = phone_match.group(1)
                clients = self._mongo.find("clients", {"phone": phone})
            elif name_match:
                name = name_match.group(1).strip()
                clients = self._mongo.find("clients", {"name": name})
            else:
                return {"error": "No valid identifier (name/email/phone) found in query"}
            return {"clients": fix_mongo_ids(clients)}

        # 5. Order Management
        elif "order" in query_lower and ("status" in query_lower or "get" in query_lower):
            match = re.search(r'id\s*(\d+)', query, re.IGNORECASE)
            if match:
                order_id = match.group(1)
                orders = self._mongo.find("orders", {"_id": order_id})
                return {"orders": fix_mongo_ids(orders)}
            else:
                return {"error": "Order ID not found in query"}

        # 6. Payment Info
        elif "payment" in query_lower and ("details" in query_lower or "dues" in query_lower):
            match = re.search(r'order\s*(\d+)', query, re.IGNORECASE)
            if match:
                order_id = match.group(1)
                payments = self._mongo.find("payments", {"order_id": order_id})
                return {"payments": fix_mongo_ids(payments)}
            else:
                return {"error": "Order ID not found in query"}

        # 7. Course Discovery
        elif "course" in query_lower and ("list" in query_lower or "upcoming" in query_lower):
            courses = self._mongo.find("courses", {"status": "upcoming"})
            return {"courses": fix_mongo_ids(courses)}

        # 8. External API Usage for Client Enquiry
        elif "create enquiry" in query_lower or "new client" in query_lower:
            match = re.search(r'client (.+)', query, re.IGNORECASE)
            if match:
                client_name = match.group(1).strip()
                result = self._create_client_tool._run(name=client_name)
                return {"result": result}
            else:
                return {"error": "Client name not found in query"}

        # Fallback
        else:
            return {"error": "Query not understood. Please rephrase or provide more details."}
