from .client.dfp import Client


def get_orders(version='v202008'):
    """
    Gets all the orders.
    Returns a list of dictionaries, each order is it's own dictionary.
    """
    dfp_account = 20842576
    client = Client(code=dfp_account)
    # order_service = client.GetService('OrderService', version=version)
    statement = ad_manager.StatementBuilder(version=version)
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

