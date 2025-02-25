from database import db
from sqlalchemy import Enum
import json
import enum

class OrderStatusEnum(enum.Enum):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING, nullable=False)
    item_ids = db.Column(db.String(1000), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    @property
    def item_list(self):
        return json.loads(self.items)
