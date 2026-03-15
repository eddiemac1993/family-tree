from django.contrib import admin
from .models import FamilyMember


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "gender", "born", "died", "mother", "father")
    search_fields = ("name", "occupation", "location", "bio")
    list_filter = ("gender", "born")
    filter_horizontal = ("spouses",)
    autocomplete_fields = ("mother", "father")