from flask import Blueprint, request, jsonify
from sqlalchemy import text
from extensions import WorkerSingleton
from database import db
from models import Order, OrderStatusEnum
import json

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/create_order', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(
        user_id=data['user_id'],
        total_amount=data['total_amount'],
        item_ids=json.dumps(data['item_ids']),
        status=OrderStatusEnum.PENDING
    )
    db.session.add(new_order)
    db.session.commit()

    # send to queue
    WorkerSingleton().getQ().put(new_order.id)

    response = jsonify({'message': 'Order created successfully!', 'data': data})
    response.headers.add('Content-Type', 'application/json')
    return response

@order_bp.route('/metrics', methods=['GET'])
def metrics():
    data = {
        'pending_count': 0,
        'processing_count': 0,
        'processed_count': 0,
        'total_orders': 0,
        'avg_processing_time': 0,
    }

    for order in Order.query.all():
        if order.status == OrderStatusEnum.PENDING:
            data['pending_count'] += 1
        elif order.status == OrderStatusEnum.PROCESSING:
            data['processing_count'] += 1
        elif order.status == OrderStatusEnum.COMPLETED:
            data['processed_count'] += 1

    data['total_orders'] = data['pending_count'] + data['processing_count'] + data['processed_count']

    # Custom SQL query to calculate average processing time
    result = db.session.execute(text("""
            SELECT AVG(TIMESTAMPDIFF(SECOND, started_at, completed_at)) AS avg_processing_time
            FROM orders 
            WHERE status='COMPLETED';
        """), {'status': OrderStatusEnum.COMPLETED.value})

    data['avg_processing_time'] = result.scalar()

    return jsonify(data)