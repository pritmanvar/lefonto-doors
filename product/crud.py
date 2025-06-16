import django
from django.db.models import Q
from django.db import InterfaceError, Error, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError
from fastapi import status

from utils.utils import CommonResponse
from product.models import DoorCategory, DoorStyle, DoorMaterial, DoorColor, DoorDimension, Product, GallarySupporting
from reviews.models import CustomerReview
from authentication.models import Location

import os

def get_filtered_products_details(response, filters):
    # try:
        filters_data = Q()
        materials_list = list(DoorMaterial.objects.filter(id__in=filters.material).values('id', 'name'))
        colors_list = list(DoorColor.objects.filter(id__in=filters.color).values('id', 'name'))
        dimentions_list = list(DoorDimension.objects.filter(id__in=filters.dimentions).values('id', 'thickness', 'height', 'width', 'thickness_measure', 'height_measure', 'width_measure'))
        print(dimentions_list)
        print(materials_list)
        print(colors_list)
        if filters.category:
            filters_data &= Q(category__in=filters.category)
        if filters.style:
            filters_data &= Q(style__in=filters.style)
        if filters.material:
            for mat in materials_list:
                filters_data |= Q(variants__contains=[{"material": f"{mat['name']} - {mat['id']}"}])
        if filters.color:
            for color in colors_list:
                filters_data |= Q(colors__contains=[{"color": f"{color['name']} - {color['id']}"}])
        if filters.dimentions:
            for dim in dimentions_list:
                filters_data |= Q(variants__contains=[{"dimensions": f"{dim['height']}{dim['height_measure']}x{dim['width']}{dim['width_measure']}x{dim['thickness']}{dim['thickness_measure']} - {dim['id']}"}])
        if filters.location:
            filters_data &= Q(location__id=filters.location)

        if filters.short_based_on_ratings:
            products = Product.objects.filter(filters_data).order_by('-ratings')
        else:
            products = Product.objects.filter(filters_data)
        if filters.number_of_products_to_fetch:
            products = products[:filters.number_of_products_to_fetch]
        
        print(filters_data)
        products_obj = []
        for product in products:
            products_obj.append({
                'id': product.id,
                'product_name': product.product_name,
                'category': product.category.title,
                'style': product.style.name,
                'weight': product.weight,
                'ratings': product.ratings,
                'variants': product.get_product_varients(),
                'colors': [{'color_id': color['color'][1], 'color_code': color['color'].split(' -- ')[2], 'color_name': color['color'].split(' -- ')[0], 'images': [f"{os.getenv('BASE_URL')}{img}" for img in color.get('images', [])]} for color in product.colors if (color and len(color['color'].split(' -- ')) == 3)],
                'image': f"{os.getenv('BASE_URL')}{product.main_image.url}" if product.main_image else None,
                'location': [{
                    'id': loc.id,
                    'country': loc.country,
                    'state': loc.state,
                    'city': loc.city,
                    'pincode': loc.pincode,
                    'landmark': loc.landmark
                } for loc in product.location.all()]
            })

        return CommonResponse(200, "True", 200, "Filters details fetched successfully.", 'success', Value=products_obj)
    
    # except (InterfaceError, Error, Exception, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
    #     print(error)
    #     response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    #     return CommonResponse(500, "True", 0, "Something went wrong, Please try again.", Message=("{}").format(error))

def get_product_details(response, product_id: int):
    try:
        try:
            product = Product.objects.get(id=product_id)
            
            if product.colors is None:
                product.colors = []
            
        except Product.DoesNotExist:
            response.status_code = status.HTTP_404_NOT_FOUND
            return CommonResponse(404, "True", 0, "Product not found.", 'error')

        # Prepare features list
        features = list(product.features.values('id', 'feature_name', 'image'))
        features_data = []
        for feature in features:
            features_data.append({
                'id': feature['id'],
                'name': feature['feature_name'],
                'image': f"{os.getenv('BASE_URL')}/uploads/{feature['image']}" if feature['image'] else None
            })

        # Prepare recommended products
        recommended = list(product.recommanded_products.values('id', 'product_name', 'main_image', 'category', 'style', 'ratings', 'variants'))
        recommended_data = []
        for rec in recommended:
            recommended_data.append({
                'id': rec['id'],
                'product_name': rec['product_name'],
                'category': rec['category'],
                'style': rec['style'],
                'ratings': rec['ratings'],
                'variants': rec['variants'],
                'image': f"{os.getenv('BASE_URL')}/uploads/{rec['main_image']}" if rec['main_image'] else None,
            })

        # Prepare gallery images
        gallery = list(GallarySupporting.objects.filter(product=product).values('id', 'image'))
        gallery_data = []
        for img in gallery:
            if img['image']:
                gallery_data.append({
                    'id': img['id'],
                    'image': f"{os.getenv('BASE_URL')}/uploads/{img['image']}" if img['image'] else None
                })

        # Construct the complete product details
        customer_reviews = CustomerReview.objects.filter(product=product)
        product_details = {
            'id': product.id,
            'product_name': product.product_name,
            'details': product.details,
            'weight': product.weight,
            'short_description': product.short_description,
            'main_image': f"{os.getenv('BASE_URL')}{product.main_image.url}" if product.main_image else None,
            'ratings': product.ratings,
            'category': {
                'id': product.category.id,
                'title': product.category.title,
                'image': f"{os.getenv('BASE_URL')}{product.category.category_image.url}" if product.category.category_image else None
            } if product.category else None,
            'style': {
                'id': product.style.id,
                'name': product.style.name,
                'description': product.style.description
            } if product.style else None,
            'variants': product.get_product_varients(),
            'colors': [{'color_id': color['color'][1], 'color_code': color['color'].split(' -- ')[2], 'color_name': color['color'].split(' -- ')[0], 'images': [f"{os.getenv('BASE_URL')}{img}" for img in color['images']]} for color in product.colors if (color and len(color['color'].split(' -- ')) == 3)],
            'features': features_data,
            'warranty_details': product.warranty_details,
            'return_policy': product.return_policy,
            'location': [{
                'id': loc.id,
                'country': loc.country,
                'state': loc.state,
                'city': loc.city,
                'pincode': loc.pincode,
                'landmark': loc.landmark,
            } for loc in product.location.all()],
            'recommended_products': recommended_data,
            'gallery_images': gallery_data,
            'reviews': [
                {
                    'id': review.id,
                    'user': {
                        'username': review.user.username,
                        'profile_image': f"{os.getenv('BASE_URL')}{review.user.profile_image.url}" if review.user.profile_image else None,
                        'mobile': review.user.mobile,
                        'email': review.user.email
                    },
                    'rating': review.rating,
                    'review_text': review.review_text,
                } for review in customer_reviews
            ],
            'created_at': product.created_at,
            'updated_at': product.updated_at,
        }

        return CommonResponse(200, "True", 200, "Product details fetched successfully.", 'success', Value=product_details)

    except (InterfaceError, Error, Exception, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return CommonResponse(500, "True", 0, "Something went wrong, Please try again.", Message=("{}").format(error))

def get_filters_details(response):
    try:
        categories = list(DoorCategory.objects.all().values('id', 'title', 'category_image'))
        styles = list(DoorStyle.objects.all().values('id', 'name', 'description'))
        materials = list(DoorMaterial.objects.all().values('id', 'name'))
        colors = list(DoorColor.objects.all().values('id', 'name', 'color_code'))
        dimensions = list(DoorDimension.objects.all().values('id', 'height', 'width', 'thickness', 'height_measure', 'width_measure', 'thickness_measure'))
        locations = list(Location.objects.all().values('id', 'country', 'state', 'city', 'pincode', 'landmark'))
        return CommonResponse(200, "True", 200, "Filters Fetched Successfully.", 'success', Value={'categories': categories, 'styles': styles, 'materials': materials, 'colors': colors, 'dimensions': dimensions, 'locations': locations})

    except (InterfaceError, Error, Exception, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return CommonResponse(500, "True", 0, "Something went wrong, Please try again.", Message=("{}").format(error))