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
        distiller.distiller_details = request.POST['distiller_details']
        distiller.save()

    def delete_distiller(self, request, id):
        Distiller.objects.get(id=id).delete()

    def exclude_current_distiller(self, distiller_id):
        distiller_id = distiller_id.id
        other_distillers = Distiller.objects.values().exclude(id=distiller_id)
        return other_distillers

# class TryManager(models.Manager):
#     def create_try(self, beverage_id, user_id):
#         pass

class ReviewManager(models.Manager):
    def create_review(self, request, new_id):
        beverage_reviewed = Beverage.objects.get(id=new_id)
        reviewer = User.objects.get(id=request.session['user']['user_id'])
        review = Review.objects.create(review_content=request.POST['review'], reviewer=reviewer, bev_reviewed=beverage_reviewed)


class FavorPointManager(models.Manager):
    def create_favor(request, user_id, beverage_id):
        exists = FavorPoint.objects.filter(favor_user=user_id, favor_beverage=beverage_id)
        # , favor_point=request.POST['favor_point']+1
        if exists:
            print 'exists: ', exists
        else:
            # VV  check the use of '_id' appended to favor_user and favor_beverage...  VV
            FavorPoint.objects.create(favor_user_id=user_id, favor_beverage=beverage_id)


class Distiller(models.Model):
    name_distiller = models.CharField(max_length=70)
    distiller_details = models.TextField(max_length=1000, default='details go here')
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

class FavorPoint(models.Model):
    favor_user = models.ForeignKey(User, related_name='favor_user')
    favor_beverage = models.ForeignKey(Beverage, related_name='favor_beverage')
    favor_point = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FavorPointManager()

# class Try(models.Model):
#     tried = models.BooleanField()
#     try_beverage = models.ForeignKey(Beverage)
#     try_user = models.ForeignKey(User)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     object = TryManager()