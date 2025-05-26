from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random
from datetime import datetime, timedelta

from product.models import (
    Category, ProductMaterial, Style, Color, Size, Feature,
    Product, ProductSizePrice, ProductImage
)
from about.models import WhyUsAbout, Expertise, About
from catalog.models import WhyUsCatalog, Catalog
from contactus.models import ContactQueries
from reviews.models import CustomerReview
from home.models import Banner, Home

fake = Faker()

class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Create superuser
        User = get_user_model()
        if not User.objects.filter(email='admin@gmail.com').exists():
            User.objects.create_superuser('admin@gmail.com', 'admin@123')
            self.stdout.write('Superuser created.')

        # Seed Categories
        categories = []
        category_names = ['Interior Doors', 'Exterior Doors', 'Sliding Doors', 'French Doors', 'Security Doors']
        for name in category_names:
            category, created = Category.objects.get_or_create(name=name)
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {name}')

        # Seed Materials
        materials = []
        material_names = ['Wood', 'Metal', 'Glass', 'Fiberglass', 'PVC']
        for name in material_names:
            material, created = ProductMaterial.objects.get_or_create(material_name=name)
            materials.append(material)
            if created:
                self.stdout.write(f'Created material: {name}')

        # Seed Styles
        styles = []
        style_names = ['Modern', 'Traditional', 'Contemporary', 'Rustic', 'Industrial']
        for name in style_names:
            style, created = Style.objects.get_or_create(style_name=name)
            styles.append(style)
            if created:
                self.stdout.write(f'Created style: {name}')

        # Seed Colors
        colors = []
        color_data = [
            ('White', '#FFFFFF'),
            ('Brown', '#8B4513'),
            ('Black', '#000000'),
            ('Gray', '#808080'),
            ('Natural Wood', '#DEB887')
        ]
        for name, code in color_data:
            color, created = Color.objects.get_or_create(color_name=name, color_code=code)
            colors.append(color)
            if created:
                self.stdout.write(f'Created color: {name}')

        # Seed Sizes
        sizes = []
        size_combinations = [
            (80, 32), (80, 36), (96, 36),
            (72, 32), (72, 36), (84, 36)
        ]
        for height, width in size_combinations:
            size, created = Size.objects.get_or_create(height=height, width=width)
            sizes.append(size)
            if created:
                self.stdout.write(f'Created size: {height}x{width}')

        # Seed Features
        features = []
        feature_names = [
            'Termite Proof', 'Premium Finish', 'Fire Retardant', 'Zero Shrinkage',
            '100% Waterproof', 'Maintenance Free' ,'Long Life Durability', 'Scratch & Stain Resistant'
        ]
        for name in feature_names:
            feature, created = Feature.objects.get_or_create(feature_name=name)
            features.append(feature)
            if created:
                self.stdout.write(f'Created feature: {name}')

        # Seed Products
        for i in range(20):
            product = Product.objects.create(
                product_name=f"{fake.word().title()} Door {i+1}",
                details=fake.paragraph(nb_sentences=5),
                short_description=fake.paragraph(nb_sentences=2),
                category=random.choice(categories),
                material=random.choice(materials),
                style=random.choice(styles),
                thickness=random.uniform(1.5, 3.0),
                weight=random.uniform(20, 50),
                warranty_details=fake.paragraph(nb_sentences=3),
                return_policy=fake.paragraph(nb_sentences=2),
                ratings=random.uniform(3.5, 5.0)
            )
            # Add random colors and features
            product.color.set(random.sample(colors, random.randint(1, 3)))
            product.features.set(random.sample(features, random.randint(2, 4)))
            
            # Add product sizes with prices
            for size in random.sample(sizes, random.randint(2, 4)):
                ProductSizePrice.objects.create(
                    product=product,
                    size=size,
                    price=random.uniform(200, 1000),
                    discount=random.uniform(0, 15)
                )
            
            # Add product images
            ProductImage.objects.create(
                product=product,
                image='dummy/product.jpg'  # You'll need to handle actual images
            )
            
            self.stdout.write(f'Created product: {product.product_name}')

        # Seed About Section
        why_us_items = []
        for i in range(4):
            why_us = WhyUsAbout.objects.create(
                title=f"Why Choose Us {i+1}",
                description=fake.paragraph()
            )
            why_us_items.append(why_us)

        expertise_items = []
        for i in range(4):
            expertise = Expertise.objects.create(
                title=f"Expertise {i+1}"
            )
            expertise_items.append(expertise)

        about = About.objects.create(
            title="About Our Door Company",
            title_description=fake.paragraph(),
            why_us_description=fake.paragraph(),
            description=fake.paragraph(),
            question="Why choose our doors?",
            answer=fake.paragraph(),
            contact_number=fake.phone_number(),
            email=fake.email(),
            address=fake.address(),
            website="www.example.com"
        )
        about.why_us.set(why_us_items)
        about.expertise.set(expertise_items)

        # Seed Catalog Section
        why_us_catalog_items = []
        for i in range(4):
            why_us = WhyUsCatalog.objects.create(
                title=f"Catalog Feature {i+1}",
                description=fake.paragraph()
            )
            why_us_catalog_items.append(why_us)

        catalog = Catalog.objects.create(
            about=fake.paragraph(),
            description=fake.paragraph()
        )
        catalog.why_us.set(why_us_catalog_items)

        # Seed Contact Queries
        for _ in range(10):
            ContactQueries.objects.create(
                name=fake.name(),
                email=fake.email(),
                message=fake.paragraph()
            )

        # Seed Home Page
        banner = Banner.objects.create(
            description="Welcome to our Door Store",
            product_material=random.choice(materials),
            is_active=True
        )

        home = Home.objects.create(
            title="Welcome to Our Door Store",
            description=fake.paragraph(),
            question="Looking for quality doors?",
            answer=fake.paragraph()
        )
        home.categories.set(random.sample(list(categories), 3))
        home.features.set(random.sample(list(features), 3))

        # Create some regular users
        users = []
        for i in range(5):
            user = User.objects.create_user(
                email=f"user{i+1}@example.com",
                password="user123",
                name=fake.name(),
                country=fake.country(),
                city=fake.city()
            )
            users.append(user)

        # Seed Reviews
        for product in Product.objects.all():
            for _ in range(random.randint(1, 3)):
                CustomerReview.objects.create(
                    user=random.choice(users),
                    product=product,
                    rating=random.uniform(3.5, 5.0),
                    review_text=fake.paragraph()
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database')) 