from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    #Django di default crea un campo 'id'. Se nel DB è 'id', non serve dichiararlo,
    nome = models.CharField(max_length=255)
    descrizione = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categoria'  #Forza Django a usare il nome tabella

    def __str__(self):      #Specifico l'output da dare se si chiama la stampa
        return self.nome


class Prodotto(models.Model):
    nome = models.CharField(max_length=255)
    descrizione = models.TextField(blank=True, null=True)
    prezzo = models.FloatField()  # Usiamo FloatField come richiesto
    disponibile = models.IntegerField(default=1)  # 1 = Disponibile, 0 = Esaurito
    immagine_url = models.URLField(max_length=500, blank=True, null=True)

    #Relazione con Categoria (Foreign Key)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='prodotti')

    class Meta:
        db_table = 'prodotto'

    def __str__(self):
        return self.nome


class Ordine(models.Model):
    STATI_ORDINE = [
        ('in_attesa', 'In Attesa'),
        ('in_preparazione', 'In Preparazione'),
        ('completato', 'Completato'),
        ('annullato', 'Annullato'),
    ]

    #FK verso auth_user
    utente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordini')
    data_ordine = models.DateTimeField(auto_now_add=True)
    stato = models.CharField(max_length=20, choices=STATI_ORDINE, default='in_attesa')
    totale = models.FloatField(default=0.0)
    note = models.TextField(blank=True, null=True)

    #Relazione Many-to-Many con Prodotto tramite la tabella ponte
    prodotti = models.ManyToManyField(Prodotto, through='OrdineProdotto')

    class Meta:
        db_table = 'ordine'

    def __str__(self):
        return f"Ordine {self.id} - {self.utente.username}"


class OrdineProdotto(models.Model):
    ordine = models.ForeignKey(Ordine, on_delete=models.CASCADE)
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE)
    quantita = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'ordine_prodotto'