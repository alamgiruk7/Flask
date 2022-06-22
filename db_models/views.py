from datetime import datetime, timedelta
from http.client import OK

from db_models import db
from flask import Blueprint, make_response, request, jsonify
from .models import (
    Customer, 
    CustomerSchema, 
    OrderSchema,
    OrderUpdateSchema,
    OrdersByProductSchema,
    Product, 
    Order, 
    ProductSchema,
    CustomerOrdersSchema,
    user_args,
    order_product
)
from webargs.flaskparser import use_args
from webargs import fields


bp = Blueprint('views', __name__)


@bp.route('/add_customer', methods=['POST'])
@use_args(user_args, location='json')
def add_customer(args):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        city = data.get('city')
        address = data.get('address')
        
        customer = Customer(name=name, email=email, city=city, address=address)
        customer.save()
        schema = CustomerOrdersSchema().dump(customer)

        return jsonify(schema)
    except Exception as e:
        return jsonify({"Error": e.name}), e.code


@bp.route('/customers', methods=['GET'])
def showAllCustomers():
    customers = Customer.allItems()
    result = CustomerOrdersSchema(many=True).dump(customers)
    return jsonify(result), OK


@bp.route('/update/customer/<int:id>', methods=['PUT'])
@use_args(user_args, location='json')
def updateCustomer(args, id):
    customer = Customer.customer_by_id(id)
    customer.name = args.get('name')
    customer.email = args.get('email')
    customer.city = args.get('city')
    customer.address = args.get('address')

    customer.update()

    schema = CustomerOrdersSchema().dump(customer)

    return jsonify(schema)


@bp.route('/customer/delete/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        Customer.delete(id)
        return jsonify({"message": "customer deleted successfully."}), OK
    except Exception as e:
        return make_response(jsonify({"error": e.name}), e.code)


@bp.route('/add_product', methods=['POST'])
@use_args(
    {
    "item_name": fields.String(required=True),
    "item_price": fields.Integer(required=True),
    },
    location="json",
)
def add_product(args):
    item_name = args.get('item_name')
    item_price = args.get('item_price')

    item = Product(item_name=item_name, item_price=item_price)

    item.save()

    return {"message": "Item Added!"}


@bp.route('/', methods=['GET'])
def View_All_Items():
    items = Product.allItems()
    schema = ProductSchema(many=True)


    list_items = schema.dump(items)

    return jsonify(list_items), OK


@bp.route('/product/<int:id>', methods=['GET'])
def get_item(id):
    item_found = Product.get_item(id)
    schema = ProductSchema()

    dump_item = schema.dump(item_found)
    
    return jsonify(dump_item), 201


@bp.route('/product/update/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        item_to_update = request.get_json()
        Product.update_item(id, **item_to_update)

        schema = ProductSchema()
        schema_update = schema.dump(item_to_update)

        return jsonify(schema_update), 201
    except Exception as e:
        return jsonify(
            {
                "Error": e.name
            }
        ), 404



@bp.route('/product/delete/<int:id>', methods=['DELETE'])
def delete_product(id):
    """Delete Products from Order"""
    Product.delete_item(id)

    return jsonify({"message": "Item Deleted!"}), 201



@bp.route('/customer/orders/<int:id>', methods=['GET'])
def customer_orders(id):
    item = Customer.customer_by_id(id)
    schema = CustomerSchema().dump(item)
    return jsonify(schema), OK


@bp.route('/place_order', methods=['Post'])
@use_args(
    {
    "ids": fields.DelimitedList(fields.Integer, required=True),
    },
    location="json",
)
def place_order(args):
    products = [Product.get_item(i) for i in args.get('ids')]

    order = Order(customer_id=2, products= products)
    order.save()

    order_schema = OrderSchema().dump(order)

    return jsonify(order_schema), OK



@bp.route('/orders_by_product/<int:id>', methods=['GET'])
def orders_by_product(id):
    product = Product.get_item(id)
    orders = product.orders

    all_orders = dict(product_id=product.id, product_name=product.item_name, orders=orders)
    schema = OrdersByProductSchema().dump(all_orders)

    return schema


@bp.route('/orders', methods=['GET'])
def orders():
    query = Order.allItems()

    schema = OrderSchema().dump(query, many=True)

    return jsonify(schema)



@bp.route('/order/<int:id>', methods=['GET'])
def order_by_id(id):
    query = Order.get_item(id)

    

    schema = OrderSchema().dump(query)

    return jsonify(schema), OK




@bp.route('/revenue/<int:days>', methods=['GET'])
def get_revenue(days):
    revenue = db.session.query(
        db.func.sum(Product.item_price)).join(order_product).join(Order).filter(
            Order.order_date > (datetime.now() - timedelta(days=days))
            ).scalar()
    
    revenue = dict(revenue=revenue)

    return jsonify(revenue)



@bp.route('/order/delete/<int:id>', methods=['DELETE'])
def delete_order(id):
    """Delete Order"""
    Order.delete_item(id)

    return jsonify({"message": "Item Deleted!"}), OK



@bp.route('/update/order', methods=['PUT'])
@use_args(
    OrderUpdateSchema,
    location="json",
)
def update_order(args):
    try:
        order = Order.get_item(args.get('order_id'))
        order.products.clear()
        products = [Product.get_item(i) for i in args.get('products')]
        order.products = products
        order.update()
        result = OrderSchema().dump(order)
        return jsonify(result), OK
    except Exception as e:
        return make_response(jsonify({"Error":e.name}), e.code)

