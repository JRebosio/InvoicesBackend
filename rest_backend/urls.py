from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, InvoiceViewSet, ProviderViewSet

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .authentication import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutView,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"invoices", InvoiceViewSet)
router.register(r"providers", ProviderViewSet)

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", include(router.urls)),
]
