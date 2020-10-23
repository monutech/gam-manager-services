from .client.dfp import Client
from googleads import (ad_manager as dfp, oauth2)


def get_orders(version='v202008'):
    """
    Gets all the orders.
    Returns a list of dictionaries, each order is it's own dictionary.
    """
    dfp_account = 20842576
    client = Client(code=dfp_account)
    # order_service = client.GetService('OrderService', version=version)
    statement = dfp.StatementBuilder(version=version)
    orders = []
    while True:
        response = client.order_service.getOrdersByStatement(statement.ToStatement())
        if 'results' in response and len(response['results']):
            for order in response['results']:
                orders.append(order)

            statement.offset += statement.limit
        else:
            break

    return orders


def get_line_items(version='v202008'):
    dfp_account = 20842576
    client = Client(code=dfp_account)
    # client = ad_manager.AdManagerClient.LoadFromStorage()
    # line_item_service = client.GetService('LineItemService', version='v202008')

    statement = dfp.StatementBuilder(version=version)
    line_items = []
    while True:
        response = client.li_service.getLineItemsByStatement(statement.ToStatement(
        ))
        if 'results' in response and len(response['results']):
            for line_item in response['results']:
                line_items.append(line_item)
            statement.offset += statement.limit
        else:
            break
    
    return line_items

