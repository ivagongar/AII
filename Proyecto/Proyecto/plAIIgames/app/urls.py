from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('populateSwitch', views.populateSwitch, name='populateSwitch'),
    path('listAll', views.mostrarJuegos, name='listAll'),
    

#     path('voters/', views.listVoters, name='census_voters'),
#     path('voting/', views.selectVoting, name="select_voting"),
# 
#     path('census/', views.selectVotingReuse, name="select_voting_reuse"),
#     path('reuse/', views.reuseCensus, name="reuse_census"),
# 
#     path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
# 
#     path('create', views.create, name='create'),
#     path('create2', views.create2, name='create2'),
# 
#     path('exportcsv', views.ExportAsCSV, name='exportcsv'),
#     path('exportjson', views.ExportAsJSON, name='exportjson'),
#     path('exportexcel', views.ExportAsExcel, name='exportexcel'),
#     
#     path('import', views.ImportAs.as_view(), name = 'import'),
#     path('importcsv', views.ImportAsCSV, name='importcsv'),
#     path('importjson', views.ImportAsJSON, name='importjson'),

    
    
    

]


