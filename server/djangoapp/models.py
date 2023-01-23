from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=256, default='unknown')
    description = models.CharField(null=False, max_length=256, default='no description')

    def __str__(self):
        return self.name + " / " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    TYPE_CHOICES = [
        ('SE', 'Sedan'),
        ('SU', 'SUV'),
        ('WA', 'WAGON')
    ]

    name = models.CharField(null=False, max_length=256, default='unknown')
    dealerId = models.IntegerField(null=True)
    type = models.CharField(null=True, max_length=2, choices=TYPE_CHOICES, default='SE')
    year = models.DateField(null=True)
    carMake = models.ForeignKey(CarMake, on_delete=models.CASCADE)


    def __str__(self):
        return self.name + " / " + str(self.dealerId) + " / "+ self.type + " / " + str(self.year)


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
