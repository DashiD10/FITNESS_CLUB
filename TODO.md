# TODO for Fitness Club Forms

## Completed Tasks
- [x] Created ReviewForm (ModelForm for Review model)
  - Dropdown for trainers (all active trainers)
  - Rating dropdown with descriptive choices (1-5)
  - Client name field
  - Text field for review
- [x] Created OrderForm (ModelForm for Order model)
  - Trainer selection
  - Services selection (filtered by trainer)
  - Name, phone, comment, appointment_date fields
  - Validation in clean() to ensure services belong to selected trainer
- [x] Added create_review and create_order views
- [x] Updated URLs for new routes
- [x] Created templates for create_review and create_order
- [x] Added AJAX endpoint for dynamic service loading
- [x] Added JavaScript for dynamic services loading on trainer change
- [x] Server running successfully
- [x] Added menu links for forms

## Pending Tasks
- [ ] Test forms functionality
- [ ] Test validation
- [ ] Test AJAX dynamic loading

## Notes
- Forms redirect to thanks page on success
- CSRF tokens included
- Bootstrap styling used
- Dynamic loading optional but implemented
