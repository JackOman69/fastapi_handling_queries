from pydantic import BaseModel, Field
from datetime import datetime

class ApplicationModel(BaseModel):
    id: int
    user_name: str
    description: str
    created_at: datetime

class CreateApplicationRequest(BaseModel):
    user_name: str
    description: str

class CreateApplicationResponse(ApplicationModel):
    pass
    
class RetrieveApplicationResponse(ApplicationModel):
    pass
    
class KafkaApplicationCreate(ApplicationModel):
    pass    
    
class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=10, gt=0, description="Number of items per page")
    
