from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Villa, VillaImage, TarifVente, AppelFonds, TarifLocation


# ── Actions ───────────────────────────────────────────────────────────

@admin.action(description="📦 Archiver les villas sélectionnées")
def archiver_villas(modeladmin, request, queryset):
    updated = queryset.update(is_archived=True)
    modeladmin.message_user(request, f"{updated} villa(s) archivée(s).")


@admin.action(description="♻️ Restaurer les villas sélectionnées")
def restaurer_villas(modeladmin, request, queryset):
    updated = queryset.update(is_archived=False)
    modeladmin.message_user(request, f"{updated} villa(s) restaurée(s).")


@admin.action(description="✅ Rendre disponible à la vente")
def activer_vente(modeladmin, request, queryset):
    queryset.update(disponible_vente=True)


@admin.action(description="❌ Retirer de la vente")
def desactiver_vente(modeladmin, request, queryset):
    queryset.update(disponible_vente=False)


@admin.action(description="✅ Rendre disponible à la location")
def activer_location(modeladmin, request, queryset):
    queryset.update(disponible_location=True)


@admin.action(description="❌ Retirer de la location")
def desactiver_location(modeladmin, request, queryset):
    queryset.update(disponible_location=False)


# ── Inlines ───────────────────────────────────────────────────────────

class VillaImageInline(admin.TabularInline):
    model = VillaImage
    extra = 3
    fields = ['image', 'legende', 'ordre']


class AppelFondsInline(admin.TabularInline):
    model = AppelFonds
    extra = 0
    fields = ['etape', 'pourcentage', 'montant']
    readonly_fields = []


# ── Villa Admin ───────────────────────────────────────────────────────

class VillaAdmin(admin.ModelAdmin):
    list_display = [
        'numero', 'nom', 'type_villa', 'categorie', 'superficie', 'capacite',
        'badge_vente', 'badge_location', 'badge_archive',
    ]
    list_filter   = ['type_villa', 'categorie', 'disponible_vente', 'disponible_location', 'is_archived']
    search_fields = ['nom', 'numero', 'description']
    actions = [archiver_villas, restaurer_villas, activer_vente, desactiver_vente, activer_location, desactiver_location]
    inlines = [VillaImageInline]
    save_on_top = True

    fieldsets = (
        ('Identification', {
            'fields': ('numero', 'type_villa', 'categorie', 'slug')
        }),
        ('Caractéristiques', {
            'fields': ('superficie', 'capacite', 'description', 'equipements', 'image_principale')
        }),
        ('Disponibilité', {
            'fields': ('disponible_vente', 'disponible_location', 'is_archived'),
            'description': "Une villa archivée n'apparaît plus sur le site public mais reste récupérable."
        }),
    )

    def badge_vente(self, obj):
        if obj.disponible_vente:
            return mark_safe('<span style="background:#d1fae5;color:#065f46;padding:2px 10px;border-radius:9999px;font-size:11px;font-weight:700;">Vente ✓</span>')
        return mark_safe('<span style="background:#fee2e2;color:#991b1b;padding:2px 10px;border-radius:9999px;font-size:11px;font-weight:700;">Vente ✗</span>')
    badge_vente.short_description = "Vente"

    def badge_location(self, obj):
        if obj.disponible_location:
            return mark_safe('<span style="background:#dbeafe;color:#1e40af;padding:2px 10px;border-radius:9999px;font-size:11px;font-weight:700;">Location ✓</span>')
        return mark_safe('<span style="background:#fee2e2;color:#991b1b;padding:2px 10px;border-radius:9999px;font-size:11px;font-weight:700;">Location ✗</span>')
    badge_location.short_description = "Location"

    def badge_archive(self, obj):
        if obj.is_archived:
            return mark_safe('<span style="background:#fef3c7;color:#92400e;padding:2px 10px;border-radius:9999px;font-size:11px;font-weight:700;">🗄 Archivée</span>')
        return mark_safe('<span style="background:#f0fdf4;color:#166534;padding:2px 10px;border-radius:9999px;font-size:11px;font-weight:700;">Active</span>')
    badge_archive.short_description = "Statut"


# ── TarifVente Admin ──────────────────────────────────────────────────

class TarifVenteAdmin(admin.ModelAdmin):
    list_display  = ['type_villa', 'categorie', 'prix_formate']
    list_filter   = ['type_villa', 'categorie']
    inlines       = [AppelFondsInline]
    save_on_top   = True

    def prix_formate(self, obj):
        return format_html('<strong>{} FCFA</strong>', '{:,}'.format(obj.prix).replace(',', ' '))
    prix_formate.short_description = "Prix"


# ── TarifLocation Admin ───────────────────────────────────────────────

class TarifLocationAdmin(admin.ModelAdmin):
    list_display = ['type_villa', 'categorie', 'duree', 'prix_formate']
    list_filter  = ['type_villa', 'categorie', 'duree']
    show_facets  = admin.ShowFacets.NEVER

    def prix_formate(self, obj):
        return format_html('<strong>{} FCFA</strong>', '{:,}'.format(obj.prix).replace(',', ' '))
    prix_formate.short_description = "Prix"


# ── Register ──────────────────────────────────────────────────────────

def register_to(site):
    site.register(Villa, VillaAdmin)
    site.register(TarifVente, TarifVenteAdmin)
    site.register(TarifLocation, TarifLocationAdmin)
