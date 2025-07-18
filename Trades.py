from flask import Blueprint, request, jsonify
from src.models.user import db, User
from src.models.order import Order
from src.models.trade import Trade
from datetime import datetime
import uuid

trades_bp = Blueprint('trades', __name__)

@trades_bp.route('/trades', methods=['GET'])
def get_trades():
    """Get all trades with optional filtering"""
    try:
        # Get query parameters
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        
        # Build query
        query = Trade.query
        
        if user_id:
            query = query.filter((Trade.buyer_id == user_id) | (Trade.seller_id == user_id))
        if status:
            query = query.filter_by(status=status)
            
        trades = query.order_by(Trade.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'trades': [trade.to_dict() for trade in trades]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@trades_bp.route('/trades', methods=['POST'])
def create_trade():
    """Initiate a trade from an existing order"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['order_id', 'buyer_id', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        # Get the order
        order = Order.query.get(data['order_id'])
        if not order:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
            
        if order.status != 'active':
            return jsonify({'success': False, 'error': 'Order is not active'}), 400
        
        # Validate buyer exists
        buyer = User.query.get(data['buyer_id'])
        if not buyer:
            return jsonify({'success': False, 'error': 'Buyer not found'}), 404
            
        # Validate amount doesn't exceed order amount
        if data['amount'] > order.amount:
            return jsonify({'success': False, 'error': 'Trade amount exceeds order amount'}), 400
        
        # Determine buyer and seller based on order type
        if order.order_type == 'sell':
            seller_id = order.user_id
            buyer_id = data['buyer_id']
        else:  # buy order
            seller_id = data['buyer_id']
            buyer_id = order.user_id
            
        # Calculate total value
        total_value = data['amount'] * order.price_per_unit
        
        # Generate escrow address (simplified - in real implementation this would be a real crypto address)
        escrow_address = f"escrow_{uuid.uuid4().hex[:16]}"
        
        # Create trade
        trade = Trade(
            order_id=data['order_id'],
            buyer_id=buyer_id,
            seller_id=seller_id,
            amount=data['amount'],
            price_per_unit=order.price_per_unit,
            total_value=total_value,
            status='pending',
            escrow_address=escrow_address
        )
        
        db.session.add(trade)
        
        # Update order amount
        order.amount -= data['amount']
        if order.amount <= 0:
            order.status = 'completed'
        order.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'trade': trade.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@trades_bp.route('/trades/<int:trade_id>', methods=['GET'])
def get_trade(trade_id):
    """Get a specific trade by ID"""
    try:
        trade = Trade.query.get(trade_id)
        if not trade:
            return jsonify({'success': False, 'error': 'Trade not found'}), 404
            
        return jsonify({
            'success': True,
            'trade': trade.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@trades_bp.route('/trades/<int:trade_id>/confirm-payment', methods=['POST'])
def confirm_payment(trade_id):
    """Buyer confirms payment has been sent"""
    try:
        trade = Trade.query.get(trade_id)
        if not trade:
            return jsonify({'success': False, 'error': 'Trade not found'}), 404
            
        data = request.get_json()
        user_id = data.get('user_id')
        
        # Verify the user is the buyer
        if user_id != trade.buyer_id:
            return jsonify({'success': False, 'error': 'Only buyer can confirm payment'}), 403
            
        if trade.status != 'pending':
            return jsonify({'success': False, 'error': 'Trade is not in pending status'}), 400
            
        trade.payment_confirmed = True
        trade.status = 'escrowed'
        trade.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'trade': trade.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@trades_bp.route('/trades/<int:trade_id>/release-crypto', methods=['POST'])
def release_crypto(trade_id):
    """Seller releases cryptocurrency after receiving payment"""
    try:
        trade = Trade.query.get(trade_id)
        if not trade:
            return jsonify({'success': False, 'error': 'Trade not found'}), 404
            
        data = request.get_json()
        user_id = data.get('user_id')
        
        # Verify the user is the seller
        if user_id != trade.seller_id:
            return jsonify({'success': False, 'error': 'Only seller can release crypto'}), 403
            
        if trade.status != 'escrowed':
            return jsonify({'success': False, 'error': 'Trade is not in escrowed status'}), 400
            
        trade.crypto_released = True
        trade.status = 'completed'
        trade.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'trade': trade.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@trades_bp.route('/trades/<int:trade_id>/dispute', methods=['POST'])
def create_dispute(trade_id):
    """Create a dispute for a trade"""
    try:
        trade = Trade.query.get(trade_id)
        if not trade:
            return jsonify({'success': False, 'error': 'Trade not found'}), 404
            
        data = request.get_json()
        user_id = data.get('user_id')
        
        # Verify the user is involved in the trade
        if user_id not in [trade.buyer_id, trade.seller_id]:
            return jsonify({'success': False, 'error': 'User not involved in this trade'}), 403
            
        if trade.status in ['completed', 'cancelled']:
            return jsonify({'success': False, 'error': 'Cannot dispute completed or cancelled trade'}), 400
            
        trade.status = 'disputed'
        trade.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'trade': trade.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@trades_bp.route('/trades/<int:trade_id>/cancel', methods=['POST'])
def cancel_trade(trade_id):
    """Cancel a trade (only if in pending status)"""
    try:
        trade = Trade.query.get(trade_id)
        if not trade:
            return jsonify({'success': False, 'error': 'Trade not found'}), 404
            
        data = request.get_json()
        user_id = data.get('user_id')
        
        # Verify the user is involved in the trade
        if user_id not in [trade.buyer_id, trade.seller_id]:
            return jsonify({'success': False, 'error': 'User not involved in this trade'}), 403
            
        if trade.status != 'pending':
            return jsonify({'success': False, 'error': 'Can only cancel pending trades'}), 400
            
        trade.status = 'cancelled'
        trade.updated_at = datetime.utcnow()
        
        # Return the amount back to the original order
        order = Order.query.get(trade.order_id)
        if order:
            order.amount += trade.amount
            if order.status == 'completed':
                order.status = 'active'
            order.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'trade': trade.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

                                
