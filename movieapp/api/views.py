from asyncio import streams
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from movieapp.api.serializers import WatchListserializer,StreamListserializer, ReviewSerializer
from rest_framework.views import APIView
from rest_framework import status
from movieapp.models import WatchList,StreamPlatform,Reviews
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from movieapp.api.permission import AdminOrReadOnly, ReviewUserReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from movieapp.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from movieapp.api.paginations import WatchListPagination
class WatchListAV(APIView):
    # permission_classes = [IsAuthenticated]
    pagination_class = WatchListPagination
    def get(self,request):
        movie = WatchList.objects.all()
        serializer = WatchListserializer(movie,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = WatchListserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchDetialsAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request,movie_id):
        try:
            movie = WatchList.objects.get(pk=movie_id)
        except WatchList.DoesNotExist:
            return Response({'Error':'Movie not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListserializer(movie)
        return Response(serializer.data)
    
    def put(self,request,movie_id):
        movie = WatchList.objects.get(pk=movie_id)
        serializer = WatchListserializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_404_BAD_REQUEST)

        
    def delete(self,request,movie_id):
        movie = WatchList.objects.get(pk=movie_id)
        movie.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)


class StreamListAV(viewsets.ModelViewSet):
    serializer_class = StreamListserializer
    queryset = StreamPlatform.objects.all()
    permission_classes = [AdminOrReadOnly]
# class StreamListAV(viewsets.ViewSet):
#     def list(self,request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamListserializer(queryset,many=True)
#         return Response(serializer.data)

#     def retrieve(self,request,pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset,pk=pk)
#         serializer = StreamListserializer(watchlist)
#         return Response(serializer.data)

#     def create(self,request):
#         serializer = StreamListserializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    


class StreamList(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request):
        stream = StreamPlatform.objects.all()
        serializer = StreamListserializer(stream,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = StreamListserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamDetails(APIView):
    
    def get(self,request,stream_id):
        stream = StreamPlatform.objects.get(pk=stream_id)
        serialzer = StreamListserializer(stream)
        return Response(serialzer.data)
    
    def put(self,request,stream_id):
        stream = StreamPlatform.objects.get(pk=stream_id)
        serializer = StreamListserializer(stream,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_404_BAD_REQUEST)
        
    def delete(self,request,stream_id):
        stream = StreamPlatform.objects.get(pk=stream_id)
        stream.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)

class ReviewCreateAV(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Reviews.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Reviews.objects.filter(watchList=movie,reviews_user=review_user)
        if review_queryset.exists():
            raise ValidationError("you already reviewed this watchlist")
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2
        movie.number_rating = movie.number_rating + 1
        movie.save() 
        serializer.save(watchList=movie,reviews_user=review_user)
        

class ReviewListAV(generics.ListAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reviews_user__username','active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Reviews.objects.filter(watchList=pk)

class ReviewDetailsAV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserReadOnly]
    # throttle_classes = [UserRateThrottle,AnonRateThrottle]
    throttle_classes = [ReviewCreateThrottle]
    

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Reviews.objects.filter(reviews_user__username=username)     

    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Reviews.objects.filter(reviews_user__username=username)