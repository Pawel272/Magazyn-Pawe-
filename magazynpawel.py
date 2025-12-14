import streamlit as st

# --- Ustawienia Strony ---
st.set_page_config(
    page_title="Magazyn Streamlit (Stabilny)",
    layout="centered"
)

# --- 1. Inicjalizacja Magazynu w Stanie Sesji ---
# Jeśli 'magazyn' nie istnieje w st.session_state, tworzymy go z wartościami początkowymi.
# Gwarantuje to, że lista nie zresetuje się po interakcjach użytkownika.
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = ["Mleko", "Chleb", "Jajka", "Ser"]

# --- Funkcje Logiki (Callbacki) ---

def dodaj_towar():
    """Dodaje towar pobrany z inputu do listy w stanie sesji."""
    # Wartość jest pobierana z widżetu tekstowego za pomocą jego klucza
    nowy_towar = st.session_state.input_dodawanie.strip().capitalize()
    
    if nowy_towar:
        if nowy_towar not in st.session_state.magazyn:
            st.session_state.magazyn.append(nowy_towar)
            st.success(f"Dodano: {nowy_towar}")
            # Czyścimy pole wejściowe po pomyślnym dodaniu
            st.session_state.input_dodawanie = "" 
        else:
            st.warning(f"Towar '{nowy_towar}' jest już w magazynie.")
    else:
        st.error("Wprowadź poprawną nazwę towaru.")

def usun_towar():
    """Usuwa wybrany towar z listy w stanie sesji."""
    # Wartość jest pobierana z selectboxa za pomocą jego klucza
    towar_do_usuniecia = st.session_state.select_usuwanie
    
    if towar_do_usuniecia in st.session_state.magazyn:
        st.session_state.magazyn.remove(towar_do_usuniecia)
        st.success(f"Usunięto: {towar_do_usuniecia}")
    # Nie jest potrzebny 'else', ponieważ selectbox pokazuje tylko istniejące elementy.


# --- Interfejs Użytkownika Streamlit ---

st.title("🛒 Stabilny Magazyn Streamlit")
st.markdown("Aplikacja do zarządzania towarem z wykorzystaniem trwałego stanu sesji.")

# --- Sekcja: Dodawanie Towaru ---
st.header("➕ Dodaj Nowy Towar")
with st.form("form_dodawania"):
    # Klucz 'input_dodawanie' pozwala na dostęp do wartości w callbacku i jej czyszczenie
    st.text_input("Nazwa Towaru", key="input_dodawanie")
    
    # Przycisk wywołuje funkcję dodaj_towar
    st.form_submit_button("Dodaj do Magazynu", on_click=dodaj_towar)


# --- Sekcja: Usuwanie Towaru ---
st.header("➖ Usuń Towar")

if st.session_state.magazyn:
    # Selectbox zawsze odzwierciedla aktualną listę magazyn
    st.selectbox(
        "Wybierz Towar do Usunięcia", 
        st.session_state.magazyn,
        key="select_usuwanie"
    )
    
    # Przycisk wywołuje funkcję usun_towar
    st.button(
        "Usuń Wybrany Towar", 
        on_click=usun_towar
    )
else:
    st.info("Magazyn jest pusty, nie można nic usunąć.")


# --- Sekcja: Stan Magazynu ---
st.header("📊 Aktualny Stan Magazynu")

if st.session_state.magazyn:
    # Wyświetlenie jako tabela
    magazyn_df = st.session_state.magazyn
    st.table({"Lp.": list(range(1, len(magazyn_df) + 1)), "Nazwa Towaru": magazyn_df})
    st.metric("Całkowita liczba towarów", len(st.session_state.magazyn))
else:
    st.info("Magazyn jest obecnie pusty.")

st.markdown("---")
