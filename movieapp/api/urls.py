from django.urls import path,include
from movieapp.api.views import UserReview, ReviewCreateAV, ReviewDetailsAV, StreamListAV, WatchListAV, WatchDetialsAV, StreamList, StreamDetails,ReviewListAV
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('stream',StreamListAV,basename='streamplatform')

urlpatterns = [
    path('',WatchListAV.as_view(),name='movie'),
    path('<int:movie_id>/',WatchDetialsAV.as_view(),name='movie-detail'),
    path('',include(router.urls)),
    # path('stream/',StreamList.as_view(),name='streamlist'),
    # path('streamdetails/<int:stream_id>/',StreamDetails.as_view(),name='stream-details'),
    path('<int:pk>/review-create',ReviewCreateAV.as_view(),name='review-create'),
    path('<int:pk>/reviews',ReviewListAV.as_view(),name='review'),
    path('review/<int:pk>',ReviewDetailsAV.as_view(),name='review-detials'),
    path('reviews/<str:username>/',UserReview.as_view(),name='user-review'),
]
