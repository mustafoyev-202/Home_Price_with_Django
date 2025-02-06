from django.http import JsonResponse
from django.shortcuts import render
from . import utils
import json


def home(request):
    # Load locations when rendering the home page
    locations = utils.get_location_names()
    return render(request, "home.html", {"locations": locations})


def predict_home_price(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            total_sqft = float(data.get("total_sqft"))
            location = data.get("location")
            bhk = int(data.get("bhk"))
            bath = int(data.get("bath"))

            estimated_price = utils.get_estimated_price(location, total_sqft, bhk, bath)

            return JsonResponse(
                {"estimated_price": estimated_price, "status": "success"}
            )
        except Exception as e:
            return JsonResponse({"error": str(e), "status": "error"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_location_names(request):
    try:
        locations = utils.get_location_names()
        print("Locations loaded:", locations)  # Debug print
        return JsonResponse({"locations": locations})
    except Exception as e:
        print("Error loading locations:", str(e))  # Debug print
        return JsonResponse({"error": str(e)}, status=500)
