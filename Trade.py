from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    total_value = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'escrowed', 'completed', 'disputed', 'cancelled'
    escrow_address = db.Column(db.String(100))  # Crypto address for escrow
    payment_confirmed = db.Column(db.Boolean, default=False)
    crypto_released = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', backref=db.backref('trades', lazy=True))
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref=db.backref('buyer_trades', lazy=True))
    seller = db.relationship('User', foreign_keys=[seller_id], backref=db.backref('seller_trades', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'buyer_id': self.buyer_id,
            'seller_id': self.seller_id,
            'amount': self.amount,
            'price_per_unit': self.price_per_unit,
            'total_value': self.total_value,
            'status': self.status,
            'escrow_address': self.escrow_address,
            'payment_confirmed': self.payment_confirmed,
            'crypto_released': self.crypto_released,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'buyer': self.buyer.username if self.buyer else None,
            'seller': self.seller.username if self.seller else None
        }

