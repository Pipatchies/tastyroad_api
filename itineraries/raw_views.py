from django.db import connection
from django.http import JsonResponse


class ItineraryDTO:
    def __init__(
        self,
        itinerary_id,
        title,
        zone,
        distance,
        author_username,
        average_rating,
        steps_count,
    ):
        self.id = itinerary_id
        self.title = title
        self.zone = zone
        self.distance = distance
        self.author = author_username
        self.average_rating = round(float(average_rating), 1)
        self.steps_count = int(steps_count)

    def to_dict(self):
        """Méthode de sérialisation manuelle pour préparer le passage en JSON"""
        return {
            "id": self.id,
            "title": self.title,
            "zone": self.zone,
            "distance": self.distance,
            "author": self.author,
            "average_rating": self.average_rating,
            "steps_count": self.steps_count,
        }


def raw_sql_itineraries_view(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed. Use GET."}, status=405)

    limit = request.GET.get("limit", 5)
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
            SELECT
                i.id,
                i.title,
                i.zone,
                i.distance,
                u.username,
                COALESCE(AVG(c.review), 0) AS average_rating,
                COUNT(DISTINCT s.id) AS steps_count
            FROM itineraries_itinerary i
            INNER JOIN users_user u ON i.author_id = u.id
            LEFT JOIN itineraries_comment c ON c.itinerary_id = i.id
            LEFT JOIN itineraries_step s ON s.itinerary_id = i.id
            GROUP BY i.id, u.username
            ORDER BY average_rating DESC, i.id ASC
            LIMIT %s;
        """
        cursor.execute(query, [limit])

        for row in cursor.fetchall():
            itinerary_obj = ItineraryDTO(
                itinerary_id=row[0],
                title=row[1],
                zone=row[2],
                distance=row[3],
                author_username=row[4],
                average_rating=row[5],
                steps_count=row[6],
            )
            itineraries_data.append(itinerary_obj.to_dict())

    return JsonResponse({"status": "success", "data": itineraries_data}, status=200)
