from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProdottoSerializer, CategoriaSerializer, OrdineSerializer
from .models import Prodotto, Categoria, Ordine

#Registrazione nuovo utente
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] #Chiunque può registrarsi

#Endpoint /api/auth/me/
class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] #Solo se loggato

    def get_object(self):
        return self.request.user #Restituisce l'utente che sta facendo la richiesta


class CategoriaListView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]


class ProdottoListView(generics.ListAPIView):
    serializer_class = ProdottoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Prodotto.objects.all()
        #Filtro per categoria: ?categoria=1
        cat_id = self.request.query_params.get('categoria')
        if cat_id:
            queryset = queryset.filter(categoria_id=cat_id)

        #Filtro per disponibilità: ?disponibile=true
        disp = self.request.query_params.get('disponibile')
        if disp == 'true':
            queryset = queryset.filter(disponibile=1)

        return queryset


class ProdottoCreateUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    queryset = Prodotto.objects.all()
    serializer_class = ProdottoSerializer
    permission_classes = [permissions.IsAdminUser] #Solo Admin


class OrdineListCreateView(generics.ListCreateAPIView):
    serializer_class = OrdineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ordine.objects.all() #L'admin vede tutto
        return Ordine.objects.filter(utente=user) #L'utente vede solo i suoi

    def perform_create(self, serializer):
        #Collega l'ordine all'utente che sta scrivendo
        serializer.save(utente=self.request.user)

#Per cambiare lo stato (Solo Admin)
class OrdineUpdateStatoView(generics.UpdateAPIView):
    queryset = Ordine.objects.all()
    serializer_class = OrdineSerializer
    permission_classes = [permissions.IsAdminUser]