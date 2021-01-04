from rest_framework import serializers

class count_serializers(serializers.Serializer):
    url         = serializers.URLField(max_length=100)
    is_complete = serializers.BooleanField(default=False)
    count_js    = serializers.IntegerField()
    count_image = serializers.IntegerField()
    count_css   = serializers.IntegerField()