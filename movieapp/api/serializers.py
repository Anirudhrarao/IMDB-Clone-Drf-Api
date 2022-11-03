from rest_framework import serializers
from movieapp.models import WatchList, StreamPlatform, Reviews

class ReviewSerializer(serializers.ModelSerializer):
    reviews_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Reviews
        exclude = ('watchList',)


class WatchListserializer(serializers.ModelSerializer):
    # len_name = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True,read_only=True)
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = "__all__"

class StreamListserializer(serializers.ModelSerializer):
    watchlist = WatchListserializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = "__all__"
    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField()
    # about = serializers.CharField()
    # website = serializers.CharField()


    # def create(self, validated_data):
    #     return StreamPlatform.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name',instance.name)
    #     instance.about = validated_data.get('about',instance.about)
    #     instance.website = validated_data.get('website',instance.website)
    #     instance.save()
    #     return instance

       
