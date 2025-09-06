from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import datetime, timedelta
from decimal import Decimal
from core.models import Service, Trainer, Order, Review, STATUS_CHOICES, RATING_CHOICES


class ServiceModelTest(TestCase):
    def setUp(self):
        self.service_data = {
            'name': 'Тренировка по боксу',
            'description': 'Интенсивная тренировка',
            'price': Decimal('1500.00'),
            'duration': 60,
            'is_popular': True,
        }

    def test_service_creation(self):
        service = Service.objects.create(**self.service_data)
        self.assertEqual(service.name, 'Тренировка по боксу')
        self.assertEqual(service.price, Decimal('1500.00'))
        self.assertEqual(service.duration, 60)
        self.assertTrue(service.is_popular)
        self.assertEqual(str(service), 'Тренировка по боксу')

    def test_service_str_method(self):
        service = Service.objects.create(**self.service_data)
        self.assertEqual(str(service), service.name)

    def test_service_blank_description(self):
        self.service_data['description'] = ''
        service = Service.objects.create(**self.service_data)
        self.assertEqual(service.description, '')

    def test_service_blank_image(self):
        service = Service.objects.create(**self.service_data)
        self.assertEqual(service.image.name, '')


class TrainerModelTest(TestCase):
    def setUp(self):
        self.trainer_data = {
            'name': 'Иван Иванов',
            'phone': '+7(999)123-45-67',
            'address': 'ул. Ленина, 10',
            'experience': 5,
            'is_active': True,
        }

    def test_trainer_creation(self):
        trainer = Trainer.objects.create(**self.trainer_data)
        self.assertEqual(trainer.name, 'Иван Иванов')
        self.assertEqual(trainer.experience, 5)
        self.assertTrue(trainer.is_active)
        self.assertEqual(str(trainer), 'Иван Иванов')

    def test_trainer_str_method(self):
        trainer = Trainer.objects.create(**self.trainer_data)
        self.assertEqual(str(trainer), trainer.name)

    def test_trainer_services_relationship(self):
        trainer = Trainer.objects.create(**self.trainer_data)
        service1 = Service.objects.create(
            name='Бокс', price=Decimal('1000.00'), duration=45
        )
        service2 = Service.objects.create(
            name='Кроссфит', price=Decimal('1200.00'), duration=60
        )
        trainer.services.add(service1, service2)
        self.assertEqual(trainer.services.count(), 2)
        self.assertIn(service1, trainer.services.all())
        self.assertIn(service2, trainer.services.all())


class OrderModelTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Персональная тренировка',
            price=Decimal('2000.00'),
            duration=60
        )
        self.trainer = Trainer.objects.create(
            name='Петр Петров',
            phone='+7(999)987-65-43',
            address='ул. Пушкина, 5',
            experience=3
        )
        self.order_data = {
            'name': 'Алексей Смирнов',
            'phone': '+7(999)111-22-33',
            'comment': 'Хочу похудеть',
            'appointment_date': datetime.now() + timedelta(days=1),
        }

    def test_order_creation(self):
        order = Order.objects.create(**self.order_data)
        self.assertEqual(order.name, 'Алексей Смирнов')
        self.assertEqual(order.status, 'not_approved')
        self.assertIsNotNone(order.date_created)
        self.assertIsNotNone(order.date_updated)
        self.assertEqual(str(order), 'Заказ от Алексей Смирнов')

    def test_order_status_choices(self):
        order = Order.objects.create(**self.order_data)
        self.assertIn(order.status, [choice[0] for choice in STATUS_CHOICES])

    def test_order_trainer_relationship(self):
        self.order_data['trainer'] = self.trainer
        order = Order.objects.create(**self.order_data)
        self.assertEqual(order.trainer, self.trainer)

    def test_order_services_relationship(self):
        order = Order.objects.create(**self.order_data)
        order.services.add(self.service)
        self.assertEqual(order.services.count(), 1)
        self.assertIn(self.service, order.services.all())

    def test_order_blank_comment(self):
        self.order_data['comment'] = ''
        order = Order.objects.create(**self.order_data)
        self.assertEqual(order.comment, '')


class ReviewModelTest(TestCase):
    def setUp(self):
        self.trainer = Trainer.objects.create(
            name='Сергей Сергеев',
            phone='+7(999)555-66-77',
            address='ул. Гагарина, 15',
            experience=7
        )
        self.review_data = {
            'text': 'Отличный тренер! Очень помог с тренировками.',
            'client_name': 'Мария Иванова',
            'trainer': self.trainer,
            'rating': 5,
            'is_published': True,
        }

    def test_review_creation(self):
        review = Review.objects.create(**self.review_data)
        self.assertEqual(review.text, 'Отличный тренер! Очень помог с тренировками.')
        self.assertEqual(review.rating, 5)
        self.assertTrue(review.is_published)
        self.assertIsNotNone(review.created_at)
        self.assertEqual(str(review), 'Отзыв от Мария Иванова')

    def test_review_rating_choices(self):
        review = Review.objects.create(**self.review_data)
        self.assertIn(review.rating, [choice[0] for choice in RATING_CHOICES])

    def test_review_blank_client_name(self):
        self.review_data['client_name'] = ''
        review = Review.objects.create(**self.review_data)
        self.assertEqual(review.client_name, '')
        self.assertEqual(str(review), 'Отзыв от Аноним')

    def test_review_trainer_relationship(self):
        review = Review.objects.create(**self.review_data)
        self.assertEqual(review.trainer, self.trainer)

    def test_review_blank_photo(self):
        review = Review.objects.create(**self.review_data)
        self.assertIsNone(review.photo.name)


class ModelRelationshipsTest(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='Групповая тренировка',
            price=Decimal('800.00'),
            duration=45
        )
        self.trainer = Trainer.objects.create(
            name='Анна Аннова',
            phone='+7(999)444-55-66',
            address='ул. Советская, 20',
            experience=4
        )
        self.trainer.services.add(self.service)

    def test_trainer_services_reverse_relationship(self):
        self.assertEqual(self.service.trainers.count(), 1)
        self.assertIn(self.trainer, self.service.trainers.all())

    def test_order_services_reverse_relationship(self):
        order = Order.objects.create(
            name='Дмитрий Дмитриев',
            phone='+7(999)777-88-99',
            appointment_date=datetime.now() + timedelta(days=2)
        )
        order.services.add(self.service)
        self.assertEqual(self.service.orders.count(), 1)
        self.assertIn(order, self.service.orders.all())

    def test_review_trainer_cascade_delete(self):
        review = Review.objects.create(
            text='Хороший тренер',
            trainer=self.trainer,
            rating=4
        )
        trainer_id = self.trainer.id
        self.trainer.delete()
        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(id=review.id)

    def test_order_trainer_set_null_on_delete(self):
        order = Order.objects.create(
            name='Елена Еленова',
            phone='+7(999)333-44-55',
            trainer=self.trainer,
            appointment_date=datetime.now() + timedelta(days=3)
        )
        self.trainer.delete()
        order.refresh_from_db()
        self.assertIsNone(order.trainer)
