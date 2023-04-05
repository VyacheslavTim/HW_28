from django.urls import path

from ads.views import JobListView, JobDetailView, JobCreateView, JobUpdateView, JobDeleteView, JobImageUpload

urlpatterns = [
    path('', JobListView.as_view()),
    path('<int:pk>/', JobDetailView.as_view()),
    path('create/', JobCreateView.as_view()),
    path('<int:pk>/update/', JobUpdateView.as_view()),
    path('<int:pk>/delete/', JobDeleteView.as_view()),
    path('<int:pk>/upload_image/', JobImageUpload.as_view())
]
