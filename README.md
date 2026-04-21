# Gattini Cafe - API REST

Backend REST per la gestione di un catalogo (categorie + prodotti) e di un sistema di ordini con autenticazione tramite JWT.  
Realizzato con Django e Django REST Framework.

---

## Panoramica

L’API permette:
- consultazione pubblica del catalogo
- autenticazione utenti tramite token JWT
- creazione e gestione ordini
- operazioni amministrative su prodotti e categorie

---

## Setup progetto

Clonare la repository:

```bash
git clone <url-del-repository>
cd gattini_cafe_project
```

Creare ambiente virtuale:

```bash
python -m venv venv
```

Attivare ambiente:

Linux / Mac:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

Installare dipendenze:

```bash
pip install -r requirements.txt
```

---

## Database

Il progetto utilizza SQLite con un database già pronto:

```text
gattini_cafe.db
```

Configurazione in settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'gattini_cafe.db',
    }
}
```

Allineare le migrazioni senza perdere i dati:

```bash
python manage.py makemigrations
python manage.py migrate --fake-initial
```

---

## Avvio server

```bash
python manage.py runserver
```

API disponibile su:

```text
http://127.0.0.1:8000/api/
```

---

## Autenticazione

L’accesso agli endpoint protetti avviene tramite JWT.

Login:
POST /api/auth/login/

Refresh token:
POST /api/auth/token/refresh/

Registrazione:
POST /api/auth/register/

Profilo utente autenticato:
GET /api/auth/me/

Header richiesto:

```http
Authorization: Bearer <access_token>
```

---

## Catalogo

### Categorie

Accesso pubblico:
GET /api/categorie/
GET /api/categorie/{id}/

Accesso admin:
POST /api/categorie/
PUT /api/categorie/{id}/
DELETE /api/categorie/{id}/

---

### Prodotti

Accesso pubblico:
GET /api/prodotti/
GET /api/prodotti/{id}/

Filtri disponibili:
- categoria
- disponibile
- search

Accesso admin:
POST /api/prodotti/
PUT /api/prodotti/{id}/
PATCH /api/prodotti/{id}/
DELETE /api/prodotti/{id}/

---

## Ordini

Accesso riservato a utenti autenticati.

Lista ordini:
GET /api/ordini/

- utente normale → vede solo i propri
- admin → vede tutti

Creazione ordine:
POST /api/ordini/

Dettaglio ordine:
GET /api/ordini/{id}/

Aggiornamento stato (admin):
PATCH /api/ordini/{id}/stato/

---

## Payload creazione ordine

```json
{
  "note": "Senza glutine",
  "prodotti": [
    { "prodotto_id": 1, "quantita": 2 },
    { "prodotto_id": 3, "quantita": 1 }
  ]
}
```

---

## Esempi richieste

Lista prodotti disponibili:

```bash
curl -X GET "http://127.0.0.1:8000/api/prodotti/?disponibile=true"
```

Login:

```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

Creazione ordine:

```bash
curl -X POST "http://127.0.0.1:8000/api/ordini/" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "note": "Senza lattosio",
    "prodotti": [
      {"prodotto_id": 1, "quantita": 2}
    ]
  }'
```

---

## Utente amministratore

Creazione superuser:

```bash
python manage.py createsuperuser
```

---

## Struttura progetto

- autenticazione utenti (JWT)
- gestione catalogo prodotti e categorie
- gestione ordini

Permessi:
- utenti: operazioni base e ordini personali
- admin: gestione completa sistema

---

## Client CLI

Client Python per test API.

Installazione dipendenze:

```bash
pip install requests
```

Avvio client (quando il server è attivo su un altro terminale):

```bash
cd client
python main.py
```
