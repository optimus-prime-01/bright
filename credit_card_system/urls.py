from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from credit_api import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/apply-loan/', views.apply_loan),
    path('api/make-payment/', views.make_payment),
    path('api/get-statement/<uuid:loan_id>/', views.get_statement),
]
