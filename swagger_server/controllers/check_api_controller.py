import connexion
import six
from swagger_server.models.order import Order  # noqa: E501
from swagger_server import util
import pymongo
import uuid
import time
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()




client=pymongo.MongoClient("mongodb://localhost:27017/verifili")
db=client['verifili']



@auth.verify_password
def verify_password(username, password):
    users=list(db.api_credentials.find({'status':'Active'}))
    print(username,password)
    for user in users:
        if user['username']== username:
            return check_password_hash(user['password'],password)
    return False



@auth.login_required
def create_order(Order=None):  # noqa: E501
    """creates an Order

    create an exisying Order # noqa: E501

    :param Order: Order  to add
    :type Order: dict | bytes

    :rtype: None
    """
    merchant_id=auth.username().split('_')[0]
    order_=connexion.request.get_json()
    order_['id']=str(uuid.uuid4())
    order_['created_time']=time.time()
    order_['updated_time']=time.time()
    order_['merchant_id']=merchant_id
    db.orders.insert(order_)
    order_.pop('_id')
    order_.pop('merchant_id')
    return order_

@auth.login_required
def getorder(OrderId):  # noqa: E501
    """read an order from Verifi.

    By passing in the appropriate options, you can search for available inventory in the system  # noqa: E501

    :param OrderId: id of the order
    :type OrderId: str

    :rtype: List[Order]
    """
    merchant_id=auth.username().split('_')[0]
    return db.orders.find_one({'id':OrderId,'merchant_id':merchant_id},{'_id':0,'merchant_id':0})

@auth.login_required
def update_order(OrderId, Order=None):  # noqa: E501
    """updates an Order

    update an exisying Order # noqa: E501

    :param OrderId: id of the order
    :type OrderId: str
    :param Order: Order  to update
    :type Order: dict | bytes

    :rtype: None
    """
    merchant_id=auth.username().split('_')[0]
    order_=connexion.request.get_json()
    order_['updated_time']=time.time()
    if merchant_id in order_ :
        order_.pop('merchant_id')
    
    db.orders.find_one_and_update({'id':OrderId,'merchant_id':merchant_id},{'$set':order_})
    return order_
