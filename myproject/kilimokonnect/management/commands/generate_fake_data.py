# kilimokonnect/management/commands/generate_fake_data.py
from django.core.management.base import BaseCommand # type: ignore
from faker import Faker # type: ignore
import random
from django.utils import timezone # type: ignore
from kilimokonnect.models import (
    CustomUser, 
    FreshProduceRetailer, 
    ProduceCategory, 
    FreshProduce, 
    Order, 
    OrderItem,
    StorageOwner, 
    StorageFacility, 
    Product, 
    StorageBooking, 
    Payment, 
    Review
)

#User = get_user_model()

class Command(BaseCommand):
    help = 'Generate fake data for the database'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Clear existing data (optional)
        models_to_clear = [
            CustomUser, 
            FreshProduceRetailer, 
            ProduceCategory, 
            FreshProduce, 
            Order, 
            StorageOwner, 
            StorageFacility, 
            Product, 
            StorageBooking, 
            Payment, 
            Review
        ]
        for model in models_to_clear:
            model.objects.all().delete()

        # Create 20 CustomUser entries
        users = []
        for _ in range(20):
            user = CustomUser.objects.create_user(
                email=fake.unique.email(),
                password='testpassword123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                user_type=random.choice(['owner', 'retailer']),
                location=fake.city()
            )
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.email}'))

        # Create ProduceCategories
        categories = []
        for _ in range(5):
            category = ProduceCategory.objects.create(
                name=fake.unique.word(),
                description=fake.text(),
                storage_requirements=fake.text(),
                shelf_life=random.randint(1, 30)
            )
            categories.append(category)
            self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Create FreshProduce
        produces = []
        for _ in range(20):
            produce = FreshProduce.objects.create(
                name=fake.unique.word(),
                category=random.choice(categories),
                quality_grade=random.choice(['A', 'B', 'C']),
                unit_price=round(random.uniform(10, 1000), 2),
                available_quantity=round(random.uniform(10, 1000), 2),
                minimum_order_quantity=round(random.uniform(1, 10), 2),
                harvest_date=fake.date_this_year(),
                expiry_date=fake.date_between(start_date='+1d', end_date='+30d'),
                is_organic=random.choice([True, False])
            )
            produces.append(produce)
            self.stdout.write(self.style.SUCCESS(f'Created produce: {produce.name}'))

        # Create FreshProduceRetailers
        retailers = []
        for user in users:
            if user.user_type == 'retailer':
                retailer = FreshProduceRetailer.objects.create(
                    user=user,
                    business_name=fake.company(),
                    contact_person=fake.name(),
                    phone_number=fake.phone_number(),
                    email=user.email,
                    business_address=fake.address(),
                    business_registration=fake.bothify(text='BR-######'),
                    tax_number=fake.bothify(text='TN-######'),
                    is_verified=random.choice([True, False])
                )
                retailers.append(retailer)
                self.stdout.write(self.style.SUCCESS(f'Created retailer: {retailer.business_name}'))

        # Create Orders
        orders = []
        for retailer in retailers:
            order = Order.objects.create(
                retailer=retailer,
                delivery_date=fake.date_between(start_date='+1d', end_date='+30d'),
                status=random.choice([status[0] for status in Order.ORDER_STATUS]),
                total_amount=round(random.uniform(100, 10000), 2),
                shipping_address=fake.address(),
            )
            orders.append(order)
            self.stdout.write(self.style.SUCCESS(f'Created order: {order.order_reference}'))

            # Create OrderItems
            for _ in range(random.randint(1, 3)):
                produce = random.choice(produces)
                OrderItem.objects.create(
                    order=order,
                    produce=produce,
                    quantity=round(random.uniform(1, 50), 2),
                    unit_price=produce.unit_price,
                    subtotal=round(random.uniform(50, 500), 2)
                )

        # Create StorageOwners
        storage_owners = []
        for user in users:
            if user.user_type == 'owner':
                storage_owner = StorageOwner.objects.create(
                    user=user,
                    business_name=fake.company(),
                    phone_number=fake.phone_number(),
                    email=user.email,
                    address=fake.address(),
                    registration_number=fake.bothify(text='SO-######'),
                    is_verified=random.choice([True, False])
                )
                storage_owners.append(storage_owner)
                self.stdout.write(self.style.SUCCESS(f'Created storage owner: {storage_owner.business_name}'))

        # Create StorageFacilities
        facilities = []
        for owner in storage_owners:
            facility = StorageFacility.objects.create(
                owner=owner,
                name=fake.company(),
                facility_type=random.choice([ft[0] for ft in StorageFacility.FACILITY_TYPES]),
                capacity=round(random.uniform(10, 1000), 2),
                available_space=round(random.uniform(5, 500), 2),
                location=fake.city(),
                gps_coordinates=f"{fake.latitude()}, {fake.longitude()}",
                price_per_unit=round(random.uniform(10, 100), 2),
                is_active=random.choice([True, False])
            )
            facilities.append(facility)
            self.stdout.write(self.style.SUCCESS(f'Created storage facility: {facility.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data'))