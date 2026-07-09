from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import ServiceInclus, TarifParcAquatique, SoinSpa


class ServiceInclusAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'icone', 'ordre']
    list_editable = ['ordre']
    save_on_top   = True
    search_fields = ['nom']


class TarifParcAquatiqueAdmin(admin.ModelAdmin):
    list_display  = ['categorie', 'prix_visiteur_fmt', 'prix_resident_fmt', 'badge_gratuit']
    list_filter   = ['gratuit']
    save_on_top   = True

    def prix_visiteur_fmt(self, obj):
        if obj.gratuit:
            return mark_safe('<span style="color:#94a3b8;font-style:italic;">Gratuit</span>')
        return format_html('<strong>{} FCFA</strong>', '{:,}'.format(obj.prix_visiteur).replace(',', ' '))
    prix_visiteur_fmt.short_description = "Prix visiteur"

    def prix_resident_fmt(self, obj):
        if obj.gratuit:
            return mark_safe('<span style="color:#94a3b8;font-style:italic;">Gratuit</span>')
        return format_html('<strong>{} FCFA</strong>', '{:,}'.format(obj.prix_resident).replace(',', ' '))
    prix_resident_fmt.short_description = "Prix résident"

    def badge_gratuit(self, obj):
        if obj.gratuit:
            return mark_safe('<span style="background:#d1fae5;color:#065f46;padding:2px 10px;border-radius:9999px;font-size:11px;font-weight:700;">✓ Gratuit</span>')
        return ''
    badge_gratuit.short_description = "Gratuit"


class SoinSpaAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'badge_type', 'duree_fmt', 'prix_teranga_fmt', 'prix_resident_fmt', 'ordre']
    list_filter   = ['type_soin']
    list_editable = ['ordre']
    save_on_top   = True
    search_fields = ['nom']

    def badge_type(self, obj):
        colors = {
            'soin':    ('#e0f2fe', '#0369a1', 'Soin'),
            'forfait': ('#fef9c3', '#854d0e', 'Forfait'),
        }
        bg, fg, label = colors.get(obj.type_soin, ('#f1f5f9', '#64748b', obj.type_soin))
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;">{}</span>',
            bg, fg, label
        )
    badge_type.short_description = "Type"

    def duree_fmt(self, obj):
        if obj.duree:
            return format_html('<span style="color:#64748b;">{} min</span>', obj.duree)
        return '—'
    duree_fmt.short_description = "Durée"

    def prix_teranga_fmt(self, obj):
        return format_html('<strong>{} FCFA</strong>', '{:,}'.format(obj.prix_teranga).replace(',', ' '))
    prix_teranga_fmt.short_description = "Prix Teranga"

    def prix_resident_fmt(self, obj):
        return format_html('{} FCFA', '{:,}'.format(obj.prix_resident).replace(',', ' '))
    prix_resident_fmt.short_description = "Prix résident"


def register_to(site):
    site.register(ServiceInclus, ServiceInclusAdmin)
    site.register(TarifParcAquatique, TarifParcAquatiqueAdmin)
    site.register(SoinSpa, SoinSpaAdmin)
