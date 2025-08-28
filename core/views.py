from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from.serializers import PartySerializer, CountySerializer, ConstituencySerializer, CandidateSerializer,CandidateScoreSerializer
from .models import Party, County, Constituency, Candidate, CandidateScore 

# Create your views here.

class PartyList(ListCreateAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer  

class PartyDetail(RetrieveUpdateDestroyAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer      

class CountyList(ListCreateAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer  

class CountyDetail(RetrieveUpdateDestroyAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer      

class ConstituenciesByCounty(ListAPIView):
    serializer_class = ConstituencySerializer

    def get_queryset(self):
        county_id = self.kwargs['id'] 
        return Constituency.objects.filter(county__id=county_id)

class ConstituencyDetail(RetrieveUpdateDestroyAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer    

class ConstituencyList(ListAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer

class CandidateList(ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer  

class PresidentListView(ListAPIView):
    serializer_class = CandidateSerializer

    def get_queryset(self):
        return Candidate.objects.filter(position__iexact="President")

class CandidateDetail(RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer  

class CountyGovernorScoresView(ListAPIView):
    serializer_class = CandidateScoreSerializer

    def get_queryset(self):
        county_id = self.kwargs['pk']
        # Filter candidate scores where candidate is in this county and position is governor
        return CandidateScore.objects.filter(
            candidate__county_id=county_id,
            candidate__position='governor'
        )
    
class ConstituencyMPScoresView(ListAPIView):
    serializer_class = CandidateScoreSerializer

    def get_queryset(self):
        constituency_id = self.kwargs['pk']
        # Filter candidate scores where candidate is in this constituency and position is MP
        return CandidateScore.objects.filter(
            candidate__constituency_id=constituency_id,
            candidate__position='mp'
        ).order_by('-overall_score')