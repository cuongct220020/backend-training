# app/schemas/base_schema.py
from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    """
    A base schema for all other schemas in the application.
    It includes a common configuration.
    """
    model_config = ConfigDict(
        from_attributes=True,  # Equivalent to orm_mode = True in Pydantic v1
        extra='forbid',
        populate_by_name=True, # Cho phép dùng alias
        use_enum_values=True # Tự động chuyển Enum thành giá trị của nó
    )