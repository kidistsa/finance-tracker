from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime

from app.core.config import settings
from app.api.routes import transactions, budgets, auth, plaid, recurring, email, admin, security, receipt_scanner, analytics
from app.core.firebase import firebase_client

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# CORS - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_STR)
app.include_router(transactions.router, prefix=settings.API_STR)
app.include_router(budgets.router, prefix=settings.API_STR)
app.include_router(recurring.router, prefix=settings.API_STR)
app.include_router(email.router, prefix=settings.API_STR)
app.include_router(admin.router, prefix=settings.API_STR)
app.include_router(security.router, prefix=settings.API_STR)
# app.include_router(receipt_scanner.router, prefix=settings.API_STR)
app.include_router(analytics.router, prefix=settings.API_STR)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Personal Finance Tracker API")
    try:
        firebase_client.get_db()
        logger.info("Firebase initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")
        if not settings.DEBUG:
            raise e

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Personal Finance Tracker API")

@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=9000,
        reload=settings.DEBUG,
        log_level="info"
    )
