from django.shortcuts import render
from .models import FamilyMember


def family_tree_view(request):
    members = FamilyMember.objects.prefetch_related("spouses").select_related("mother", "father").all()

    family_data = []
    for m in members:
        family_data.append({
            "id": m.id,
            "name": m.name,
            "gender": m.gender,
            "born": m.born,
            "died": m.died,
            "occupation": m.occupation,
            "location": m.location,
            "bio": m.bio,
            "photo": m.photo.url if m.photo else None,
            "motherId": m.mother.id if m.mother else None,
            "fatherId": m.father.id if m.father else None,
            "spouseIds": [sp.id for sp in m.spouses.all()],
        })

    return render(request, "family_tree.html", {
        "family_data": family_data
    })