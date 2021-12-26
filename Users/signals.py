from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


'''
The sender is user while the receiver is profile
The receiver decorator gets what type of signal to receive and from whom(sender)
The build_profile function checks if our signal is true( if created == True) and then does a task which is to create a profile for that user
The save_profile simply saves our profile. Observe that the created parameter is absent

Last task is to go under apps.py module under Usersconfig class and add a function to import signals module:
    def ready(self):
        import Users.signals 
'''



@receiver(post_save, sender=User)
def build_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(post_save, sender=User)       
def save_profile(sender, instance, **kwargs):
    instance.profile.save()