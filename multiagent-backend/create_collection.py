from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["mydb"]

# Sample documents
db.clients.insert_one({
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "enrolled_services": ["Yoga Beginner"],
    "status": "active",
    "dob": "1990-07-03",
    "created_at": "2025-07-01"
})

db.orders.insert_one({
    "_id": "12345",
    "client_id": "1",
    "service": "Yoga Beginner",
    "status": "paid",
    "created_at": "2025-07-01",
    "amount": 100.0
})

db.payments.insert_one({
    "order_id": "12345",
    "amount": 100.0,
    "status": "paid",
    "paid_at": "2025-07-02"
})

db.courses.insert_one({
    "name": "Yoga Beginner",
    "instructor": "Alice",
    "status": "upcoming",
    "start_date": "2025-07-10",
    "end_date": "2025-08-10"
})

db.classes.insert_one({
    "course_id": "Yoga Beginner",
    "date": "2025-07-12",
    "instructor": "Alice",
    "status": "scheduled"
})

db.attendance.insert_one({
    "class_id": "Yoga Beginner",
    "client_id": "1",
    "attended": True
})

print("Sample data inserted!")
