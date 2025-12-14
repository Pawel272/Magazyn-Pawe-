import streamlit as st

# --- Zmienna Globalna Magazynu ---
# Globalna lista, którą modyfikujemy w callbackach. 
# Streamlit odświeża skrypt po interakcji, 
# więc ta lista jest ponownie ładowana, ale callbacki modyfikują ją przed ponownym renderowaniem.
magazyn = ["Kawa", "Cukier", "Mąka", "Olej"]

# --- Ustawienia Strony ---
st.set_page_config(
    page_title="Prosty Magazyn Bez Stanu Sesji (Poprawiony)",
    layout="centered"
)

# --- Funkcje Callback Logiki ---

def dodaj_callback():
    """Obsługuje dodawanie towaru po kliknięciu przycisku 'Dodaj do Magazynu'."""
    # Dostęp do wartości pola tekstowego poprzez st.session_state (klucz 'input_dodawanie')
    nowy_towar = st.session_state.input_dodawanie 
    
    towar_do_dodania = nowy_towar.strip().capitalize()
    
    if towar_do_dodania:
        if towar_do_dodania not in magazyn:
            magazyn.append(towar_do_dodania)
            st.success(f"Dodano: {towar_do_dodania}")
            # Kluczowy moment: Wyczyść pole tekstowe (stan sesji) wewnątrz callbacka!
            st.session_state.input_dodawanie = "" 
        else:
            st.warning(f"Towar '{towar_do_dodania}' jest już w magazynie.")
    else:
        st.error("Wprowadź poprawną nazwę towaru.")

def usun_callback():
    """Usuwa wybrany towar z listy magazyn."""
    # Dostęp do wartości selectboxa poprzez st.session_state (klucz 'select_usuwanie')
    towar = st.session_state.select_usuwanie
    
    if towar in magazyn:
        magazyn.remove(towar)
        st.success(f"Usunięto: {towar}")
    else:
        st.error(f"Błąd: Nie znaleziono towaru: {towar}")


# --- Interfejs Użytkownika Streamlit ---

st.title("🛒 Prosty Magazyn (Bez Stanu Sesji - POPRAWIONY)")
st.markdown("Użycie funkcji callback eliminuje błędy związane z modyfikacją stanu sesji.")

# --- Sekcja: Dodawanie Towaru ---
st.header("➕ Dodaj Nowy Towar")
with st.form("form_dodawania"):
    # Klucz 'input_dodawanie' jest niezbędny do dostępu w callbacku
    st.text_input("Nazwa Towaru", key="input_dodawanie")
    
    # Przycisk, który wywołuje funkcję dodaj_callback po kliknięciu
    st.form_submit_button("Dodaj do Magazynu", on_click=dodaj_callback)


# --- Sekcja: Usuwanie Towaru ---
st.header("➖ Usuń Towar")

if magazyn:
    # Klucz 'select_usuwanie' jest niezbędny do dostępu w callbacku
    st.selectbox(
        "Wybierz Towar do Usunięcia", 
        magazyn,
        key="select_usuwanie"
    )
    
    # Przycisk, który wywołuje funkcję usun_callback po kliknięciu
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

st.markdown("---")
st.markdown("Aplikacja stworzona przy użyciu **Streamlit**.")
