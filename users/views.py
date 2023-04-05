import json

from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from users.models import User, Location


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse({"id": user.pk,
                             "first_name": user.first_name,
                             "last_name": user.last_name,
                             "username": user.username,
                             "role": user.role,
                             "age": user.age,
                             "location": [loc.name for loc in user.location.all()]
                             }, safe=False)


class UserListView(ListView):
    model = User
    queryset = User.objects.annotate(total_ads=Count("job", filter=Q(job__is_published=True)))

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse([{"id": user.pk,
                              "first_name": user.first_name,
                              "last_name": user.last_name,
                              "username": user.username,
                              "role": user.role,
                              "age": user.age,
                              "total_ads": user.total_ads,
                              "location": [loc.name for loc in user.location.all()]
                              } for user in self.object_list], safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = "__all__"

    @csrf_exempt
    def post(self, request, **kwargs):
        ad_data = json.loads(request.body)

        user = User.objects.create(
            first_name=ad_data.get("first_name"),
            last_name=ad_data.get("last_name"),
            username=ad_data.get("username"),
            password=ad_data.get("password"),
            role=ad_data.get("role"),
            age=ad_data.get("age"),
        )

        locations = ad_data.get("locations")

        if locations:
            for loc_name in ad_data.get("locations"):
                loc, created = Location.objects.get_or_create(name=loc_name)
                user.location.add(loc)

        return JsonResponse({"id": user.pk,
                             "first_name": user.first_name,
                             "last_name": user.last_name,
                             "username": user.username,
                             "role": user.role,
                             "age": user.age,
                             "location": [loc.name for loc in user.location.all()]
                             }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        if "first_name" in ad_data:
            self.object.first_name = ad_data.get("first_name")
        if "last_name" in ad_data:
            self.object.last_name = ad_data.get("last_name")
        if "username" in ad_data:
            self.object.username = ad_data.get("username")
        if "age" in ad_data:
            self.object.age = ad_data.get("age")

        if "locations" in ad_data:
            self.object.location.all().delete()
            for loc_name in ad_data.get("locations"):
                loc, created = Location.objects.get_or_create(name=loc_name)
                self.object.location.add(loc)

        return JsonResponse({"id": self.object.pk,
                             "first_name": self.object.first_name,
                             "last_name": self.object.last_name,
                             "username": self.object.username,
                             "role": self.object.role,
                             "age": self.object.age,
                             "location": [loc.name for loc in self.object.location.all()]
                             }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user_id = user.id
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok", "id": user_id}, safe=False)
