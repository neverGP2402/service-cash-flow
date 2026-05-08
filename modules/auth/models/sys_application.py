from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class SysApplication(BaseModel):
    __tablename__ = 'sys_application'

    name = mapped_column(VARCHAR(255), nullable=False)
    description = mapped_column(VARCHAR(255))
    version_mobile = mapped_column(VARCHAR(100))
    version_web = mapped_column(VARCHAR(100))
    author = mapped_column(VARCHAR(255))
    process_flag = mapped_column(VARCHAR(20))
