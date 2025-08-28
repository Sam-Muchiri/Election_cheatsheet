from django.urls import path
from . import views

urlpatterns = [
    path('parties/', views.PartyList.as_view(), name='party-list'),
    path('party/<int:pk>/', views.PartyDetail.as_view(), name='party-detail'),
    path('counties/', views.CountyList.as_view(), name='county-list'),
    path('counties/<int:pk>/', views.CountyDetail.as_view(), name='county-detail'),
    path('counties/<int:pk>/candidates/governor/', views.CountyGovernorScoresView.as_view(), name='county-governors-scores'),
    # urls.py
    path('counties/<int:id>/constituencies/', views.ConstituenciesByCounty.as_view(), name='county-constituencies'),
    path('constituencies/<int:pk>/', views.ConstituencyDetail.as_view(), name='constituency-detail'),
    # urls.py
    path('constituencies/', views.ConstituencyList.as_view(), name='constituency-list'),
    # urls.py
    path('constituencies/<int:pk>/candidates/mp/', views.ConstituencyMPScoresView.as_view(), name='constituency-mp-scores'),
    path("candidates/presidents/", views.PresidentListView.as_view(), name="president-list"),
    path('candidates/', views.CandidateList.as_view(), name='candidate-list'),
    path('candidate/<int:pk>/', views.CandidateDetail.as_view(), name='candidate-detail'), 
]
