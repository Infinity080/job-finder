from django.urls import path
from .views import websites_list,JobLinkView,SpecsView, UploadCVView, SpecsView

urlpatterns = [
    path('websites/', websites_list, name='websites_list'),
    path('api/jobs/', JobLinkView.as_view(), name='job-link'),
    path('api/specs/', SpecsView.as_view(), name='specs-list'),
    path('api/upload-cv/', UploadCVView.as_view(), name='upload_cv')
]