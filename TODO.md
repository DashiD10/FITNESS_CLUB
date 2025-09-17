# TODO for Customizing Admin Models

- [x] Update core/admin.py with necessary imports (admin, models, filters)
- [x] Define custom DateRangeFilter for Order appointment_date
- [x] Define OrderServiceInline for Order admin
- [x] Define ReviewInline for Trainer admin
- [x] Define OrderAdmin with list_display, list_filter, search_fields, list_editable, actions, inlines
- [x] Update TrainerAdmin with list_display, list_filter, search_fields, inlines
- [x] Define ServiceAdmin with list_display, list_filter, search_fields
- [x] Register all models with their admins
- [x] Run makemigrations and migrate for model changes
- [x] Test the admin panel (server running, superuser exists)
