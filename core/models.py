from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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
    is_incumbent = models.BooleanField(default=False)
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

# --- Evidence model ---
class Evidence(models.Model):
    EVIDENCE_TYPE_CHOICES = [
        ('corruption_case', 'Corruption Case'),
        ('legal_case', 'Legal Case'),
        ('achievement', 'Achievement'),
        ('manifesto_point', 'Manifesto Point'),
        ('community_engagement', 'Community Engagement'),
    ]

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="evidences")
    evidence_type = models.CharField(max_length=50, choices=EVIDENCE_TYPE_CHOICES)
    description = models.TextField(help_text="Describe the evidence or source")
    source = models.URLField(blank=True, null=True, help_text="Link to news article, official report, or document")
    date_reported = models.DateField(blank=True, null=True)
    verified = models.BooleanField(default=False, help_text="Mark True if the source is verified and trustworthy")

    def __str__(self):
        return f"{self.candidate.name} - {self.get_evidence_type_display()}"


# --- CandidateScore model ---
class CandidateScore(models.Model):
    candidate = models.OneToOneField("Candidate", on_delete=models.CASCADE, related_name="score")

    # Scores are automatically calculated based on evidence
    track_record = models.FloatField(default=0.0)
    manifesto_relevance = models.FloatField(default=0.0)
    integrity = models.FloatField(default=0.0)
    education_experience = models.FloatField(default=0.0)

    overall_score = models.FloatField(default=0.0)

    # Weighting configuration
    TRACK_RECORD_WEIGHT = 0.4
    EDUCATION_WEIGHT = 0.2
    MANIFESTO_WEIGHT = 0.2
    INTEGRITY_WEIGHT = 0.2

    def calculate_scores(self):
        evidences = self.candidate.evidences.filter(verified=True)

        # --- Track record score ---
        achievements_count = evidences.filter(evidence_type='achievement').count()
        community_count = evidences.filter(evidence_type='community_engagement').count()
        self.track_record = min((achievements_count + community_count) * 10, 100)

        # --- Manifesto relevance ---
        manifesto_points = evidences.filter(evidence_type='manifesto_point').count()
        self.manifesto_relevance = min(manifesto_points * 20, 100)

        # --- Integrity score ---
        corruption_count = evidences.filter(evidence_type='corruption_case').count()
        legal_count = evidences.filter(evidence_type='legal_case').count()
        self.integrity = max(100 - (corruption_count + legal_count) * 25, 0)

        # --- Education & experience ---
        self.education_experience = 50  # placeholder or can be extended

        # --- Overall score ---
        self.overall_score = (
            self.track_record * self.TRACK_RECORD_WEIGHT +
            self.education_experience * self.EDUCATION_WEIGHT +
            self.manifesto_relevance * self.MANIFESTO_WEIGHT +
            self.integrity * self.INTEGRITY_WEIGHT
        )

        self.save()

    def __str__(self):
        return f"{self.candidate.name} Score: {self.overall_score:.2f}"


# --- Signals to auto-update scores when Evidence changes ---
@receiver(post_save, sender="core.Evidence")
@receiver(post_delete, sender="core.Evidence")
def update_candidate_score(sender, instance, **kwargs):
    candidate = instance.candidate
    score, created = CandidateScore.objects.get_or_create(candidate=candidate)
    score.calculate_scores()