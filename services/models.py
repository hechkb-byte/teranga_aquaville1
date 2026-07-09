from django.db import models


class ServiceInclus(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icone = models.CharField(max_length=50, help_text="Classe CSS ou nom d'icône (ex: 'pool', 'sports_soccer')")
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Service inclus"
        verbose_name_plural = "Services inclus"
        ordering = ['ordre']

    def __str__(self):
        return self.nom


class TarifParcAquatique(models.Model):
    CATEGORIE_CHOICES = [
        ('enfant_05', 'Enfants 0–5 ans'),
        ('enfant_512', 'Enfants 5–12 ans'),
        ('accompagnant', 'Accompagnant'),
        ('adolescent', 'Adolescents 12–18 ans'),
        ('adulte', 'Adultes (+18 ans)'),
        ('toboggan', 'Toboggans haute attraction'),
        ('vip', 'Accès VIP'),
    ]

    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, unique=True)
    prix_visiteur = models.PositiveIntegerField(help_text="Prix en FCFA (0 = gratuit)")
    prix_resident = models.PositiveIntegerField(help_text="Prix en FCFA (0 = gratuit)")
    gratuit = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Tarif parc aquatique"
        verbose_name_plural = "Tarifs parc aquatique"

    def __str__(self):
        return self.get_categorie_display()


class SoinSpa(models.Model):
    TYPE_CHOICES = [
        ('soin', 'Soin individuel'),
        ('forfait', 'Forfait'),
    ]

    type_soin = models.CharField(max_length=10, choices=TYPE_CHOICES, default='soin')
    nom = models.CharField(max_length=150)
    duree = models.CharField(max_length=50, blank=True, help_text="Ex: 30 min, 1 heure")
    prix_teranga = models.PositiveIntegerField(help_text="Prix en FCFA")
    prix_resident = models.PositiveIntegerField(help_text="Prix en FCFA")
    contenu = models.TextField(blank=True, help_text="Description du forfait (pour les forfaits uniquement)")
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Soin Spa"
        verbose_name_plural = "Soins Spa"
        ordering = ['type_soin', 'ordre']

    def __str__(self):
        return f"{self.nom} ({self.get_type_soin_display()})"
