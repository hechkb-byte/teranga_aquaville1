from django.db import models


class Villa(models.Model):
    TYPE_CHOICES = [
        ('F4', 'F4 (6 pers. min.)'),
        ('F5', 'F5 (8 pers. min.)'),
        ('F6', 'F6 (12 pers. min.)'),
    ]
    CATEGORIE_CHOICES = [
        ('standard', 'Standard'),
        ('bord_mer', 'Bord de mer'),
    ]

    numero = models.PositiveSmallIntegerField(verbose_name="Numéro de villa")
    nom = models.CharField(max_length=100, blank=True, verbose_name="Nom de la villa")
    type_villa = models.CharField(max_length=2, choices=TYPE_CHOICES)
    categorie = models.CharField(max_length=10, choices=CATEGORIE_CHOICES)
    superficie = models.PositiveIntegerField(help_text="en m²")
    capacite = models.PositiveSmallIntegerField(verbose_name="Capacité (personnes)")
    description = models.TextField(blank=True)
    equipements = models.TextField(
        blank=True,
        help_text="Liste des équipements séparés par des virgules"
    )
    disponible_vente = models.BooleanField(default=True)
    disponible_location = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False, verbose_name="Archivée")
    image_principale = models.ImageField(upload_to='villas/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Villa"
        ordering = ['numero']

    def __str__(self):
        if self.nom:
            return f"Villa {self.nom} — {self.type_villa} {self.get_categorie_display()}"
        return f"Villa {self.numero} — {self.type_villa} {self.get_categorie_display()}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = self.nom.lower().replace(' ', '-') if self.nom else str(self.numero)
            self.slug = f"villa-{base}-{self.type_villa.lower()}-{self.categorie}"
        super().save(*args, **kwargs)

    def get_equipements_list(self):
        return [e.strip() for e in self.equipements.split(',') if e.strip()]


class VillaImage(models.Model):
    villa = models.ForeignKey(Villa, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='villas/galerie/')
    legende = models.CharField(max_length=200, blank=True)
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return f"Photo {self.ordre} — {self.villa}"


class TarifVente(models.Model):
    type_villa = models.CharField(max_length=2, choices=Villa.TYPE_CHOICES)
    categorie = models.CharField(max_length=10, choices=Villa.CATEGORIE_CHOICES)
    prix = models.BigIntegerField(help_text="Prix en FCFA")

    class Meta:
        verbose_name = "Tarif vente VEFA"
        unique_together = ('type_villa', 'categorie')

    def __str__(self):
        return f"{self.type_villa} {self.categorie} — {self.prix:,} FCFA"


class AppelFonds(models.Model):
    ETAPES = [
        (1, 'Contrat de réservation'),
        (2, 'Acte authentique'),
        (3, 'Fondations'),
        (4, 'Plancher / RDC'),
        (5, 'Toiture / étanchéité'),
        (6, 'Cloisons'),
        (7, 'Achèvement'),
        (8, 'Remise des clés'),
    ]

    tarif_vente = models.ForeignKey(TarifVente, on_delete=models.CASCADE, related_name='appels_fonds')
    etape = models.PositiveSmallIntegerField(choices=ETAPES)
    pourcentage = models.DecimalField(max_digits=5, decimal_places=2)
    montant = models.BigIntegerField(help_text="Montant en FCFA")

    class Meta:
        ordering = ['etape']
        unique_together = ('tarif_vente', 'etape')

    def __str__(self):
        return f"Appel {self.etape} — {self.tarif_vente} — {self.pourcentage}%"


class TarifLocation(models.Model):
    DUREE_CHOICES = [
        ('nuit', 'Nuitée'),
        ('mois', 'Mensuel'),
    ]

    type_villa = models.CharField(max_length=2, choices=Villa.TYPE_CHOICES)
    categorie = models.CharField(max_length=10, choices=Villa.CATEGORIE_CHOICES)
    duree = models.CharField(max_length=5, choices=DUREE_CHOICES)
    prix = models.BigIntegerField(help_text="Prix en FCFA")

    class Meta:
        verbose_name = "Tarif location"
        unique_together = ('type_villa', 'categorie', 'duree')

    def __str__(self):
        return f"{self.type_villa} {self.categorie} ({self.duree}) — {self.prix:,} FCFA"
