# Gattini Cafe - API REST

API REST per la gestione di categorie, prodotti, utenti autenticati e ordini, sviluppata con **Django REST Framework** e autenticazione **JWT** tramite Simple JWT.

---

## Funzionalità

- Registrazione utente  
- Login JWT con access e refresh token  
- Endpoint protetto `/api/auth/me/`  
- Liste pubbliche di prodotti e categorie  
- Filtri su prodotti:  
  - `categoria`  
  - `disponibile`  
  - `search`  
- CRUD protetto per prodotti e categorie (admin)  
- Creazione e gestione ordini per utenti autenticati  
- Calcolo automatico del totale ordine  
- Visibilità ordini:  
  - utente → solo i propri  
  - admin → tutti  
- Aggiornamento stato ordine solo per admin  
- Database preconfigurato con dati di esempio  

---

## Tecnologie

- Python  
- Django  
- Django REST Framework  
- Simple JWT  
- SQLite  

---

## Installazione

Clonare il repository e configurare l’ambiente:

```bash
git clone <url-del-repository>
cd gattini_cafe_project
python -m venv venv
```

---

## 🗄️ Database

Il progetto utilizza il database SQLite fornito:

```
gattini_cafe.db
```

Configurazione in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'gattini_cafe.db',
    }
}
```

Eseguire le migrazioni senza perdere i dati:

```bash
python manage.py makemigrations
python manage.py migrate --fake-initial
```

---

## Avvio del server

```bash
python manage.py runserver
```

API disponibile su:

```
http://127.0.0.1:8000/api/
```

---

## 🔐 Autenticazione JWT

L’autenticazione avviene tramite token JWT.

Login  
`POST /api/auth/login/`  

Restituisce:  
- access  
- refresh  

Refresh token  
`POST /api/auth/token/refresh/`  

Registrazione  
`POST /api/auth/register/`  

Dati utente autenticato  
`GET /api/auth/me/`  

Header richiesto:

```http
Authorization: Bearer <access_token>
```

---

## Endpoints disponibili

### Prodotti

Pubblici  
- `GET /api/prodotti/`  
  Lista prodotti con filtri: categoria, disponibile, search  
- `GET /api/prodotti/{id}/`  
  Dettaglio prodotto  

Protetti JWT + admin  
- `POST /api/prodotti/`  
- `PUT /api/prodotti/{id}/`  
- `PATCH /api/prodotti/{id}/`  
- `DELETE /api/prodotti/{id}/`  

---

### Categorie

Pubbliche  
- `GET /api/categorie/`  
- `GET /api/categorie/{id}/`  

Protette JWT + admin  
- `POST /api/categorie/`  
- `PUT /api/categorie/{id}/`  
- `DELETE /api/categorie/{id}/`  

---

### Ordini

Protetti JWT  
- `GET /api/ordini/`  
  - utente → solo i propri  
  - admin → tutti  
- `POST /api/ordini/`  
- `GET /api/ordini/{id}/`  

Protetto JWT + admin  
- `PATCH /api/ordini/{id}/stato/`  

### Payload creazione ordine

```json
{
  "note": "Senza glutine!",
  "prodotti": [
    { "prodotto_id": 1, "quantita": 2 },
    { "prodotto_id": 3, "quantita": 1 }
  ]
}
```

Il totale viene calcolato automaticamente dal server.

---

## Utente Admin

Le password degli utenti di test sono state resettate.  

Creare un nuovo admin con:

```bash
python manage.py createsuperuser
```

---

## Esempi di chiamate API

Lista prodotti disponibili

```bash
curl -X GET "http://127.0.0.1:8000/api/prodotti/?disponibile=true"
```

Login

```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Creazione ordine

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
