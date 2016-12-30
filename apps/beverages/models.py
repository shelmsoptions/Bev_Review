from __future__ import unicode_literals
from ..login_and_registration.models import User
from django.db import models

class BeverageManager(models.Manager):
    def create_beverage(self, request):
        errors = []
        if request.POST['name'] == "":
            errors.append('Name cannot be empty')

        if request.POST['new_distiller_name'] == "" and request.POST['distiller_name'] == "":
            errors.append('You must either Enter or Select a Distiller Name')
            return (False, errors)
        if request.POST['distiller_name'] == "":
            distiller = Distiller.objects.create(name_distiller=request.POST['new_distiller_name'])
        else:
            # request.POST['new_distiller_name'] == "":
            distiller = Distiller.objects.get(id=request.POST['distiller_name'])
        if not errors:
            print 'No Errors!!'
            new_beverage = self.create(
                name=request.POST['name'],
                distiller=distiller,
            )
            return (True, new_beverage)
        else:
            return (False, errors)

    def delete_beverage(self, request, id):
        # print 'in model'
        # print 'self: ', self
        # print 'id: ', id
        Beverage.objects.get(id=id).delete()

class DistillerManager(models.Manager):
    def update_distiller(self, distiller_id, request):
        distiller = Distiller.objects.get(id=distiller_id)
        # print distiller
        distiller.name_distiller = request.POST['name_distiller']
        distiller.save()

    def delete_distiller(self, request, id):
        Distiller.objects.get(id=id).delete()

    def exclude_current_distiller(self, distiller_id):
        distiller_id = distiller_id.id
        other_distillers = Distiller.objects.values().exclude(id=distiller_id)
        return other_distillers


class ReviewManager(models.Manager):
    def create_review(self, request, new_id):
        beverage_reviewed = Beverage.objects.get(id=new_id)
        reviewer = User.objects.get(id=request.session['user']['user_id'])
        review = Review.objects.create(review_content=request.POST['review'], reviewer=reviewer, bev_reviewed=beverage_reviewed)


class Distiller(models.Model):
    name_distiller = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DistillerManager()

class Beverage(models.Model):
    name = models.CharField(max_length=70)
    distiller = models.ForeignKey(Distiller)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BeverageManager()

class Review(models.Model):
    reviewer = models.ForeignKey(User)
    review_content = models.CharField(max_length=500)
    bev_reviewed = models.ForeignKey(Beverage)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()
