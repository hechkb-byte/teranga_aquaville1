import re
from django import forms
from .models import DemandeContact

VALID_TYPE_BIEN = {c[0] for c in DemandeContact.TYPE_BIEN_CHOICES}
VALID_BUDGET    = {c[0] for c in DemandeContact.BUDGET_CHOICES}


class DemandeContactForm(forms.Form):
    # Champ honeypot caché — les bots le remplissent, les humains non
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    # Étape 1
    type_bien = forms.ChoiceField(choices=DemandeContact.TYPE_BIEN_CHOICES)

    # Étape 2
    budget = forms.ChoiceField(
        choices=[('', '—')] + list(DemandeContact.BUDGET_CHOICES),
        required=False,
    )

    # Étape 3
    prenom    = forms.CharField(max_length=100, strip=True)
    nom       = forms.CharField(max_length=100, strip=True)
    email     = forms.EmailField(max_length=254)
    telephone = forms.CharField(max_length=30, strip=True)
    message   = forms.CharField(max_length=2000, required=False, strip=True)

    def clean_website(self):
        """Honeypot : si ce champ est rempli, c'est un bot."""
        value = self.cleaned_data.get('website', '')
        if value:
            raise forms.ValidationError("Soumission refusée.")
        return value

    def clean_type_bien(self):
        value = self.cleaned_data.get('type_bien', '')
        if value not in VALID_TYPE_BIEN:
            raise forms.ValidationError("Type de bien invalide.")
        return value

    def clean_budget(self):
        value = self.cleaned_data.get('budget', '')
        if value and value not in VALID_BUDGET:
            raise forms.ValidationError("Budget invalide.")
        return value

    def clean_prenom(self):
        value = self.cleaned_data.get('prenom', '')
        if not re.search(r'[a-zA-ZÀ-ÿ]', value):
            raise forms.ValidationError("Prénom invalide.")
        return value

    def clean_nom(self):
        value = self.cleaned_data.get('nom', '')
        if not re.search(r'[a-zA-ZÀ-ÿ]', value):
            raise forms.ValidationError("Nom invalide.")
        return value

    def clean_telephone(self):
        tel = self.cleaned_data.get('telephone', '')
        digits = re.sub(r'[\s\+\-\.\(\)]', '', tel)
        if not digits.isdigit() or not (6 <= len(digits) <= 15):
            raise forms.ValidationError("Numéro de téléphone invalide (6 à 15 chiffres).")
        return tel
