
from django.urls import path, include
from django.urls import path


urlpatterns = [
    path("account/", include("app.account.v1.urls"), name="account"),
    

    
]

