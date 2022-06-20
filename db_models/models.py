from flask_marshmallow import Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from . import db
from marshmallow import ValidationError, fields, pre_load

from datetime import datetime


# MODELS
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    orders = db.relationship('Order', backref='customers')

    def __repr__(self) -> str:
        return f"Customer_id: {self.id} | Customer_name: {self.name}"

    @classmethod
    def allItems(cls):
        return cls.query.all()
    
    @classmethod
    def customer_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @classmethod
    def delete(cls, id):
        customer = cls.customer_by_id(id)
        db.session.delete(customer)
        db.session.commit()


    

order_product = db.Table('order_product', 
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    shipped_date = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    products = db.relationship('Product', secondary=order_product, backref='orders', cascade="all, delete", passive_deletes=True)

    def __repr__(self) -> str:
        return f"Order_ID: {self.id}"

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        try:
            db.session.commit()
        except ValidationError as e:
            raise e

    @classmethod
    def allItems(cls):
        return cls.query.all()

    @classmethod
    def get_item(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def delete_item(cls, id):
        item = cls.get_item(id)
        db.session.delete(item)
        db.session.commit()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50), nullable=False)
    item_price = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Product_id: {self.id} | Product_name: {self.item_name}"

    @classmethod
    def allItems(cls):
        return cls.query.all()

    @classmethod
    def get_item(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update_item(cls, id, **kwargs):
        try:
            item = cls.get_item(id)
            item.item_name = kwargs.get('item_name')
            item.item_price = kwargs.get('item_price')
            db.session.commit()
        except ValidationError as e:
            raise e

    @classmethod
    def delete_item(cls, id):
        item = cls.get_item(id)
        db.session.delete(item)
        db.session.commit()



# SCHEMAS
class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product


class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order

    products = fields.Nested(ProductSchema(many=True))



class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

    orders = fields.Nested(OrderSchema(many=True))


class CustomerOrdersSchema(CustomerSchema):
    class Meta:
        exclude = ('orders',)


class OrdersByProductSchema(Schema):
    product_id = fields.Integer()
    product_name = fields.String()
    orders = fields.List(fields.Integer())


class OrderUpdateSchema(OrderSchema):
    order_id = fields.Integer(required=True)
    products = fields.List(fields.Integer(), required=True)

    @pre_load
    def check_products(self, data, **kwargs):
        # breakpoint()
        if not data.get("products"):
            raise ValidationError("Empty list provided")

        return data



def customer_validation(c_name):
    if len(c_name) < 3 or len(c_name) > 50:
        raise ValidationError("Name length should be in between 3 to 50 characters.")

    elif not c_name.replace(" ", "").isalpha():
        raise ValidationError("Name must only contain alphabatic characters.")



user_args ={
    "name": fields.String(required=True, validate=customer_validation),
    "email": fields.Email(required=True, ),
    "city": fields.String(required=True),
    "address": fields.String(required=True)
    }

