from django.db import models


class DemandeContact(models.Model):
    TYPE_BIEN_CHOICES = [
        ('vente_f4', 'Villa à vendre — F4'),
        ('vente_f5', 'Villa à vendre — F5'),
        ('vente_f6', 'Villa à vendre — F6'),
        ('location_nuit', 'Villa à louer — courte durée'),
        ('location_mois', 'Villa à louer — longue durée'),
        ('parc', 'Parc aquatique'),
        ('spa', 'Spa & Massage'),
        ('autre', 'Autre demande'),
    ]

    BUDGET_CHOICES = [
        ('moins_175m', 'Moins de 175M FCFA'),
        ('175_240m', '175M – 240M FCFA'),
        ('240_320m', '240M – 320M FCFA'),
        ('plus_320m', 'Plus de 320M FCFA'),
        ('location', 'Location (pas d\'achat)'),
    ]

    # Étape 1 — type de bien
    type_bien = models.CharField(max_length=20, choices=TYPE_BIEN_CHOICES, verbose_name="Type de bien")
    # Étape 2 — budget
    budget = models.CharField(max_length=20, choices=BUDGET_CHOICES, blank=True, verbose_name="Budget")
    # Étape 3 — coordonnées
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    message = models.TextField(blank=True)

    # Métadonnées
    date_envoi = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False, verbose_name="Traité")
    notes_internes = models.TextField(blank=True, verbose_name="Notes internes")
    is_archived = models.BooleanField(default=False, verbose_name="Archivée")

    class Meta:
        verbose_name = "Demande de contact"
        verbose_name_plural = "Demandes de contact"
        ordering = ['-date_envoi']

    def __str__(self):
        return f"{self.prenom} {self.nom} — {self.get_type_bien_display()} — {self.date_envoi.strftime('%d/%m/%Y')}"
