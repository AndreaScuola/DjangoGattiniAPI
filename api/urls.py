from django.urls import path
from .views import (RegisterView, UserMeView, CategoriaListView, ProdottoListView, ProdottoCreateUpdateDeleteView,
                    OrdineListCreateView, OrdineUpdateStatoView, CategoriaDetailView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    #Autenticazione
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', UserMeView.as_view(), name='user_me'),

    #Menu (Pubblico e Gestione Admin)
    path('categorie/', CategoriaListView.as_view(), name='categoria_list'),
    path('categorie/<int:pk>/', CategoriaDetailView.as_view()),
    path('prodotti/', ProdottoListView.as_view(), name='prodotto_list'),
    path('prodotti/<int:pk>/', ProdottoCreateUpdateDeleteView.as_view(), name='prodotto_detail'),

    #Gestione prodotti per admin
    path('admin/prodotti/', ProdottoCreateUpdateDeleteView.as_view()),
    path('admin/prodotti/<int:pk>/', ProdottoCreateUpdateDeleteView.as_view()),

    #Ordini
    path('ordini/', OrdineListCreateView.as_view(), name='ordine_list_create'),
    path('ordini/<int:pk>/stato/', OrdineUpdateStatoView.as_view(), name='ordine_stato_update'),
]