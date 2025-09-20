def menu_links(request):
    """
    Контекстный процессор для передачи данных навигационного меню во все шаблоны.
    """
    links = [
        {'url_name': 'landing', 'label': 'Главная', 'anchor': '#about'},
        {'url_name': 'landing', 'label': 'Услуги', 'anchor': '#services'},
        {'url_name': 'landing', 'label': 'Тренеры', 'anchor': '#trainers'},
        {'url_name': 'create_order', 'label': 'Запись', 'anchor': ''},
        {'url_name': 'create_review', 'label': 'Отзыв', 'anchor': ''},
    ]

    if request.user.is_staff:
        links.append({'url_name': 'orders_list', 'label': 'Заявки', 'anchor': ''})

    return {'menu_links': links}


def auth_menu(request):
    """
    Контекстный процессор для передачи данных аутентификации в меню.
    """
    if request.user.is_authenticated:
        return {
            'user_menu': [
                {'label': f'Привет, {request.user.username}!', 'url': '#', 'is_username': True},
                {'label': 'Выход', 'url': '#', 'is_logout': True, 'form_id': 'logout-form'},
            ]
        }
    else:
        return {
            'user_menu': [
                {'label': 'Вход', 'url': 'users:login', 'is_login': True},
                {'label': 'Регистрация', 'url': 'users:register', 'is_register': True},
            ]
        }
