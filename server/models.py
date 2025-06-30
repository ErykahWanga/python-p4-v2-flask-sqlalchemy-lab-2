from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Relationship with Review
    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')
    
    # Association proxy to get items through reviews
    items = association_proxy('reviews', 'item')

    # Serialization rules to avoid recursion
    serialize_rules = ('-reviews.customer',)

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Relationship with Review
    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan')

    # Serialization rules to avoid recursion
    serialize_rules = ('-reviews.item',)

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # Relationships with Customer and Item
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    # Serialization rules to avoid recursion
    serialize_rules = ('-customer.reviews', '-item.reviews')