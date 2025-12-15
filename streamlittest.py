import streamlit as st
import pandas as pd

# --- Funkcje do zarządzania magazynem ---

def initialize_inventory():
    """Inicjalizuje magazyn w zmiennej session_state Streamlit."""
    if 'inventory' not in st.session_state:
        # Przykładowe początkowe dane
        st.session_state.inventory = [
            {"id": 1, "name": "Młotek", "quantity": 15},
            {"id": 2, "name": "Śrubokręt krzyżakowy", "quantity": 30},
            {"id": 3, "name": "Puszka farby (biała)", "quantity": 5},
        ]

def get_next_item_id():
    """Zwraca kolejny dostępny ID dla nowego towaru."""
    if not st.session_state.inventory:
        return 1
    # Znajduje maksymalny ID i dodaje 1
    return max(item["id"] for item in st.session_state.inventory) + 1

def add_item(name, quantity):
    """Dodaje nowy towar do magazynu."""
    # Prosta walidacja danych
    if name and isinstance(quantity, int) and quantity > 0:
        new_id = get_next_item_id()
        st.session_state.inventory.append({
            "id": new_id,
            "name": name,
            "quantity": quantity
        })
        st.success(f"Dodano towar: **{name}** (ID: {new_id})")
    else:
        st.error("Wprowadź poprawną nazwę i ilość (musi być liczbą całkowitą > 0).")

def delete_item(item_id):
    """Usuwa towar o podanym ID z magazynu."""
    initial_length = len(st.session_state.inventory)
    # Używamy list comprehension do stworzenia nowej listy bez usuwanego elementu
    st.session_state.inventory = [
        item for item in st.session_state.inventory if item["id"] != item_id
    ]
    if len(st.session_state.inventory) < initial_length:
        st.warning(f"Usunięto towar o ID: **{item_id}**")
    else:
        st.error(f"Nie znaleziono towaru o ID: **{item_id}**")

# --- Interfejs użytkownika Streamlit ---

def main():
    st.set_page_config(page_title="Prosty Magazyn", layout="wide")
    st.title("📦 Prosty System Zarządzania Magazynem")
    
    # Inicjalizacja magazynu przy pierwszym uruchomieniu
    initialize_inventory()

    # --- Kolumny dla lepszego układu ---
    col1, col2 = st.columns([1, 2])

    # --- Sekcja Dodawania (Kolumna 1) ---
    with col1:
        st.header("➕ Dodaj Nowy Towar")
        
        # Formularz do dodawania towaru
        with st.form("add_item_form", clear_on_submit=True):
            new_name = st.text_input("Nazwa Towaru")
            # Używamy number_input dla ilości, upewniając się, że jest to liczba całkowita >= 1
            new_quantity = st.number_input("Ilość", min_value=1, step=1, value=1)
            
            submitted = st.form_submit_button("Dodaj do Magazynu")
            
            if submitted:
                # Używamy funkcji do dodania
                add_item(new_name.strip(), int(new_quantity))

    # --- Sekcja Usuwania (Kolumna 1) ---
    with col1:
        st.header("🗑️ Usuń Towar")
        
        # Pobieramy listę ID do wyboru
        item_ids = [item["id"] for item in st.session_state.inventory]
        
        # WARUNEK ZABEZPIECZAJĄCY: Renderujemy selectbox i przycisk tylko, gdy mamy elementy do usunięcia
        if item_ids:
            # Dropdown do wyboru ID do usunięcia
            id_to_delete = st.selectbox(
                "Wybierz ID Towaru do usunięcia",
                options=item_ids,
                index=0,
                key='delete_select' # Dodanie unikalnego klucza
            )
            
            if st.button("Usuń Wybrany Towar", key='delete_button'):
                delete_item(id_to_delete)
                # Ponowne uruchomienie aplikacji jest kluczowe, aby poprawnie odświeżyć stan (np. puste listy)
                st.experimental_rerun()
        else:
            st.info("Brak towarów do usunięcia.")


    # --- Sekcja Wyświetlania (Kolumna 2) ---
    with col2:
        st.header("📋 Aktualny Stan Magazynu")
        
        # WARUNEK ZABEZPIECZAJĄCY: Wyświetlamy tabelę tylko, gdy magazyn nie jest pusty
        if st.session_state.inventory:
            # Tworzenie DataFrame z listy słowników
            df_inventory = pd.DataFrame(st.session_state.inventory)
            
            # Użycie st.dataframe dla ładniejszego i interaktywnego wyświetlania
            st.dataframe(
                df_inventory,
                use_container_width=True,
                column_config={
                    "id": st.column_config.Column("ID", width="small"),
                    "name": st.column_config.Column("Nazwa Towaru"),
                    "quantity": st.column_config.NumberColumn("Ilość", format="%d")
                }
            )
            
            total_items = sum(item['quantity'] for item in st.session_state.inventory)
            st.markdown(f"**Całkowita liczba wszystkich sztuk:** `{total_items}`")
            st.markdown(f"**Liczba unikalnych pozycji:** `{len(st.session_state.inventory)}`")
        else:
            st.info("Magazyn jest pusty! Dodaj pierwszy towar.")

if __name__ == "__main__":
    main()
