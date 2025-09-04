# TODO List for Completing Django Routes and Views

- [x] Update fitness_club/settings.py to add TEMPLATES DIRS for core/templates
- [x] Update fitness_club/urls.py to add orders_list and order_detail routes
- [x] Update core/views.py to render templates for landing and order_detail, add orders_list view with mock data

# TODO List for Connecting Static Files

- [x] Create static directory and main.css, main.js files
- [x] Update fitness_club/settings.py to add STATICFILES_DIRS
- [x] Update all templates to include static links for main.css and main.js

# TODO List for Includes and Templates

- [x] Create core/templates/core/includes/menu.html with navigation menu, anchors, mobile hamburger, is_staff logic
- [x] Update core/templates/core/base.html to include menu.html
- [x] Create core/templates/core/includes/order_card.html with order fields, status colors, detail button
- [x] Update core/templates/core/orders_list.html to use cards with include order_card.html
- [x] Update core/views.py mock data to include date, services, trainer_name
- [x] Update core/templates/core/order_detail.html to display new fields with status colors
- [x] Create core/context_processors.py for menu data
- [x] Update fitness_club/settings.py to add context processor
- [x] Update includes/menu.html to use context processor menu_links
