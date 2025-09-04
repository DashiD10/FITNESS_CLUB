def menu_links(request):
    """
    Контекстный процессор для передачи данных навигационного меню во все шаблоны.
    """
    links = [
        {'url_name': 'landing', 'label': 'Главная', 'anchor': '#about'},
        {'url_name': 'landing', 'label': 'Услуги', 'anchor': '#services'},
        {'url_name': 'landing', 'label': 'Тренеры', 'anchor': '#trainers'},
        {'url_name': 'landing', 'label': 'Запись', 'anchor': '#booking'},
    ]
    if request.user.is_staff:
        links.append({'url_name': 'orders_list', 'label': 'Заявки', 'anchor': ''})
    return {'menu_links': links}
