import hashlib
import logging

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings

from .forms import DemandeContactForm
from .models import DemandeContact

logger = logging.getLogger(__name__)

# ── Rate limiting ──────────────────────────────────────────────────────
_RATE_LIMIT   = 3          # soumissions max
_RATE_WINDOW  = 60 * 10   # par fenêtre de 10 minutes


def _get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR', '')


def _is_rate_limited(request):
    ip   = _get_client_ip(request)
    key  = 'contact_rate_' + hashlib.sha256(ip.encode()).hexdigest()[:16]
    hits = cache.get(key, 0)
    if hits >= _RATE_LIMIT:
        return True
    cache.set(key, hits + 1, _RATE_WINDOW)
    return False


# ── Views ──────────────────────────────────────────────────────────────

def contact(request):
    error_rate = False

    if request.method == 'POST':
        if _is_rate_limited(request):
            error_rate = True
        else:
            form = DemandeContactForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data

                demande = DemandeContact.objects.create(
                    type_bien = cd['type_bien'],
                    budget    = cd.get('budget', ''),
                    prenom    = cd['prenom'],
                    nom       = cd['nom'],
                    email     = cd['email'],
                    telephone = cd['telephone'],
                    message   = cd.get('message', ''),
                )

                sujet = f"Nouvelle demande — {demande.get_type_bien_display()}"
                corps = (
                    f"Nom : {demande.prenom} {demande.nom}\n"
                    f"Email : {demande.email}\n"
                    f"Téléphone : {demande.telephone}\n"
                    f"Type de bien : {demande.get_type_bien_display()}\n"
                    f"Budget : {demande.get_budget_display()}\n\n"
                    f"Message :\n{demande.message}"
                )

                try:
                    send_mail(
                        sujet, corps,
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.CONTACT_EMAIL],
                        fail_silently=False,
                    )
                except Exception:
                    logger.exception("Erreur envoi email demande #%s", demande.pk)

                return redirect('contact_succes')
    else:
        form = DemandeContactForm()

    return render(request, 'contact/contact.html', {
        'form': form,
        'error_rate': error_rate,
    })


def contact_succes(request):
    return render(request, 'contact/succes.html')
