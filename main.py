import streamlit as st
from database import (
    init_db, is_first_run, set_master_password_hash, get_master_password_hash,
    update_master_password_hash, add_password, get_passwords,
    search_passwords_by_title, delete_password
)
from crypto_utils import encrypt, decrypt, hash_password, check_password

st.set_page_config(page_title="Gestor de Contraseñas", layout="centered")
init_db()

# estado de la sesion
if "page" not in st.session_state:
    st.session_state.page = "auth"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# funciones
def go_to(page):
    st.session_state.page = page

def require_auth(func):
    def wrapper():
        if not st.session_state.authenticated:
            st.error("Debes ingresar la contraseña maestra.")
            st.stop()
        func()
    return wrapper

# Login
if st.session_state.page == "auth":
    st.title("🔐 Gestor de Contraseñas")

    if is_first_run():
        st.subheader("Establecer contraseña maestra")
        pw1 = st.text_input("Nueva contraseña maestra", type="password")
        pw2 = st.text_input("Confirmar contraseña", type="password")
        if st.button("Guardar"):
            if pw1 == pw2 and pw1:
                set_master_password_hash(hash_password(pw1))
                st.success("Contraseña maestra guardada.")
                st.session_state.authenticated = True
                go_to("menu")
            else:
                st.error("Las contraseñas no coinciden o están vacías.")
    else:
        st.subheader("Ingresar contraseña maestra")
        pw = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            if check_password(pw, get_master_password_hash()):
                st.session_state.authenticated = True
                st.session_state.master_password = pw
                go_to("menu")
                st.rerun()
            else:
                st.error("Contraseña incorrecta")

# menu
elif st.session_state.page == "menu":
    st.title("Gestor de Contraseñas")
    st.success("Sesión iniciada")

    st.button("➕ Agregar contraseña", on_click=lambda: go_to("add"))
    st.button("🔍 Buscar por servicio", on_click=lambda: go_to("search"))
    st.button("📋 Ver todas las contraseñas", on_click=lambda: go_to("view"))
    st.button("🔁 Cambiar contraseña maestra", on_click=lambda: go_to("change"))
    st.button("🚪 Cerrar sesión", on_click=lambda: [st.session_state.clear(), go_to("auth")])

# agregar contraseñas
elif st.session_state.page == "add":
    require_auth(lambda: None)()

    st.subheader("➕ Nueva contraseña")
    title = st.text_input("Nombre del servicio (Facebook, Gmail, etc)")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Guardar"):
        if title and username and password:
            encrypted = encrypt(password)
            add_password(title, username, encrypted)
            st.success("Contraseña guardada correctamente.")
        else:
            st.warning("Completa todos los campos.")
    st.button("⬅️ Volver", on_click=lambda: go_to("menu"))

# ver contraseñas
elif st.session_state.page == "view":
    require_auth(lambda: None)()

    st.subheader("📋 Todas las contraseñas")
    passwords = get_passwords()
    if passwords:
        for p in passwords:
            with st.expander(f"{p.title} ({p.username})"):
                st.code(decrypt(p.encrypted_password), language='text')
                if st.button("🗑 Eliminar", key=f"del_{p.id}"):
                    delete_password(p.id)
                    st.success("Eliminado correctamente.")
                    st.rerun()
    else:
        st.info("No hay contraseñas registradas.")
    st.button("⬅️ Volver", on_click=lambda: go_to("menu"))

# buscar por servicio
elif st.session_state.page == "search":
    require_auth(lambda: None)()

    st.subheader("🔍 Buscar por nombre de servicio")
    search = st.text_input("Buscar (ej. github, facebook, etc)")
    if search:
        results = search_passwords_by_title(search)
        if results:
            for p in results:
                with st.expander(f"{p.title} ({p.username})"):
                    st.code(decrypt(p.encrypted_password), language='text')
        else:
            st.warning("No se encontraron resultados.")
    st.button("⬅️ Volver", on_click=lambda: go_to("menu"))

# cambiar contraseña maestra
elif st.session_state.page == "change":
    require_auth(lambda: None)()

    st.subheader("🔁 Cambiar contraseña maestra")
    actual = st.text_input("Contraseña actual", type="password")
    nueva = st.text_input("Nueva contraseña", type="password")
    confirm = st.text_input("Confirmar nueva contraseña", type="password")

    if st.button("Actualizar"):
        if not check_password(actual, get_master_password_hash()):
            st.error("Contraseña actual incorrecta.")
        elif nueva != confirm or not nueva:
            st.error("Las nuevas contraseñas no coinciden o están vacías.")
        else:
            update_master_password_hash(hash_password(nueva))
            st.success("Contraseña maestra actualizada.")
            st.session_state.master_password = nueva
    st.button("⬅️ Volver", on_click=lambda: go_to("menu"))