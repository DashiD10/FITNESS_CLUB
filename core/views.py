from django.shortcuts import render
from django.shortcuts import HttpResponse

def landing(request):
    """Обработчик главной страницы"""
    return HttpResponse("<h1>Главная страница</h1>")

def order_detail(request, order_id):
    """
    Отвечает за маршрут 'orders/<int:order_id>/'
    :param request: HttpRequest
    :param order_id: int (номер заказа)
    """
    return HttpResponse(f"<h1>Детали заказа {order_id}</h1>")

def thanks(request):
    return render(request, "core/thanks.html")
