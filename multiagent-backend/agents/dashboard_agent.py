from crewai import Agent
from tools.mongodb_tool import MongoDBTool
from pydantic import PrivateAttr
from datetime import datetime
import re

class DashboardAgent(Agent):
    _mongo: MongoDBTool = PrivateAttr()

    def __init__(self, mongo_tool: MongoDBTool):
        super().__init__(
            role="Analytics Specialist",
            name="DashboardAgent",
            goal="Provide analytics and metrics useful for business owners.",
            backstory="An analytical agent for business metrics and dashboards.",
            tools=[mongo_tool]
        )
        object.__setattr__(self, "_mongo", mongo_tool)

    def handle_query(self, query: str):
        query_lower = query.lower()

        # 1. Revenue Metrics
        if "revenue" in query_lower or "total revenue" in query_lower:
            now = datetime.now()
            month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            pipeline = [
                {"$match": {
                    "status": "paid",
                    "paid_at": {"$gte": month_start.strftime("%Y-%m-%d")}
                }},
                {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
            ]
            result = self._mongo.aggregate("payments", pipeline)
            return {"total_revenue": result[0]["total"] if result else 0}

        elif "outstanding payment" in query_lower or "pending payment" in query_lower:
            pipeline = [
                {"$match": {"status": {"$ne": "paid"}}},
                {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
            ]
            result = self._mongo.aggregate("payments", pipeline)
            return {"outstanding_payments": result[0]["total"] if result else 0}

        # 2. Client Insights
        elif "inactive client" in query_lower:
            clients = self._mongo.find("clients", {"status": "inactive"})
            return {"inactive_clients": len(clients)}
        elif "active client" in query_lower:
            clients = self._mongo.find("clients", {"status": "active"})
            return {"active_clients": len(clients)}
        elif "birthday" in query_lower:
            today = datetime.now().strftime("%m-%d")
            clients = self._mongo.find("clients", {})
            birthday_clients = [
                c for c in clients if c.get("dob", "").endswith(today)
            ]
            return {"birthday_reminders": birthday_clients}
        elif "new client" in query_lower and "month" in query_lower:
            now = datetime.now()
            month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            clients = self._mongo.find("clients", {"created_at": {"$gte": month_start.strftime("%Y-%m-%d")}})
            return {"new_clients_this_month": len(clients)}

        # 3. Service Analytics
        elif "highest enrollment" in query_lower or "top course" in query_lower:
            pipeline = [
                {"$group": {"_id": "$service", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 1}
            ]
            result = self._mongo.aggregate("orders", pipeline)
            return {"top_course": result[0]["_id"] if result else None}
        elif "enrollment trend" in query_lower:
            pipeline = [
                {"$group": {
                    "_id": {"$substr": ["$created_at", 0, 7]},
                    "count": {"$sum": 1}
                }},
                {"$sort": {"_id": 1}}
            ]
            result = self._mongo.aggregate("orders", pipeline)
            return {"enrollment_trends": result}
        elif "completion rate" in query_lower:
            pipeline = [
                {"$group": {"_id": "$course_id", "completed": {"$sum": {"$cond": [{"$eq": ["$status", "completed"]}, 1, 0]}}, "total": {"$sum": 1}}},
                {"$project": {"completion_rate": {"$divide": ["$completed", "$total"]}}}
            ]
            result = self._mongo.aggregate("courses", pipeline)
            return {"course_completion_rates": result}

        # 4. Attendance Reports
        elif "attendance percentage" in query_lower:
            match = re.search(r'for ([\w\s]+)', query, re.IGNORECASE)
            if not match:
                return {"error": "Course name not found in query"}
            course_name = match.group(1).strip()
            classes = self._mongo.find("classes", {"course_id": course_name})
            class_ids = [c["_id"] for c in classes]
            total_attendance = self._mongo.find("attendance", {"class_id": {"$in": class_ids}})
            attended = [a for a in total_attendance if a.get("attended")]
            percentage = (len(attended) / len(total_attendance) * 100) if total_attendance else 0
            return {"attendance_percentage": percentage}

        elif "drop-off rate" in query_lower:
            pipeline = [
                {"$group": {"_id": "$client_id", "attended": {"$sum": {"$cond": ["$attended", 1, 0]}}}},
                {"$match": {"attended": {"$eq": 0}}}
            ]
            result = self._mongo.aggregate("attendance", pipeline)
            return {"drop_off_clients": [r["_id"] for r in result]}

        else:
            return {"error": "Query not understood. Please rephrase or provide more details."}
