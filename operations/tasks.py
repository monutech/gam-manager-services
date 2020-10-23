from .client.dfp import Client


def get_orders(version='v202008'):
    """
    Gets all the orders.
    Returns a list of dictionaries, each order is it's own dictionary.
    """
    client = Client()
    order_service = client.GetService('OrderService', version=version)
    statement = ad_manager.StatementBuilder(version=version)
    orders = []
    while True:
        response = order_service.getOrdersByStatement(statement.ToStatement())
        if 'results' in response and len(response['results']):
            for order in response['results']:
                orders.append(order)

            statement.offset += statement.limit
        else:
            break

    return orders

