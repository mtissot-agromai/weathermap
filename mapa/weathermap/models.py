from django.db import models

# Create your models here.

class Lookup(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    lookup_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lookup({self.latitude}, {self.longitude}, {self.start_date}, {self.end_date}, {self.lookup_time})"
    
    def get_latitude(self):
        return self.latitude
    
    def get_longitude(self):
        return self.longitude

    def get_start_date(self):
        return self.start_date
    
    def get_end_date(self):
        return self.end_date
    
    def get_lookup_time(self):
        return self.lookup_time

    def get_vals(self):
        return (self.get_latitude(), self.get_longitude(),
                self.get_start_date(), self.get_end_date(),
                self.get_lookup_time())
    
    def get_all(self):
        for item in Lookup.objects.all():
            print(item.get_vals())
        return None


