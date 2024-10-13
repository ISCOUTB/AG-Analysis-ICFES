from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from graphene_django.views import GraphQLView
from schema.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql", csrf_exempt(require_http_methods(
        ["POST", "OPTIONS", "GET"])(GraphQLView.as_view(graphiql=True, schema=schema)))),
    path('api/', include('saber.urls'))
]
