from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from villas.models import Villa
from services.models import SoinSpa
from contact.models import DemandeContact


class TerangaAdminSite(AdminSite):
    site_header = "Teranga Aquaville"
    site_title  = "Admin — Teranga Aquaville"
    index_title = "Tableau de bord"

    def each_context(self, request):
        context = super().each_context(request)
        context['pending_count'] = DemandeContact.objects.filter(traite=False).count()
        return context

    def logout(self, request, extra_context=None):
        from django.contrib.auth.views import LogoutView
        defaults = {
            "next_page": "/",
            "extra_context": {
                **self.each_context(request),
                "has_permission": False,
                **(extra_context or {}),
            },
        }
        if self.logout_template is not None:
            defaults["template_name"] = self.logout_template
        request.current_app = self.name
        return LogoutView.as_view(**defaults)(request)

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['stats'] = {
            'nb_villas':             Villa.objects.count(),
            'demandes_non_traitees': DemandeContact.objects.filter(traite=False).count(),
            'demandes_traitees':     DemandeContact.objects.filter(traite=True).count(),
            'nb_soins':              SoinSpa.objects.count(),
        }
        extra_context['dernieres_demandes'] = DemandeContact.objects.order_by('-date_envoi')[:8]
        return super().index(request, extra_context)


def build_admin_site():
    from django.contrib.admin.sites import AdminSite as DjangoAdminSite
    from django.contrib.auth.admin import UserAdmin, GroupAdmin

    site = TerangaAdminSite(name='admin')

    # Auth
    site.register(User, UserAdmin)
    site.register(Group, GroupAdmin)

    # Apps
    from villas.admin import register_to as villas_register
    from services.admin import register_to as services_register
    from contact.admin import register_to as contact_register

    villas_register(site)
    services_register(site)
    contact_register(site)

    return site
