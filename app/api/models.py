from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=250)
    organisation = models.ManyToManyField(
        Client, through="Bill", related_name="organisation"
    )

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Bill(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="bill")
    organisation = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="bill"
    )
    number = models.IntegerField()
    sum = models.FloatField()
    date = models.DateField()
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    fraud_score = models.FloatField()

    class Meta:
        unique_together = ["organisation", "number"]
