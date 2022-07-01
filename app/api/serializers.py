from rest_framework import serializers

from .models import Bill, Client


class FileSerializers(serializers.Serializer):
    client_org = serializers.FileField()
    bills = serializers.FileField()


class ClientSerializer(serializers.ModelSerializer):
    org_count = serializers.IntegerField()
    sum_bills = serializers.IntegerField()

    class Meta:
        model = Client
        fields = "__all__"


class BillSerialiser(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field="name", read_only=True)
    service = serializers.SlugRelatedField(slug_field="name", read_only=True)
    organisation = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Bill
        fields = "__all__"
