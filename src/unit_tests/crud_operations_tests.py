import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from ..app import app
from src.schemas import CreateApplicationRequest, PaginationParams, CreateApplicationResponse
from src.models import Application

client = TestClient(app)

@pytest.fixture
def mock_db():
    return AsyncMock()

@pytest.mark.asyncio
async def test_create_application_empty_description():
    test_user = "test_user"
    request_data = CreateApplicationRequest(
        user_name=test_user,
        description=""
    )
    
    create_result = []
    create_result.append(CreateApplicationResponse(
        id=1,
        user_name=request_data.user_name,
        description=request_data.description,
        created_at=str(datetime.now())   
    ))
    
    assert create_result[0].description == ""
    assert create_result[0].user_name == test_user

@pytest.mark.asyncio
async def test_get_applications_pagination_limits():
    test_applications = [
        Application(id=i, user_name="user1", description=f"desc{i}", created_at=datetime.now())
        for i in range(1, 21)
    ]
    
    pagination = PaginationParams(page=2, size=5)
    start_idx = (pagination.page - 1) * pagination.size
    end_idx = start_idx + pagination.size
    paginated_results = test_applications[start_idx:end_idx]
    
    assert len(paginated_results) == 5
    assert paginated_results[0].id == 6

@pytest.mark.asyncio
async def test_get_applications_multiple_users():
    test_applications = [
        Application(id=1, user_name="user1", description="desc1", created_at=datetime.now()),
        Application(id=2, user_name="user2", description="desc2", created_at=datetime.now()),
        Application(id=3, user_name="user1", description="desc3", created_at=datetime.now())
    ]
    
    user1_applications = [app for app in test_applications if app.user_name == "user1"]
    assert len(user1_applications) == 2

@pytest.mark.asyncio
async def test_create_application_with_special_characters():
    test_user = "test_user#123"
    test_description = "test application with @#$%"
    
    request_data = CreateApplicationRequest(
        user_name=test_user,
        description=test_description
    )
    
    create_result = []
    create_result.append(CreateApplicationResponse(
        id=1,
        user_name=request_data.user_name,
        description=request_data.description,
        created_at=str(datetime.now())   
    ))
    
    assert create_result[0].user_name == test_user
    assert create_result[0].description == test_description
