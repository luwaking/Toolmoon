from flask import Blueprint, request, jsonify
from src.models.user import db, User
from src.models.order import Order
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    """Get all active orders with optional filtering"""
    try:
        # Get query parameters
        order_type = request.args.get('type')  # 'buy' or 'sell'
        cryptocurrency = request.args.get('crypto')
        fiat_currency = request.args.get('fiat')
        
        # Build query
        query = Order.query.filter_by(status='active')
        
        if order_type:
            query = query.filter_by(order_type=order_type)
        if cryptocurrency:
            query = query.filter_by(cryptocurrency=cryptocurrency.upper())
        if fiat_currency:
            query = query.filter_by(fiat_currency=fiat_currency.upper())
            
        orders = query.order_by(Order.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'orders': [order.to_dict() for order in orders]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    """Create a new buy/sell order"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'order_type', 'cryptocurrency', 'fiat_currency', 
                          'amount', 'price_per_unit', 'payment_method']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        # Validate user exists
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
            
        # Calculate total value
        total_value = data['amount'] * data['price_per_unit']
        
        # Create order
        order = Order(
            user_id=data['user_id'],
            order_type=data['order_type'].lower(),
            cryptocurrency=data['cryptocurrency'].upper(),
            fiat_currency=data['fiat_currency'].upper(),
            amount=data['amount'],
            price_per_unit=data['price_per_unit'],
            total_value=total_value,
            payment_method=data['payment_method']
        )
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'order': order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order by ID"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
            
        return jsonify({
            'success': True,
            'order': order.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@orders_bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Update an order (e.g., cancel it)"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
            
        data = request.get_json()
        
        # Update allowed fields
        if 'status' in data:
            order.status = data['status']
        if 'amount' in data:
            order.amount = data['amount']
            order.total_value = order.amount * order.price_per_unit
        if 'price_per_unit' in data:
            order.price_per_unit = data['price_per_unit']
            order.total_value = order.amount * order.price_per_unit
            
        order.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'order': order.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@orders_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete/cancel an order"""
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
            
        order.status = 'cancelled'
        order.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order cancelled successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@orders_bp.route('/users/<int:user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    """Get all orders for a specific user"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
            
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'orders': [order.to_dict() for order in orders]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

