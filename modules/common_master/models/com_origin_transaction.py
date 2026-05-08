from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class ComOriginTransaction(BaseModel):
    __tablename__ = 'com_origin_transaction'

    code = mapped_column(VARCHAR(50))
    name = mapped_column(VARCHAR(255))
