from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from .models import Trainer, Review, Order
from .forms import ReviewForm, OrderForm

def landing(request):
    """Обработчик главной страницы"""
    trainers = Trainer.objects.filter(is_active=True)
    reviews = Review.objects.filter(is_published=True).select_related('trainer')
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
    order = get_object_or_404(Order.objects.select_related('trainer').prefetch_related('services').annotate(total_price=Sum('services__price')), pk=order_id)
    return render(request, "core/order_detail.html", {"order": order})

from django.db.models import Q

@login_required
def orders_list(request):
    """
    Отвечает за маршрут 'orders/'
    :param request: HttpRequest
    """
    search_query = request.GET.get('q', '').strip()
    search_name = request.GET.get('search_name', 'on') == 'on'
    search_phone = request.GET.get('search_phone') == 'on'
    search_comment = request.GET.get('search_comment') == 'on'

    orders = Order.objects.select_related('trainer').prefetch_related('services').all()

    if search_query:
        q_objects = Q()
        if search_name:
            q_objects |= Q(name__icontains=search_query)
        if search_phone:
            q_objects |= Q(phone__icontains=search_query)
        if search_comment:
            q_objects |= Q(comment__icontains=search_query)
        orders = orders.filter(q_objects)

    orders = orders.order_by('-date_created')

    context = {
        'orders': orders,
        'search_query': search_query,
        'search_name': search_name,
        'search_phone': search_phone,
        'search_comment': search_comment,
    }
    return render(request, "core/orders_list.html", context)

def thanks(request):
    return render(request, "core/thanks.html")

def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('thanks')
    else:
        form = ReviewForm()
    return render(request, 'core/create_review.html', {'form': form})

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thanks')
    else:
        form = OrderForm()
    return render(request, 'core/create_order.html', {'form': form})

def get_trainer_services(request, trainer_id):
    try:
        trainer = Trainer.objects.get(id=trainer_id)
        services = list(trainer.services.values('id', 'name'))
        return JsonResponse({'services': services})
    except Trainer.DoesNotExist:
        return JsonResponse({'error': 'Trainer not found'}, status=404)
