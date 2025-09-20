# Рефакторинг представлений Django: FBV → CBV

## План выполнения

### Часть 1: Простые представления (TemplateView)
- [ ] Создать `LandingView` (TemplateView) с передачей тренеров и отзывов в контекст
- [ ] Создать `ThanksView` (TemplateView)

### Часть 2: ListView и DetailView
- [ ] Создать `OrdersListView` (ListView) с логикой поиска в `get_queryset`
- [ ] Создать `OrderDetailView` (DetailView)

### Часть 3: CreateView
- [ ] Создать `ReviewCreateView` (CreateView) с flash-сообщением в `form_valid`
- [ ] Создать `OrderCreateView` (CreateView) с flash-сообщением в `form_valid`

### Часть 4: Обновление URLs
- [ ] Обновить `fitness_club/urls.py` для использования `.as_view()`

### Часть 5: Тестирование
- [ ] Проверить запуск проекта
- [ ] Проверить работу всех маршрутов
