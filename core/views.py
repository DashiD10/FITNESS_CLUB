from django.shortcuts import render
from django.shortcuts import HttpResponse

def landing(request):
    """Обработчик главной страницы"""
    # Optionally, add masters and services data here if available
    return render(request, "core/landing.html")

def order_detail(request, order_id):
    """
    Отвечает за маршрут 'orders/<int:order_id>/'
    :param request: HttpRequest
    :param order_id: int (номер заказа)
    """
    # Mock order data for demonstration
    orders = {
        1: {"client_name": "Иван Иванов", "status": "В обработке", "details": "Заказ на фитнес тренировки"},
        2: {"client_name": "Мария Петрова", "status": "Завершен", "details": "Заказ на йогу"},
    }
    order = orders.get(order_id)
    if not order:
        return HttpResponse(f"<h1>Заказ с ID {order_id} не найден</h1>", status=404)
    return render(request, "core/order_detail.html", {"order": order})

def orders_list(request):
    """
    Отвечает за маршрут 'orders/'
    :param request: HttpRequest
    """
    # Mock orders data for demonstration
    orders = [
        {"id": 1, "client_name": "Иван Иванов", "status": "В обработке"},
        {"id": 2, "client_name": "Мария Петрова", "status": "Завершен"},
    ]
    return render(request, "core/orders_list.html", {"orders": orders})

def thanks(request):
    return render(request, "core/thanks.html")
