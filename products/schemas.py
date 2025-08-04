from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId


class ProductDBModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    description: Optional[str]
    vendor: str

    model_config = ConfigDict(
        validate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "examples": [
                {
                    "name": "Shampoo X",
                    "description": "Premium foaming shampoo",
                    "vendor": "vendor1"
                }
            ]
        }
    )


class ProductCreateModel(BaseModel):
    name: str
    description: Optional[str] = None


class ProductUpdateModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None