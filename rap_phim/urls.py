from django.urls import path
from . import views

urlpatterns = [
    path('', views.trang_chu, name='trang_chu'),
    path('dat-ve/<str:ma_suat>/', views.chon_ghe, name='chon_ghe'),
    path('chon-bap-nuoc/', views.chon_bap_nuoc, name='chon_bap_nuoc'),
    path('chon-uu-dai/', views.chon_uu_dai, name='chon_uu_dai'),
    path('lich-su-ve/', views.lich_su_ve, name='lich_su_ve'),
    path('admin-quan-ly/', views.admin_quan_ly, name='admin_quan_ly'),
    path('dang-nhap/', views.dang_nhap, name='dang_nhap'),
    path('dang-ky/', views.dang_ky, name='dang_ky'),
    path('dang-xuat/', views.dang_xuat, name='dang_xuat'),
]