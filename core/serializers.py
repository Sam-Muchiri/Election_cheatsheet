from rest_framework import serializers
from .models import Party, County, Constituency, Candidate


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

class CandidateSerializer(serializers.ModelSerializer):
    party = PartySerializer(read_only=True)
    county = CountySerializer(read_only=True)
    constituency = ConstituencySerializer(read_only=True)
    
    class Meta:
        model = Candidate
        fields = '__all__'
