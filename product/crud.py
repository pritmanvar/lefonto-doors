import django
from django.db.models import Q
from django.db import InterfaceError, Error, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError
from fastapi import status

from utils.utils import CommonResponse
from product.models import DoorCategory, DoorStyle, DoorMaterial, DoorColor, DoorDimension, Product, GallarySupporting

def get_filters_details(response, filters):
    try:
        filters_data = Q()
        materials_list = list(DoorMaterial.objects.filter(id__in=filters.material).values('id', 'name'))
        colors_list = list(DoorColor.objects.filter(id__in=filters.color).values('id', 'name'))
        
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
        
        products = Product.objects.filter(filters_data)
        products_obj = []
        for product in products:
            products_obj.append({
                'id': product.id,
                'product_name': product.product_name,
                'category': product.category.title,
                'style': product.style.name,
                'ratings': product.ratings,
                'variants': product.variants,
                'image': product.main_image.url if product.main_image else None,
            })

        return CommonResponse(200, "True", 200, "Filters details fetched successfully.", 'success', Value=products_obj)
    
    except (InterfaceError, Error, Exception, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return CommonResponse(500, "True", 0, "Something went wrong, Please try again.", Message=("{}").format(error))

def get_product_details(response, product_id: int):
    try:
        try:
            product = Product.objects.get(id=product_id)
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
                'image': feature['image'] if feature['image'] else None
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
                'image': rec['main_image'],
            })

        # Prepare gallery images
        gallery = list(GallarySupporting.objects.filter(product=product).values('id', 'image'))
        gallery_data = []
        for img in gallery:
            if img['image']:
                gallery_data.append({
                    'id': img['id'],
                    'image': img['image']
                })

        # Construct the complete product details
        product_details = {
            'id': product.id,
            'product_name': product.product_name,
            'details': product.details,
            'short_description': product.short_description,
            'main_image': product.main_image.url if product.main_image else None,
            'ratings': product.ratings,
            'category': {
                'id': product.category.id,
                'title': product.category.title,
                'image': product.category.category_image.url if product.category.category_image else None
            } if product.category else None,
            'style': {
                'id': product.style.id,
                'name': product.style.name,
                'description': product.style.description
            } if product.style else None,
            'variants': product.variants,
            'colors': product.colors,
            'features': features_data,
            'warranty_details': product.warranty_details,
            'return_policy': product.return_policy,
            'recommended_products': recommended_data,
            'gallery_images': gallery_data,
            'created_at': product.created_at,
            'updated_at': product.updated_at
        }

        return CommonResponse(200, "True", 200, "Product details fetched successfully.", 'success', Value=product_details)

    except (InterfaceError, Error, Exception, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, ProgrammingError, NotSupportedError) as error:
        print(error)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return CommonResponse(500, "True", 0, "Something went wrong, Please try again.", Message=("{}").format(error))

