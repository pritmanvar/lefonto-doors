import django
from utils.utils import CommonResponse

from catalog.models import Catalog
from product.models import Product
from fastapi import status

import os

# ****************************************************** Get Catalog Details ******************************************************


def get_catalog_details(response):
    try:
        catalog = Catalog.objects.latest("id")

        # if isinstance(catalog.catalog_details, list):
        #     catalog.catalog_details.sort(key=lambda x: int(x.get("order", 0)))

        if catalog.catalog_details is None:
            catalog.catalog_details = []
        
        response_obj = []
        
        for obj in catalog.catalog_details:
            if "banner_image" in obj:
                response_obj.append({"banner_image": f"{os.getenv('BASE_URL')}{obj["banner_image"]}"})
            elif "why_us" in obj:
                # response_obj.append({"why_us": [{**why, "icon": f"{os.getenv('BASE_URL')}{why["icon"]}"} for why in obj["why_us"]]})
                response_obj.append({
                    "why_us": [
                        {
                            **why,
                            "icon": f"{os.getenv('BASE_URL')}{why.get('icon', '')}" #.get for why object will not return an error if icon is not present
                        }
                        for why in obj["why_us"]
                    ]
                })
            elif "moto" in obj:
                response_obj.append({"moto": {**obj["moto"], "logo": f"{os.getenv('BASE_URL')}/uploads/{obj["moto"]["logo"] if "logo" in obj["moto"] else ""}"}})
            elif "products_list" in obj:
                product_ids = [int(prod.split(" - ")[1]) for prod in obj["products_list"]]
                products = Product.objects.filter(id__in=product_ids)
                response_obj.append({"products_list": [{"id": prod.id, "name": prod.product_name, "image": prod.get_image_url()} for prod in products]})
            elif "feature_image" in obj:
                response_obj.append({"feature_image": f"{os.getenv('BASE_URL')}{obj["feature_image"]}"})
            else:
                response_obj.append(obj)

        return CommonResponse(
            200,
            "True",
            200,
            "Catalog fetched successfully.",
            "success",
            Value=response_obj,
        )
    except Catalog.DoesNotExist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return CommonResponse(
            404, "False", 404, "No catalog found.", "error", Value=None
        )
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return CommonResponse(500, "False", 500, str(e), "error", Value=None)
