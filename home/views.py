from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FoodTruck
from .serializers import FoodTruckSerializer
from math import radians, cos, sin, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def get_distance(truck_with_distance):
    return truck_with_distance[1]

@api_view(['GET'])
def nearby_food_trucks(request):
    lat = request.query_params.get('lat')
    lng = request.query_params.get('lng')


    try:
        latitude = float(lat)
        longitude = float(lng)
    except ValueError:
        return Response({"error": "Invalid latitude or longitude."}, status=400)


    all_trucks = FoodTruck.objects.all()

    trucks_with_distance = []
    for truck in all_trucks:        
        distance = calculate_distance(latitude, longitude, truck.latitude, truck.longitude)
        print("distance", distance)
        trucks_with_distance.append((truck, distance))

    trucks_with_distance.sort(key=get_distance)
    
    closest_trucks = []
    for truck_with_distance in trucks_with_distance[:5]:
        truck = truck_with_distance[0]
        closest_trucks.append(truck)
    
    serializer = FoodTruckSerializer(closest_trucks, many=True)
    return Response(serializer.data)