import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.handlers import router

app = FastAPI()

# Add CORS middleware before including routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://qest-multi-agent.vercel.app"],  # No trailing slash!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional: Add logging middleware for debugging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("uvicorn.access")
    logger.info(f"Request: {request.method} {request.url} | Origin: {request.headers.get('origin')}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code} | Headers: {dict(response.headers)}")
    return response

# Include your API routers
app.include_router(router)

# Root endpoint for health check or welcome message
@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}
