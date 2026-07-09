from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import DemandeContact


# ── Actions ───────────────────────────────────────────────────────────

@admin.action(description="✅ Marquer comme traité")
def marquer_traite(modeladmin, request, queryset):
    updated = queryset.update(traite=True)
    modeladmin.message_user(request, f"{updated} demande(s) marquée(s) comme traitée(s).")


@admin.action(description="🔄 Marquer comme non traité")
def marquer_non_traite(modeladmin, request, queryset):
    updated = queryset.update(traite=False)
    modeladmin.message_user(request, f"{updated} demande(s) remise(s) en attente.")


@admin.action(description="📦 Archiver les demandes sélectionnées")
def archiver_demandes(modeladmin, request, queryset):
    updated = queryset.update(is_archived=True)
    modeladmin.message_user(request, f"{updated} demande(s) archivée(s).")


@admin.action(description="♻️ Restaurer les demandes sélectionnées")
def restaurer_demandes(modeladmin, request, queryset):
    updated = queryset.update(is_archived=False)
    modeladmin.message_user(request, f"{updated} demande(s) restaurée(s).")


# ── Admin ─────────────────────────────────────────────────────────────

class DemandeContactAdmin(admin.ModelAdmin):
    list_display  = [
        'nom_complet', 'email', 'telephone',
        'badge_type', 'badge_budget', 'date_envoi',
        'badge_traite', 'badge_archive',
    ]
    list_filter   = ['type_bien', 'traite', 'is_archived']
    search_fields = ['nom', 'prenom', 'email', 'telephone']
    readonly_fields = ['date_envoi']
    actions = [marquer_traite, marquer_non_traite, archiver_demandes, restaurer_demandes]
    save_on_top   = True
    date_hierarchy = 'date_envoi'

    fieldsets = (
        ('Demande', {
            'fields': ('type_bien', 'budget', 'message')
        }),
        ('Coordonnées', {
            'fields': ('prenom', 'nom', 'email', 'telephone')
        }),
        ('Suivi interne', {
            'fields': ('traite', 'is_archived', 'notes_internes', 'date_envoi'),
            'description': "Cochez « Archivée » pour masquer cette demande sans la supprimer définitivement."
        }),
    )

    def nom_complet(self, obj):
        return format_html('<strong>{} {}</strong>', obj.prenom, obj.nom)
    nom_complet.short_description = "Contact"
    nom_complet.admin_order_field = 'nom'

    def badge_type(self, obj):
        return format_html(
            '<span style="background:#e0f2fe;color:#0369a1;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;">{}</span>',
            obj.get_type_bien_display()
        )
    badge_type.short_description = "Type"

    def badge_budget(self, obj):
        if not obj.budget:
            return mark_safe('<span style="color:#94a3b8;font-size:11px;">—</span>')
        return format_html(
            '<span style="background:#fef9c3;color:#854d0e;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;">{}</span>',
            obj.get_budget_display()
        )
    badge_budget.short_description = "Budget"

    def badge_traite(self, obj):
        if obj.traite:
            return mark_safe('<span style="background:#d1fae5;color:#065f46;padding:2px 10px;border-radius:9999px;font-size:11px;font-weight:700;">✓ Traité</span>')
        return mark_safe('<span style="background:#fef3c7;color:#92400e;padding:2px 10px;border-radius:9999px;font-size:11px;font-weight:700;">⏳ En attente</span>')
    badge_traite.short_description = "Statut"

    def badge_archive(self, obj):
        if obj.is_archived:
            return mark_safe('<span style="background:#f1f5f9;color:#64748b;padding:2px 10px;border-radius:9999px;font-size:11px;font-weight:700;">🗄 Archivée</span>')
        return ''
    badge_archive.short_description = "Archive"


# ── Register ──────────────────────────────────────────────────────────

def register_to(site):
    site.register(DemandeContact, DemandeContactAdmin)
