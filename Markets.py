from flask import Blueprint, jsonify
from src.models.user import db
from src.models.order import Order
from src.models.trade import Trade
from sqlalchemy import func
from datetime import datetime
import random

markets_bp = Blueprint('markets', __name__)

@markets_bp.route('/markets/overview', methods=['GET'])
def get_market_overview():
    """Get market overview with price data and statistics"""
    try:
        # Mock price data (in a real implementation, this would come from external APIs)
        mock_prices = {
            'BTC': {'price': 67234.50, 'change': 2.4, 'volume': 2100000},
            'ETH': {'price': 3456.78, 'change': 1.8, 'volume': 1800000},
            'USDT': {'price': 1.00, 'change': 0.1, 'volume': 5200000},
            'BNB': {'price': 432.15, 'change': -0.5, 'volume': 890000},
            'ADA': {'price': 0.85, 'change': 3.2, 'volume': 650000},
            'SOL': {'price': 145.67, 'change': -1.2, 'volume': 420000}
        }
        
        markets = []
        for crypto, data in mock_prices.items():
            # Add some randomness to make it look more realistic
            price_variation = random.uniform(-0.02, 0.02)
            current_price = data['price'] * (1 + price_variation)
            
            markets.append({
                'pair': f"{crypto}/USD",
                'price': round(current_price, 2),
                'change_24h': data['change'],
                'volume_24h': data['volume'],
                'high_24h': round(current_price * 1.05, 2),
                'low_24h': round(current_price * 0.95, 2)
            })
        
        return jsonify({
            'success': True,
            'markets': markets
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@markets_bp.route('/markets/stats', methods=['GET'])
def get_platform_stats():
    """Get platform statistics"""
    try:
        # Get real statistics from database
        total_trades = Trade.query.count()
        completed_trades = Trade.query.filter_by(status='completed').count()
        active_orders = Order.query.filter_by(status='active').count()
        
        # Calculate total volume (sum of completed trades)
        total_volume = db.session.query(func.sum(Trade.total_value)).filter_by(status='completed').scalar() or 0
        
        # Mock some additional stats
        stats = {
            'total_trades': max(total_trades, 50000),  # Show at least 50k for demo
            'active_users': max(total_trades * 2, 25000),  # Estimate active users
            'countries': 150,  # Mock data
            'trust_score': 4.9,
            'total_volume': max(total_volume, 10000000),  # Show at least 10M for demo
            'active_orders': active_orders,
            'completed_trades': completed_trades,
            'success_rate': round((completed_trades / max(total_trades, 1)) * 100, 1) if total_trades > 0 else 95.5
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@markets_bp.route('/markets/trending', methods=['GET'])
def get_trending_pairs():
    """Get trending trading pairs based on volume"""
    try:
        # Mock trending data
        trending = [
            {'pair': 'BTC/USD', 'volume_change': 15.2, 'trades_count': 1250},
            {'pair': 'ETH/USD', 'volume_change': 8.7, 'trades_count': 980},
            {'pair': 'USDT/USD', 'volume_change': 5.3, 'trades_count': 2100},
            {'pair': 'BNB/USD', 'volume_change': -2.1, 'trades_count': 450},
            {'pair': 'ADA/USD', 'volume_change': 12.8, 'trades_count': 320}
        ]
        
        return jsonify({
            'success': True,
            'trending': trending
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@markets_bp.route('/markets/price/<string:symbol>', methods=['GET'])
def get_price(symbol):
    """Get current price for a specific cryptocurrency"""
    try:
        symbol = symbol.upper()
        
        # Mock price data
        prices = {
            'BTC': 67234.50,
            'ETH': 3456.78,
            'USDT': 1.00,
            'BNB': 432.15,
            'ADA': 0.85,
            'SOL': 145.67
        }
        
        if symbol not in prices:
            return jsonify({'success': False, 'error': 'Symbol not found'}), 404
        
        # Add some randomness
        base_price = prices[symbol]
        current_price = base_price * (1 + random.uniform(-0.02, 0.02))
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'price': round(current_price, 2),
            'timestamp': int(datetime.utcnow().timestamp())
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
      
