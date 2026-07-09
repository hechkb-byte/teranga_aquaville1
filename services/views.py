from django.shortcuts import render
from .models import ServiceInclus, TarifParcAquatique, SoinSpa


def services_inclus(request):
    services = ServiceInclus.objects.all()
    return render(request, 'services/inclus.html', {'services': services})


def parc_aquatique(request):
    tarifs = TarifParcAquatique.objects.all()
    return render(request, 'services/parc.html', {'tarifs': tarifs})


def spa(request):
    soins = SoinSpa.objects.filter(type_soin='soin')
    forfaits = SoinSpa.objects.filter(type_soin='forfait')
    return render(request, 'services/spa.html', {'soins': soins, 'forfaits': forfaits})


def restauration(request):
    return render(request, 'services/restauration.html')
