from rest_framework import serializers
from .models import Party, County, Constituency, Candidate, Evidence, CandidateScore


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'  

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'  
        
class ConstituencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Constituency
        fields = '__all__'  

# --- Evidence Serializer ---
class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = ['id', 'evidence_type', 'description', 'source', 'date_reported', 'verified']


# --- Candidate Score Serializer ---
class CandidateScoreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='candidate.name')
    party = serializers.CharField(source='candidate.party')
    score = serializers.FloatField(source='overall_score')
    class Meta:
        model = CandidateScore
        fields = ['id', 'track_record', 'manifesto_relevance', 'integrity', 'education_experience', 'name', 'party', 'score']


class CandidateSerializer(serializers.ModelSerializer):
    party = PartySerializer(read_only=True)
    county = CountySerializer(read_only=True)
    constituency = ConstituencySerializer(read_only=True)
    evidences = EvidenceSerializer(many=True, read_only=True)
    score = CandidateScoreSerializer(read_only=True)

    class Meta:
        model = Candidate
        fields = [
            'id', 'name', 'photo', 'position', 'party', 'county', 'constituency',
            'bio', 'manifesto', 'achievements', 'is_incumbent', 'evidences', 'score'
        ]