from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Party(models.Model):
    name = models.CharField(max_length=100, unique=True)
    symbol = models.ImageField(upload_to='party_symbols/', blank=True, null=True)
    Leader=models.CharField(max_length=200, null=True)
    about=models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class County(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    code = models.CharField(unique=True, blank=True, null=True)  # e.g. 001 for Mombasa
    population = models.CharField(blank=True, null=True)
    area_km2 = models.CharField(help_text="Area in square kilometers", blank=True, null=True)
    no_of_constituencies = models.IntegerField(default=0, blank=True, null=True)
    capital = models.CharField(max_length=100, blank=True, null=True)
    symbol = models.ImageField(upload_to='county_symbols/', blank=True, null=True)
    description = models.TextField(help_text="Brief info about the county", blank=True, null=True)
    current_gov = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.name

    def __str__(self):
        return self.name

class Constituency(models.Model):
    name = models.CharField(max_length=100)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name="constituencies")
    population = models.CharField(default=0, blank=True, null=True)
    area_km2 = models.CharField(default=0.0, blank=True, null=True)
    number_of_wards = models.IntegerField(default=0, blank=True, null=True)
    current_mp = models.CharField(max_length=100, blank=True)
    voter_turnout = models.FloatField(default=0.0, help_text="Latest election voter turnout in %", blank=True, null=True)
    development_index = models.FloatField(default=0.0, help_text="Out of 100" , blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    symbol = models.ImageField(upload_to="symbols/constituencies/", blank=True, null=True)

    class Meta:
        unique_together = ('name', 'county')

    def __str__(self):
        return f"{self.name} - {self.county.name}"


class Candidate(models.Model):
    POSITION_CHOICES = [
        ('president', 'President'),
        ('governor', 'Governor'),
        ('mp', 'Member of Parliament'),
    ]

    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='candidate_photos/', blank=True, null=True)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, blank=True, null=True)
    constituency = models.ForeignKey(Constituency, on_delete=models.SET_NULL, blank=True, null=True)
    bio=models.TextField(null=True, blank=True)
    manifesto=models.TextField(null=True, blank=True)
    achievements=models.TextField(null=True, blank=True)
    def clean(self):
        if self.position == 'president':
            if self.county or self.constituency:
                raise ValidationError("President should not be assigned county or constituency.")
        elif self.position == 'governor':
            if not self.county or self.constituency:
                raise ValidationError("Governor must have a county and no constituency.")
        elif self.position == 'mp':
            if not self.county or not self.constituency:
                raise ValidationError("MP must have both county and constituency.")

    def __str__(self):
        return f"{self.name} ({self.get_position_display()})"

class Development(models.Model):
    photo = models.ImageField(upload_to='candidate_gallery/', blank=True, null=True)
    caption=models.TextField(null=True, blank=True)
    def __str__(self):
        return f"image"

class Gallery(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, blank=True, null=True, related_name='gallery')
    photo = models.ImageField(upload_to='candidate_gallery/', blank=True, null=True)
    caption=models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.candidate.name}'s image"
