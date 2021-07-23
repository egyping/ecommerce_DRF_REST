from django.db import models


from project import settings
from django.db.models.signals import pre_save, post_save
import braintree
from django.contrib.auth import get_user_model

User = get_user_model()

if settings.DEBUG:
        braintree.Configuration.configure(braintree.Environment.Sandbox,
      merchant_id=settings.BRAINTREE_MERCHANT_ID,
      public_key=settings.BRAINTREE_PUBLIC,
      private_key=settings.BRAINTREE_PRIVATE)


class UserCheckout(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) #not required
    email = models.EmailField(unique=True) #--> required
    braintree_id = models.CharField(max_length=120, null=True, blank=True)

    def __unicode__(self): #def __str__(self):
        return self.email

    @property
    def get_braintree_id(self,):
        instance = self
        if not instance.braintree_id:
            result = braintree.Customer.create({
                "email": instance.email,
            })
            if result.is_success:
                instance.braintree_id = result.customer.id
                instance.save()
        return instance.braintree_id

    def get_client_token(self):
        customer_id = self.get_braintree_id
        if customer_id:
            client_token = braintree.ClientToken.generate({
                "customer_id": customer_id
            })
            return client_token
        return None

def update_braintree_id(sender, instance, *args, **kwargs):
    	if not instance.braintree_id:
            instance.get_braintree_id


post_save.connect(update_braintree_id, sender=UserCheckout)
