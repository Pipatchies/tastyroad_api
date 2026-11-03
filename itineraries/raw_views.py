from django.db import connection
from django.http import JsonResponse


class ItineraryDTO:
    def __init__(self, itinerary_id, title, distance, author_username):
        self.id = itinerary_id
        self.title = title
        self.distance = distance
        self.author = author_username

    def to_dict(self):
        """Méthode de sérialisation manuelle pour préparer le passage en JSON"""
        return {
            "id": self.id,
            "title": self.title,
            "distance": self.distance,
            "author": self.author,
        }


def raw_sql_itineraries_view(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed. Use GET."}, status=405)

    limit = request.GET.get("limit", 10)
    try:
        limit = int(limit)
        if limit <= 0:
            raise ValueError
    except ValueError:
        return JsonResponse(
            {"error": "Invalid limit parameter. Must be a positive integer."},
            status=400,
        )

    itineraries_data = []

    with connection.cursor() as cursor:
        query = """
            SELECT i.id, i.title, i.distance, u.username
            FROM itineraries_itinerary i
            INNER JOIN users_user u ON i.author_id = u.id
            ORDER BY i.distance DESC
            LIMIT %s;
        """
        cursor.execute(query, [limit])

        for row in cursor.fetchall():
            itinerary_obj = ItineraryDTO(
                itinerary_id=row[0],
                title=row[1],
                distance=row[2],
                author_username=row[3],
            )
            itineraries_data.append(itinerary_obj.to_dict())

    return JsonResponse({"status": "success", "data": itineraries_data}, status=200)
