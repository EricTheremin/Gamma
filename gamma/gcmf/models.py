from pipeline.models import *


class SupplyLine(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Corridor(models.Model):
    name = models.CharField(max_length=50)
    supply_line = models.ForeignKey(SupplyLine, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class CommodityInCorridor(models.Model):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    corridor = models.ForeignKey(Corridor, on_delete=models.CASCADE)
    is_gcmf_commodity = models.BooleanField()

    def __str__(self):
        return str(self.commodity) + " in " + str(self.corridor)

