"""
Elite Wall Pro - FastAPI Backend
Production-grade API for job costing application
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from config import settings
from database import get_supabase, init_database
from routers import auth, jobs, costs, customers, vendors, employees, tenants, receipts

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Elite Wall Pro API...")
    init_database()
    logger.info("Database connection established")
    yield
    # Shutdown
    logger.info("Shutting down Elite Wall Pro API...")


# Create FastAPI app
app = FastAPI(
    title="Elite Wall Pro API",
    description="Production-grade job costing API for construction companies",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": str(type(exc).__name__)}
    )


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint for load balancers"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0"
    }


# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """API root - returns basic info"""
    return {
        "name": "Elite Wall Pro API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(tenants.router, prefix="/api/v1/tenants", tags=["Tenants"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(costs.router, prefix="/api/v1/costs", tags=["Costs"])
app.include_router(customers.router, prefix="/api/v1/customers", tags=["Customers"])
app.include_router(vendors.router, prefix="/api/v1/vendors", tags=["Vendors"])
app.include_router(employees.router, prefix="/api/v1/employees", tags=["Employees"])
app.include_router(receipts.router, prefix="/api/v1/receipts", tags=["Receipts"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
