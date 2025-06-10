import django
from utils.utils import CommonResponse

from catalog.models import Catalog
from fastapi import status

import os

# ****************************************************** Get Catalog Details ******************************************************


def get_catalog_details(response):
    try:
        catalog = Catalog.objects.latest("id")

        if isinstance(catalog.catalog_details, list):
            catalog.catalog_details.sort(key=lambda x: int(x.get("order", 0)))

        response_obj = [
            {
                **cat,
                "why_us": [
                    {
                        **why,
                        "image": (
                            f"{os.getenv('BASE_URL')}{why['image']}"
                            if why["image"]
                            else None
                        ),
                    }
                    for why in cat.get("why_us", [])
                ],
                "image": (
                    f"{os.getenv('BASE_URL')}{cat['image']}" if cat["image"] else None
                ),
            }
            for cat in catalog.catalog_details
        ]
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
