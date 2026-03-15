from django.db import models
from django.core.exceptions import ValidationError


class FamilyMember(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    born = models.PositiveIntegerField(null=True, blank=True)
    died = models.PositiveIntegerField(null=True, blank=True)
    occupation = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="family_photos/", null=True, blank=True)

    mother = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children_from_mother",
        limit_choices_to={"gender": "female"},
    )
    father = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children_from_father",
        limit_choices_to={"gender": "male"},
    )

    spouses = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=True
    )

    class Meta:
        ordering = ["born", "name"]

    def __str__(self):
        years = ""
        if self.born:
            years = f" ({self.born}"
            if self.died:
                years += f" - {self.died}"
            years += ")"
        return f"{self.name}{years}"

    def clean(self):
        if self.mother and self.mother == self:
            raise ValidationError({"mother": "A person cannot be their own mother."})

        if self.father and self.father == self:
            raise ValidationError({"father": "A person cannot be their own father."})

        if self.died and self.born and self.died < self.born:
            raise ValidationError({"died": "Death year cannot be earlier than birth year."})
        