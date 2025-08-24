from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from.serializers import PartySerializer, CountySerializer, ConstituencySerializer, CandidateSerializer
from .models import Party, County, Constituency, Candidate  

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

class CandidateDetail(RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer  
