from fastapi import FastAPI, APIRouter
from .crud_operations import router as applications_router

app = FastAPI()

v1_router = APIRouter(prefix="")

v1_router.include_router(applications_router, prefix="")

app.include_router(v1_router)