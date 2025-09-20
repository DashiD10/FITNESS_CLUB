from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Trainer, Review, Order
from .forms import ReviewForm, OrderForm

class LandingView(TemplateView):
    """Классовое представление для главной страницы"""
    template_name = 'core/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trainers'] = Trainer.objects.filter(is_active=True)
        context['reviews'] = Review.objects.filter(is_published=True).select_related('trainer')
        return context

@login_required
def order_detail(request, order_id):
    """
    Отвечает за маршрут 'orders/<int:order_id>/'
    :param request: HttpRequest
    :param order_id: int (номер заказа)
    """
    order = get_object_or_404(Order.objects.select_related('trainer').prefetch_related('services').annotate(total_price=Sum('services__price')), pk=order_id)
    return render(request, "core/order_detail.html", {"order": order})


class OrderDetailView(LoginRequiredMixin, DetailView):
    """Классовое представление для детальной информации о заявке"""
    model = Order
    template_name = 'core/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('trainer').prefetch_related('services').annotate(total_price=Sum('services__price'))

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


class OrdersListView(LoginRequiredMixin, ListView):
    """Классовое представление для списка заявок с поиском"""
    model = Order
    template_name = 'core/orders_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('trainer').prefetch_related('services')

        search_query = self.request.GET.get('q', '').strip()
        search_name = self.request.GET.get('search_name', 'on') == 'on'
        search_phone = self.request.GET.get('search_phone') == 'on'
        search_comment = self.request.GET.get('search_comment') == 'on'

        if search_query:
            q_objects = Q()
            if search_name:
                q_objects |= Q(name__icontains=search_query)
            if search_phone:
                q_objects |= Q(phone__icontains=search_query)
            if search_comment:
                q_objects |= Q(comment__icontains=search_query)
            queryset = queryset.filter(q_objects)

        return queryset.order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_query': self.request.GET.get('q', ''),
            'search_name': self.request.GET.get('search_name', 'on') == 'on',
            'search_phone': self.request.GET.get('search_phone') == 'on',
            'search_comment': self.request.GET.get('search_comment') == 'on',
        })
        return context

class ThanksView(TemplateView):
    """Классовое представление для страницы благодарности"""
    template_name = 'core/thanks.html'

def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш отзыв успешно создан!')
            return redirect('thanks')
    else:
        form = ReviewForm()
    return render(request, 'core/create_review.html', {'form': form})


class ReviewCreateView(CreateView):
    """Классовое представление для создания отзыва"""
    model = Review
    form_class = ReviewForm
    template_name = 'core/create_review.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        messages.success(self.request, 'Ваш отзыв успешно создан!')
        return super().form_valid(form)

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваша запись успешно принята!')
            return redirect('thanks')
    else:
        form = OrderForm()
    return render(request, 'core/create_order.html', {'form': form})


class OrderCreateView(CreateView):
    """Классовое представление для создания заявки"""
    model = Order
    form_class = OrderForm
    template_name = 'core/create_order.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        messages.success(self.request, 'Ваша запись успешно принята!')
        return super().form_valid(form)

def get_trainer_services(request, trainer_id):
    try:
        trainer = Trainer.objects.get(id=trainer_id)
        services = list(trainer.services.values('id', 'name'))
        return JsonResponse({'services': services})
    except Trainer.DoesNotExist:
        return JsonResponse({'error': 'Trainer not found'}, status=404)
