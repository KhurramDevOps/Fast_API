from sqlmodel import SQLModel, Field
from uuid import UUID,uuid4
from datetime import datetime, timezone

class BaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: datetime  =Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime  =Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # explicitly 
    class Config:
        orm_mode = True
