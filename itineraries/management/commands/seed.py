import random
from datetime import timedelta

from django.contrib.gis.geos import LineString, Point
from django.core.management.base import BaseCommand
from faker import Faker

from itineraries.models import Comment, Favorite, Itinerary, Step
from places.models import FoodPlace
from users.models import User


def random_france_point():
    """Génère un point GPS situé en France métropolitaine."""
    lon = round(random.uniform(-2.0, 6.0), 5)
    lat = round(random.uniform(43.5, 49.0), 5)
    return (lon, lat)


class Command(BaseCommand):
    help = "Génère des données mockées pour tester l'API sur Postman"

    def handle(self, *args, **kwargs):
        fake = Faker("fr_FR")

        self.stdout.write("Suppression des anciennes données...")
        Itinerary.objects.all().delete()
        FoodPlace.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write("Création de 5 utilisateurs...")
        users = []
        for _ in range(5):
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.email(),
                password="mdp_postman_123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                age=random.randint(18, 70),
            )
            users.append(user)

        self.stdout.write("Création de 10 étapes gourmandes...")
        places_templates = [
            (
                "La Ferme du Terroir",
                "Producteur local",
                "Vente directe de produits fermiers bio et dégustation sur place.",
            ),
            (
                "Fromagerie Saint-Antoine",
                "Fromagerie",
                "Affinage traditionnel de fromages au lait cru de la région.",
            ),
            (
                "Le Bistrot des Halles",
                "Restaurant",
                "Cuisine traditionnelle de saison élaborée avec les producteurs locaux.",
            ),
            (
                "Marché Couvert des Producteurs",
                "Marché",
                "Grand marché régional réunissant maraîchers, fromagers et charcutiers.",
            ),
            (
                "Cave des Coteaux",
                "Cave",
                "Découverte des cépages locaux et dégustation commentée par le vigneron.",
            ),
            (
                "Boulangerie du Vieux Moulin",
                "Boulangerie",
                "Pains au levain naturel cuits au feu de bois et viennoiseries maison.",
            ),
            (
                "L'Auberge Gourmande",
                "Restaurant",
                "Spécialités régionales mijotées et terrasse panoramique.",
            ),
            (
                "Les Vergers de la Vallée",
                "Producteur local",
                "Production artisanale de cidre fermier, jus de pomme et miel.",
            ),
            (
                "Maison du Pâtissier",
                "Pâtisserie",
                "Douceurs régionales et biscuits artisanaux pur beurre.",
            ),
            (
                "Épicerie Fine du Coin",
                "Producteur local",
                "Sélection de conserves artisanales, huiles d'olive et épices.",
            ),
        ]
        foodplaces = []
        for name, place_type, desc in places_templates:
            lon, lat = random_france_point()
            place = FoodPlace.objects.create(
                name=f"{name} ({fake.city()})",
                type=place_type,
                description=desc,
                location=Point(lon, lat),
            )
            foodplaces.append(place)

        self.stdout.write("Création de 15 itinéraires avec étapes et avis...")
        itineraries_templates = [
            (
                "La Route du Cidre et du Camembert",
                "Normandie",
                "Fromage",
                "Un parcours bucolique à travers les vergers normands et les villages à colombages.",
            ),
            (
                "Sentier des Crêperies et Ports Bretons",
                "Bretagne",
                "Fruits de mer",
                "Balade côtière entre terre et mer pour déguster galettes de sarrasin et huîtres fraîches.",
            ),
            (
                "Escapade Gourmande dans le Vignoble Alsacien",
                "Grand-Est",
                "Vin",
                "Tracé pittoresque au pied des châteaux forts à la rencontre des vignerons indépendants.",
            ),
            (
                "Saveurs de Provence et Moulins à Huile",
                "PACA",
                "Végétarien",
                "Itinéraire ensoleillé entre champs de lavande, marchés provençaux et domaines oléicoles.",
            ),
            (
                "Tour des Fromages d'Alpage",
                "Auvergne-Rhône-Alpes",
                "Fromage",
                "Parcours panoramique en altitude avec étapes dans les fruitières et fermes d'alpage.",
            ),
            (
                "Sur la Route du Cassoulet et des Bastides",
                "Occitanie",
                "Viande",
                "Découverte du patrimoine médiéval et des grandes tables généreuses du Sud-Ouest.",
            ),
            (
                "Boucle des Grands Crus et Bouchons",
                "Bourgogne-Franche-Comté",
                "Vin",
                "Voyage gastronomique au cœur des climats classés et des caves voûtées centenaires.",
            ),
            (
                "Entre Océan et Forêt des Landes",
                "Nouvelle-Aquitaine",
                "Poisson",
                "Piste agréable reliant les cabanes ostréicoles aux marchés traditionnels du littoral.",
            ),
            (
                "Les Secrets Gourmands du Maquis",
                "Corse",
                "Fromage",
                "Route sinueuse entre mer et montagne à la découverte du brocciu et de la charcuterie locale.",
            ),
        ]
        sightseeing_templates = [
            (
                "Belvédère Panoramique",
                "Point de vue exceptionnel sur la vallée et les reliefs environnants.",
            ),
            (
                "Village Médiéval",
                "Flânerie dans les ruelles pavées et découverte des remparts historiques.",
            ),
            (
                "Château Historique",
                "Halte culturelle devant l'architecture classée et ses jardins.",
            ),
            (
                "Sentier du Littoral",
                "Passage côtier offrant une vue dégagée sur les falaises.",
            ),
            (
                "Ancien Lavoir & Fontaine",
                "Petit patrimoine rural typique de la région au bord de l'eau.",
            ),
        ]
        comments_samples = [
            "Super itinéraire, les producteurs étaient très accueillants et les produits délicieux !",
            "Très belle balade, l'étape à la fromagerie vaut vraiment le détour.",
            "Parcours bien pensé et accessible, idéal pour un week-end gourmand.",
            "Les paysages sont magnifiques et le marché local du matin était une vraie pépite.",
            "Un peu sportif sur la fin mais la dégustation à l'arrivée récompense largement l'effort !",
        ]
        difficulties = ["Facile", "Moyen", "Difficile"]
        diets = ["Tout", "Végétarien", "Sans gluten", "Sans porc", "Sans lactose"]

        for i in range(15):
            title_base, zone, speciality, facts = random.choice(itineraries_templates)
            start_lon, start_lat = random_france_point()
            path = LineString(
                (start_lon, start_lat),
                (round(start_lon + 0.05, 5), round(start_lat + 0.03, 5)),
                (round(start_lon + 0.10, 5), round(start_lat - 0.02, 5)),
            )

            # Itineraries creation
            itinerary = Itinerary.objects.create(
                title=f"{title_base} #{i + 1}",
                type=random.choice(["Vélo", "Rando", "Moto"]),
                zone=zone,
                distance=round(random.uniform(5.0, 95.0), 1),
                duration=timedelta(hours=random.randint(1, 6)),
                difficulty=random.choice(difficulties),
                diet=random.choice(diets),
                speciality=speciality,
                facts=facts,
                author=random.choice(users),
                path=path,
            )

            # Step creation
            for order in range(1, 4):
                if random.choice([True, False]):
                    # Cas 1 : Étape rattachée à un FoodPlace
                    chosen_place = random.choice(foodplaces)
                    Step.objects.create(
                        name=f"Étape {order} : Pause chez {chosen_place.name}",
                        description=f"Arrêt dégustation ({chosen_place.type.lower()}) et découverte des produits locaux.",
                        step_order=order,
                        location=chosen_place.location,
                        itinerary=itinerary,
                        foodplace=chosen_place,
                    )
                else:
                    poi_name, poi_desc = random.choice(sightseeing_templates)
                    lon, lat = random_france_point()
                    Step.objects.create(
                        name=f"Étape {order} : {poi_name} ({fake.city()})",
                        description=poi_desc,
                        step_order=order,
                        location=Point(lon, lat),
                        itinerary=itinerary,
                        foodplace=None,
                    )

            # Comment creation
            Comment.objects.create(
                content=random.choice(comments_samples),
                review=random.randint(3, 5),
                author=random.choice(users),
                itinerary=itinerary,
            )

            # Favorite creation
            Favorite.objects.get_or_create(
                user=random.choice(users),
                itinerary=itinerary,
            )
        self.stdout.write(
            self.style.SUCCESS("Base de données locale remplie avec succès !")
        )
