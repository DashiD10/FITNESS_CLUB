from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trainer, Review, Order

def landing(request):
    """Обработчик главной страницы"""
    trainers = Trainer.objects.filter(is_active=True)
    reviews = Review.objects.filter(is_published=True)
    context = {
        'trainers': trainers,
        'reviews': reviews,
    }
    return render(request, "core/landing.html", context)

@login_required
def order_detail(request, order_id):
    """
    Отвечает за маршрут 'orders/<int:order_id>/'
    :param request: HttpRequest
    :param order_id: int (номер заказа)
    """
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "core/order_detail.html", {"order": order})

@login_required
def orders_list(request):
    """
    Отвечает за маршрут 'orders/'
    :param request: HttpRequest
    """
    orders = Order.objects.all().order_by('-date_created')
    return render(request, "core/orders_list.html", {"orders": orders})

def thanks(request):
    return render(request, "core/thanks.html")
