from django.db import models

class Product(models.Model):
	name = models.CharField(max_length = 30)
	producer = models.CharField(max_length = 30)
	class Meta:
		unique_together = ('name', 'producer')

class Order(models.Model):
	user = models.CharField(max_length = 50)
	product_name = models.CharField(max_length=30)
	producer_name = models.CharField(max_length=30)
	quantity = models.IntegerField()
	delivery_address = models.CharField(max_length=200)

class Information(models.Model):
	order_id = models.IntegerField()
	order_state = models.CharField(max_length=200)
	time_stamp = models.FloatField()
	location = models.CharField(max_length=50, default='')
	start_location = models.CharField(max_length=50, default='')
	end_location = models.CharField(max_length=50, default='')
	delivery_method = models.CharField(max_length=50, default='')
	shipping_company = models.CharField(max_length=30, default='')
	temperature = models.FloatField(default=-1)
	quality_rating = models.FloatField(default=-1)
	quality_note = models.CharField(max_length=250, default='')
	qa_company = models.CharField(max_length=100, default='')

	previous_hash = models.CharField(max_length=100, default='')
	hash = models.CharField(max_length=100)
	previous_block_loc = models.IntegerField(default=-1)
	block_loc = models.IntegerField()
	hashed_text = models.CharField(max_length=2000)

	user = models.CharField(max_length = 50, default='')
	product_name = models.CharField(max_length=30, default='')
	producer_name = models.CharField(max_length=30, default='')
	quantity = models.IntegerField(default=-1)
	delivery_address = models.CharField(max_length=200, default='')



# class OrderForm(ModelForm):
#     class Meta:
#         model = Order
#         fields = ['product_name', 'product_producer', 'quantity', 'address']
