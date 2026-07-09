from django.shortcuts import render, get_object_or_404
from .models import Villa, TarifVente, TarifLocation


def home(request):
    villas_sample = Villa.objects.filter(disponible_vente=True, is_archived=False)[:3]
    return render(request, 'home.html', {'villas_sample': villas_sample})


def villas_vente(request):
    type_filtre = request.GET.get('type', '')
    categorie_filtre = request.GET.get('categorie', '')

    villas = Villa.objects.filter(disponible_vente=True, is_archived=False)
    if type_filtre:
        villas = villas.filter(type_villa=type_filtre)
    if categorie_filtre:
        villas = villas.filter(categorie=categorie_filtre)

    tarifs = TarifVente.objects.prefetch_related('appels_fonds').all()

    return render(request, 'villas/vente.html', {
        'villas': villas,
        'tarifs': tarifs,
        'type_filtre': type_filtre,
        'categorie_filtre': categorie_filtre,
    })


def villa_detail_vente(request, slug):
    villa = get_object_or_404(Villa, slug=slug, disponible_vente=True, is_archived=False)
    tarif = TarifVente.objects.filter(
        type_villa=villa.type_villa,
        categorie=villa.categorie
    ).prefetch_related('appels_fonds').first()

    return render(request, 'villas/detail_vente.html', {
        'villa': villa,
        'tarif': tarif,
    })


def villas_location(request):
    type_filtre = request.GET.get('type', '')
    categorie_filtre = request.GET.get('categorie', '')

    villas = Villa.objects.filter(disponible_location=True, is_archived=False)
    if type_filtre:
        villas = villas.filter(type_villa=type_filtre)
    if categorie_filtre:
        villas = villas.filter(categorie=categorie_filtre)

    tarifs_nuit = {
        (t.type_villa, t.categorie): t.prix
        for t in TarifLocation.objects.filter(duree='nuit')
    }
    tarifs_mois = {
        (t.type_villa, t.categorie): t.prix
        for t in TarifLocation.objects.filter(duree='mois')
    }

    return render(request, 'villas/location.html', {
        'villas': villas,
        'tarifs_nuit': tarifs_nuit,
        'tarifs_mois': tarifs_mois,
        'type_filtre': type_filtre,
        'categorie_filtre': categorie_filtre,
    })
