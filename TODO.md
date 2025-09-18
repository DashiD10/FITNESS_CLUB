# TODO: Telegram Notifications for New Orders

## Completed Tasks
- [x] Analyze project structure and models
- [x] Understand Order model (name, phone, trainer, services M2M, appointment_date)
- [x] Create core/telegram.py with send_telegram_message function
- [x] Create core/signals.py with m2m_changed handler for Order.services
- [x] Update fitness_club/settings.py to add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
- [x] Update core/apps.py to import signals in ready()
- [x] Update .env.example to include TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID (assumed done by user)

## Pending Tasks
- [x] Test the notification by creating a new order (confirmed working by user)
