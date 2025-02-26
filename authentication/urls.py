from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from authentication.views import RegisterAPIView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(parser_classes=[MultiPartParser, JSONParser]),name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('driver/register', RegisterAPIView.as_view(), name='token_refresh'),

]
