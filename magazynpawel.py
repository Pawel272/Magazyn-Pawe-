import streamlit as st

# --- Zmienna Globalna Magazynu ---
# Ta lista będzie resetowana przy każdym uruchomieniu skryptu,
# ale Streamlit ładuje widżety z kluczami, co pozwala na interakcję.
magazyn = ["Kawa", "Cukier", "Mąka", "Olej"]

# --- Ustawienia Strony ---
st.set_page_config(
    page_title="Prosty Magazyn Bez Stanu Sesji",
    layout="centered"
)

# --- Funkcje Logiki ---

def dodaj_towar(nazwa_towaru):
    """Dodaje towar do magazynu, jeśli nie istnieje."""
    towar_do_dodania = nazwa_towaru.strip().capitalize()
    if towar_do_dodania and towar_do_dodania not in magazyn:
        magazyn.append(towar_do_dodania)
        st.success(f"Dodano: {towar_do_dodania}")
    elif towar_do_dodania in magazyn:
        st.warning(f"Towar '{towar_do_dodania}' jest już w magazynie.")
    else:
        st.error("Wprowadź poprawną nazwę towaru.")
        
# --- Interfejs Użytkownika Streamlit ---

st.title("🛒 Prosty Magazyn (Bez Sesji)")
st.markdown("Towary są przechowywane w globalnej liście, która jest modyfikowana przez funkcje.")

# --- Sekcja: Dodawanie Towaru ---
st.header("➕ Dodaj Nowy Towar")

# Używamy formularza (st.form) do grupowania wejścia i przycisku.
# Po naciśnięciu przycisku submit, dane z inputów wewnątrz formularza są dostępne.
with st.form("form_dodawania"):
    # Musimy użyć st.text_input, aby pobrać wartość po submit
    nowy_towar = st.text_input("Nazwa Towaru", key="input_dodawanie")
    przycisk_dodaj = st.form_submit_button("Dodaj do Magazynu")
    
    # Warunek spełniony tylko po kliknięciu przycisku
    if przycisk_dodaj:
        # Ponieważ użyliśmy klucza, wartość jest dostępna
        towar_do_dodania = st.session_state.input_dodawanie 
        dodaj_towar(towar_do_dodania)
        # Opcjonalnie: wyczyść pole tekstowe po dodaniu
        st.session_state.input_dodawanie = "" 
        st.rerun()


# --- Sekcja: Usuwanie Towaru ---
st.header("➖ Usuń Towar")

if magazyn:
    # Używamy st.selectbox do wybrania towaru
    towar_do_usuniecia = st.selectbox(
        "Wybierz Towar do Usunięcia", 
        magazyn,
        key="select_usuwanie"
    )
    
    # Funkcja usuwająca wywoływana przez callback
    def usun_callback():
        """Usuwa wybrany towar z listy magazyn."""
        towar = st.session_state.select_usuwanie
        if towar in magazyn:
            magazyn.remove(towar)
            st.success(f"Usunięto: {towar}")
        else:
            st.error(f"Błąd: Nie znaleziono towaru: {towar}")

    # Używamy on_click, aby wykonać funkcję przed odświeżeniem
    st.button(
        "Usuń Wybrany Towar", 
        on_click=usun_callback
    )
else:
    st.info("Magazyn jest pusty, nie można nic usunąć.")


# --- Sekcja: Stan Magazynu ---
st.header("📊 Aktualny Stan Magazynu")

if magazyn:
    st.table({"Lp.": list(range(1, len(magazyn) + 1)), "Nazwa Towaru": magazyn})
    st.metric("Całkowita liczba towarów", len(magazyn))
else:
    st.info("Magazyn jest obecnie pusty.")
