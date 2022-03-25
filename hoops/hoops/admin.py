from django.contrib import admin
from django.utils.html import format_html
from . models import League, Player, Match, PlayerStats


# Register your models here.
admin.site.site_header = 'Hoops'
admin.site.index_title = 'Admin' 
admin.site.site_title = admin.site.site_header


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):

    list_display = ('league', 'played_on', 'hosts', "guests",)
    

    def get_host_result(self, obj):
        return 'W' if obj.host_score > obj.guest_score else 'L'

    def get_guest_result(self, obj):
        return 'W' if obj.guest_score > obj.host_score else 'L'

    def hosts(self, obj):
        return format_html(self.get_host_result(obj) + " - " + f"<br/>{self.get_host_result(obj)} - ".join([p.name for p in obj.host.all()]))
    
    def guests(self, obj):
        return format_html(self.get_guest_result(obj) + " - " + f"<br/>{self.get_guest_result(obj)} - ".join([p.name for p in obj.guest.all()]))