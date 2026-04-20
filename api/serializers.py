from rest_framework import serializers
from .models import Categoria, Prodotto, Ordine, OrdineProdotto
from django.contrib.auth.models import User

#Per visualizzare le categorie
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

#Per visualizzare i prodotti
class ProdottoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.ReadOnlyField(source='categoria.nome')

    class Meta:
        model = Prodotto
        fields = ['id', 'nome', 'descrizione', 'prezzo', 'disponibile', 'immagine_url', 'categoria', 'categoria_nome']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}} #La password non viene mai inviata indietro per sicurezza

    def create(self, validated_data):
        #Questo serve per criptare la password quando si crea l'utente
        user = User.objects.create_user(**validated_data)
        return user


class OrdineProdottoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdineProdotto
        fields = ['prodotto', 'quantita']


class OrdineSerializer(serializers.ModelSerializer):
    #Includiamo i dettagli dei prodotti annidati
    prodotti = OrdineProdottoSerializer(many=True, source='ordineprodotto_set')
    utente = serializers.ReadOnlyField(source='utente.username')

    class Meta:
        model = Ordine
        fields = ['id', 'utente', 'data_ordine', 'stato', 'totale', 'note', 'prodotti']
        read_only_fields = ['totale', 'stato']

    def create(self, validated_data):
        #Logica per salvare l'ordine e calcolare il totale
        prodotti_data = validated_data.pop('ordineprodotto_set')
        ordine = Ordine.objects.create(**validated_data)
        totale_ordine = 0

        for p_data in prodotti_data:
            prodotto = p_data['prodotto']
            quantita = p_data['quantita']
            #Calcolo il totale parziale
            totale_ordine += prodotto.prezzo * quantita
            #Salvo nella tabella ponte
            OrdineProdotto.objects.create(ordine=ordine, prodotto=prodotto, quantita=quantita)

        ordine.totale = totale_ordine
        ordine.save()
        return ordine