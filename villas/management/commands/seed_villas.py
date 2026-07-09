from django.core.management.base import BaseCommand
from villas.models import Villa, VillaImage, TarifVente, TarifLocation, AppelFonds


VILLAS = [
    {
        "numero": 1,
        "nom": "AYO",
        "type_villa": "F4",
        "categorie": "standard",
        "superficie": 120,
        "capacite": 6,
        "description": (
            "Villa AYO, un havre de paix niché dans le complexe Teranga Aquaville. "
            "Ses espaces lumineux et ses finitions haut de gamme en font la résidence idéale "
            "pour les familles à la recherche du confort et du dépaysement sur la Petite Côte."
        ),
        "equipements": "Piscine privée, Climatisation, Cuisine équipée, Terrasse, Wi-Fi, TV écran plat, Parking",
        "disponible_vente": True,
        "disponible_location": True,
        "image_principale": "villas/villa-ayo-principale.png",
        "galerie": ["villas/villa-ayo-2.png"],
    },
    {
        "numero": 2,
        "nom": "Pasteur BEN",
        "type_villa": "F5",
        "categorie": "bord_mer",
        "superficie": 160,
        "capacite": 8,
        "description": (
            "La Villa Pasteur BEN jouit d'une position privilégiée en bord de mer, "
            "avec une vue imprenable sur l'Atlantique. Spacieuse et raffinée, elle offre "
            "tout le confort nécessaire pour un séjour d'exception à Pointe Sarène."
        ),
        "equipements": "Vue mer, Piscine privée, Climatisation, Cuisine équipée, Grande terrasse, Wi-Fi, TV écran plat, Parking, Jardin",
        "disponible_vente": True,
        "disponible_location": True,
        "image_principale": "villas/villa-pasteur-ben-principale.png",
        "galerie": ["villas/villa-pasteur-ben-2.png"],
    },
    {
        "numero": 3,
        "nom": "Touba",
        "type_villa": "F6",
        "categorie": "standard",
        "superficie": 220,
        "capacite": 12,
        "description": (
            "La Villa Touba est la plus grande et la plus prestigious résidence du complexe. "
            "Avec ses 220 m² et sa capacité de 12 personnes, elle est parfaite pour les grandes "
            "familles et les événements privés au cœur du complexe Teranga Aquaville."
        ),
        "equipements": "Grande piscine, Climatisation, Cuisine professionnelle, Terrasse XL, Wi-Fi haut débit, TV 4K, Parking 3 véhicules, Jardin tropical, Salle de jeux",
        "disponible_vente": True,
        "disponible_location": True,
        "image_principale": "villas/villa-touba-principale.png",
        "galerie": ["villas/villa-touba-2.png"],
    },
]

TARIFS_VENTE = [
    {"type_villa": "F4", "categorie": "standard",  "prix": 45_000_000},
    {"type_villa": "F5", "categorie": "bord_mer",  "prix": 75_000_000},
    {"type_villa": "F6", "categorie": "standard",  "prix": 110_000_000},
]

TARIFS_LOCATION = [
    {"type_villa": "F4", "categorie": "standard", "duree": "nuit", "prix": 150_000},
    {"type_villa": "F4", "categorie": "standard", "duree": "mois", "prix": 2_500_000},
    {"type_villa": "F5", "categorie": "bord_mer", "duree": "nuit", "prix": 250_000},
    {"type_villa": "F5", "categorie": "bord_mer", "duree": "mois", "prix": 4_000_000},
    {"type_villa": "F6", "categorie": "standard", "duree": "nuit", "prix": 400_000},
    {"type_villa": "F6", "categorie": "standard", "duree": "mois", "prix": 6_500_000},
]

# Appels de fonds VEFA (% par étape — total 100%)
APPELS = [
    (1, "5.00"),
    (2, "10.00"),
    (3, "15.00"),
    (4, "20.00"),
    (5, "15.00"),
    (6, "15.00"),
    (7, "15.00"),
    (8, "5.00"),
]


class Command(BaseCommand):
    help = "Peuple la base avec les 3 villas réelles et leurs tarifs"

    def handle(self, *args, **options):
        self._seed_tarifs()
        self._seed_villas()
        self.stdout.write(self.style.SUCCESS("Base de données peuplée avec succès !"))

    def _seed_tarifs(self):
        for t in TARIFS_VENTE:
            tv, created = TarifVente.objects.get_or_create(
                type_villa=t["type_villa"],
                categorie=t["categorie"],
                defaults={"prix": t["prix"]},
            )
            if created:
                for etape, pct in APPELS:
                    montant = int(tv.prix * float(pct) / 100)
                    AppelFonds.objects.get_or_create(
                        tarif_vente=tv,
                        etape=etape,
                        defaults={"pourcentage": pct, "montant": montant},
                    )
                self.stdout.write(f"  Tarif vente créé : {tv}")

        for t in TARIFS_LOCATION:
            tl, created = TarifLocation.objects.get_or_create(
                type_villa=t["type_villa"],
                categorie=t["categorie"],
                duree=t["duree"],
                defaults={"prix": t["prix"]},
            )
            if created:
                self.stdout.write(f"  Tarif location créé : {tl}")

    def _seed_villas(self):
        for data in VILLAS:
            galerie = data.pop("galerie")
            image_principale = data.pop("image_principale")

            villa, created = Villa.objects.get_or_create(
                numero=data["numero"],
                defaults={**data, "image_principale": image_principale},
            )

            if not created:
                self.stdout.write(f"  Villa {villa.nom} existe déjà — ignorée")
                continue

            for i, img_path in enumerate(galerie):
                VillaImage.objects.get_or_create(
                    villa=villa,
                    image=img_path,
                    defaults={"ordre": i + 1},
                )

            self.stdout.write(f"  Villa créée : {villa}")
