from django.contrib import admin
from .models import User, Team, Match, Pull, MatchHistory, Notification
from .models import PartidoAbierto
from .models import Convocatoria, ConvocatoriaJugador, ConvocatoriaPareja, ParejaEnPistaConvocatoria




# Registrar modelos en el panel de admin
admin.site.register(User)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Pull)
admin.site.register(MatchHistory)
admin.site.register(PartidoAbierto)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'created_at', 'is_read', 'send_email')
    list_filter = ('notification_type', 'is_read', 'send_email')
    search_fields = ('user__username', 'message')


# convocatorias

admin.site.register(Convocatoria)
admin.site.register(ConvocatoriaJugador)
admin.site.register(ConvocatoriaPareja)
admin.site.register(ParejaEnPistaConvocatoria)