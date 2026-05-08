from sqlalchemy import BigInteger, VARCHAR
from sqlalchemy.orm import mapped_column
from common.base.base_model import BaseModel


class ComWallet(BaseModel):
    __tablename__ = 'com_wallets'

    user_id = mapped_column(BigInteger, nullable=False)
    code = mapped_column(VARCHAR(50))
    name = mapped_column(VARCHAR(255))
    type = mapped_column(VARCHAR(10))
