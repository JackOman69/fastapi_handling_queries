import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from aiokafka import AIOKafkaProducer

from .settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from .models import Application
from .schemas import CreateApplicationRequest, CreateApplicationResponse, PaginationParams
from .database import db_session
from .logs.logger import logger


router = APIRouter()

@router.post("/application", summary="Создать новую заявку")
async def create_applications(db: Annotated[AsyncSession, Depends(db_session)], request_data: CreateApplicationRequest):
    logger.info(f"Создание новой заявки на имя: {request_data.user_name}")
    
    db_application = Application(user_name=request_data.user_name, description=request_data.description)
    db.add(db_application)  
    try:
        await db.commit()
        await db.refresh(db_application)
        logger.info(f"Заявка успешно создана с ID: {db_application.id}")
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()
        try:
            message = {
                "ID Заявки": db_application.id,
                "Пользователь": db_application.user_name,
                "Текст заявки": db_application.description,
                "Дата создания": str(db_application.created_at) 
            }
            logger.info(f"Отправка заявки в Kafka топик: {KAFKA_TOPIC}")
            await producer.send_and_wait(KAFKA_TOPIC, json.dumps(message).encode('utf-8'))
            logger.info(f"Сообщение было отправлено в Kafka - {message}")
        except Exception as e:
            logger.error(f"Kafka error: {str(e)}")
            return HTTPException(status_code=502, detail=f"{e}")
        finally:
            await producer.stop()
            return CreateApplicationResponse(
                id=db_application.id,
                user_name=db_application.user_name,
                description=db_application.description,
                created_at=db_application.created_at   
            )
    except Exception as e:
        logger.error(f"Ошибка с базой данных: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/application", summary="Получить заявку по имени пользователя")
async def get_applications(
    db: Annotated[AsyncSession, Depends(db_session)],
    user_name: str = None, 
    pagination: Annotated[PaginationParams, Depends()] = PaginationParams()
):
    
    logger.info(f"Получение заявки через запрос. Фильтр по имени: {user_name}, Страница: {pagination.page}, Количество элементов: {pagination.size}")
    
    query = select(Application)
    if user_name:
        query = query.where(Application.user_name == user_name)
    
    skip = (pagination.page - 1) * pagination.size
    
    result = await db.execute(query.offset(skip).limit(pagination.size))
    
    return result.scalars().all()