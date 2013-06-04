from django.db import models
from django.db.models import Q

import datetime

class ProductManager(models.Model):
    """ Manager for the :class:`Product` model """
    def send_product(self,sender,to_user,amount):
	""" send the product to a user"""
        pass 
	
