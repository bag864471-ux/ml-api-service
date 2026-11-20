from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
import time
import structlog

from app.api.v1 import predict, models, monitoring
from app.config import settings
from app.core.model_manager import ModelManager

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
app = FastAPI(
    title="ML API Service",
    description="Production-ready machine learning API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        "request_processed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=process_time
    )

    return response

# Routes
app.include_router(predict.router, prefix="/api/v1", tags=["prediction"])
app.include_router(models.router, prefix="/api/v1/models", tags=["models"])
app.include_router(monitoring.router, prefix="/api/v1/monitoring", tags=["monitoring"])

# Metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Model manager
model_manager = ModelManager()

@app.on_event("startup")
async def startup_event():
    await model_manager.load_models()
    logger.info("application_started", models_loaded=len(model_manager.models))

@app.get("/")
async def root():
    return {
        "message": "ML API Service",
        "version": "1.0.0",
        "docs": "/docs",
        "metrics": "/metrics"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": len(model_manager.models)
    }
