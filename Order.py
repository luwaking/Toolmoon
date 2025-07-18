from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_type = db.Column(db.String(10), nullable=False)  # 'buy' or 'sell'
    cryptocurrency = db.Column(db.String(10), nullable=False)  # 'BTC', 'ETH', etc.
    fiat_currency = db.Column(db.String(10), nullable=False)  # 'USD', 'EUR', etc.
    amount = db.Column(db.Float, nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='active')  # 'active', 'completed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'order_type': self.order_type,
            'cryptocurrency': self.cryptocurrency,
            'fiat_currency': self.fiat_currency,
            'amount': self.amount,
            'price_per_unit': self.price_per_unit,
            'total_value': self.total_value,
            'payment_method': self.payment_method,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user': self.user.username if self.user else None
        }

