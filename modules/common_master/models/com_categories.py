from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class ComCategory(BaseModel):
    __tablename__ = 'com_categories'

    code = mapped_column(VARCHAR(50))
    name = mapped_column(VARCHAR(255))
    type = mapped_column(VARCHAR(10))
