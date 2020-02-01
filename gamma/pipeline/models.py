from django.db import models


class Period(models.Model):
    date_start = models.DateField()

    def __str__(self):
        return str(self.date_start)


class RB(models.Model):
    name = models.CharField(max_length=3)

    def __str__(self):
        return self.name


class Country(models.Model):
    iso_code = models.CharField(max_length=2)
    co_code = models.CharField(max_length=4)
    name = models.CharField(max_length=50)
    rb = models.ForeignKey(RB, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class WBSElement(models.Model):
    code = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.code


class Commodity(models.Model):
    name = models.CharField(max_length=50)
    planning_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PipelineElement(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    wbs = models.ForeignKey(WBSElement, on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)

    implementation_reqs_mt = models.FloatField()
    implementation_shortfalls_mt = models.FloatField()
    implementation_resourced_mt = models.FloatField()
    implementation_reqs_fcr = models.FloatField()
    implementation_shortfalls_fcr = models.FloatField()
    implementation_resourced_fcr = models.FloatField()

    def __str__(self):
        return str(self.country) + " " + str(self.wbs) + " " + str(self.commodity) + " " + str(self.period)

