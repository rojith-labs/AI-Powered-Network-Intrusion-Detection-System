from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.dashboard import router as dashboard_router
from app.api.alerts import router as alerts_router
from app.api.predict import router as predict_router
from app.api.analyze_pcap import router as analyze_pcap_router
from app.api.traffic import router as traffic_router
from app.api.analytics import router as analytics_router
from app.api.models import router as models_router
from app.api.websocket import router as ws_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(dashboard_router, tags=["Dashboard"])
api_router.include_router(alerts_router, tags=["Alerts"])
api_router.include_router(predict_router, tags=["Prediction"])
api_router.include_router(analyze_pcap_router, tags=["PCAP Analysis"])
api_router.include_router(traffic_router, tags=["Traffic"])
api_router.include_router(analytics_router, tags=["Analytics"])
api_router.include_router(models_router, tags=["Models"])
api_router.include_router(ws_router, tags=["WebSocket"])
