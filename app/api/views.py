import pandas as pd
from django.db import IntegrityError
from django.db.models import Count, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Bill, Client, Organization, Service
from .serializers import BillSerialiser, ClientSerializer, FileSerializers
from .services import fraud_detector, get_objects, service_classification


class FileUploadView(APIView):
    """Загрузка файлов в БД"""
    parser_classes = (MultiPartParser,)
    serializer_class = FileSerializers

    def put(self, request):
        
        try:  
            client_org_file = request.FILES["client_org"]
            bills_file = request.FILES["bills"]
            xls = pd.ExcelFile(client_org_file)
            clients_df = pd.read_excel(xls, "client")
            organisations_df = pd.read_excel(xls, "organization")
            bills = pd.read_excel(bills_file)
        except Exception as e:
            return Response({"Неверно загружены файлы, или неверный формат файлов"},status=400)


        for client in clients_df["name"]:
            client_data = Client(name=client)
            try:
                client_data.save()
            except IntegrityError:
                print("Уже есть запись")

        for i, organisation in organisations_df.iterrows():
            organisation_data = Organization(
                name=organisation["name"], address=organisation["address"]
            )
            try:
                organisation_data.save()
            except IntegrityError:
                print("Уже есть запись")

        clients = Client.objects.filter(name__in=pd.unique(bills["client_name"]))

        organisations = Organization.objects.filter(
            name__in=pd.unique(bills["client_org"])
        )
        services = Service.objects.all()

        for _, bill in bills.iterrows():

            bill_data = Bill(
                client=get_objects(clients, bill["client_name"]),
                organisation=get_objects(organisations, bill["client_org"]),
                number=bill["№"],
                sum=bill["sum"],
                date=bill["date"],
                service=get_objects(services, service_classification(bill["service"])),
                fraud_score=fraud_detector(bill["service"]),
            )
            try:
                bill_data.save()
            except IntegrityError:
                print("Уже есть запись")

        return Response({"Файлы загружены"},status=200)


class ClientViews(ListAPIView):
    """Список всех клиентов"""
    serializer_class = ClientSerializer
    queryset = Client.objects.annotate(
        sum_bills=Sum("bill__sum", default=0),
        org_count=Count("organisation", distinct=True),
    ).all()


class BillViews(ListAPIView):
    """Список всех считов"""
    serializer_class = BillSerialiser
    queryset = Bill.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("client", "organisation")
