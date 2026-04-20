import requests

BASE_URL = "http://127.0.0.1:8000/api"
tokens = {}


def login():
    print("\n--- LOGIN GATTINI CAFE ---")
    username = input("Username: ")
    password = input("Password: ")

    response = requests.post(f"{BASE_URL}/auth/login/", json={
        "username": username,
        "password": password
    })

    if response.status_code == 200:
        global tokens
        tokens = response.json()
        print("Login effettuato con successo!")
    else:
        print("Credenziali errate.")


def visualizza_menu():
    print("\n--- MENU DEL GIORNO ---")
    response = requests.get(f"{BASE_URL}/prodotti/")
    if response.status_code == 200:
        prodotti = response.json()
        for p in prodotti:
            disp = "Disponibile" if p['disponibile'] else "Esaurito"
            print(f"[{p['id']}] {p['nome']} - €{p['prezzo']} ({disp})")
    else:
        print("Errore nel recupero del menu.")


def crea_ordine():
    if not tokens.get('access'):
        print("Devi prima effettuare il login!")
        return

    visualizza_menu()
    print("\n--- CREA NUOVO ORDINE ---")
    try:
        p_id = int(input("Inserisci l'ID del prodotto: "))
        quant = int(input("Quantità: "))
        note = input("Note (es. senza lattosio): ")

        # Header con il Token JWT
        headers = {"Authorization": f"Bearer {tokens['access']}"}

        payload = {
            "note": note,
            "prodotti": [{"prodotto": p_id, "quantita": quant}]
        }

        response = requests.post(f"{BASE_URL}/ordini/", json=payload, headers=headers)

        if response.status_code == 201:
            ordine = response.json()
            print(f"Ordine creato! Totale: €{ordine['totale']}")
        else:
            print(f"Errore: {response.json()}")
    except ValueError:
        print("Inserisci numeri validi per ID e quantità.")


def main():
    while True:
        print("\n=== GATTINI CAFE CLI CLIENT ===")
        print("1. Login")
        print("2. Visualizza Menu")
        print("3. Crea Ordine")
        print("4. Esci")
        scelta = input("Scegli un'opzione: ")

        if scelta == '1':
            login()
        elif scelta == '2':
            visualizza_menu()
        elif scelta == '3':
            crea_ordine()
        elif scelta == '4':
            break
        else:
            print("Scelta non valida.")


if __name__ == "__main__":
    main()