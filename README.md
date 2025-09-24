🔐 Gestor de Contraseñas Seguro

Este es un proyecto de gestor de contraseñas desarrollado en Python + Streamlit + SQLite, que permite guardar y administrar contraseñas de forma segura utilizando cifrado con Fernet (AES) y una contraseña maestra para acceder.

🚀 Tecnologías usadas

Python 3.11

Streamlit
 – interfaz web simple y rápida

SQLite + SQLAlchemy
 – base de datos ligera y organizada

Cryptography (Fernet)
 – cifrado seguro

Hashlib (SHA-256)
 – hash de la contraseña maestra

 ⚙️ Instalación

Clonar este repositorio o descargar el código:

git clone https://github.com/MartinAban/Diplomado.git


Crear y activar un entorno virtual:

python -m venv venv
# En Windows
venv\Scripts\activate
# En Mac/Linux
source venv/bin/activate

# Instalar dependencias:
pip install -r requirements.txt en la consola

▶️ Ejecución

Inicia la aplicación con:

streamlit run main.py

📖 Uso del sistema

Primer inicio

Se te pedirá crear una contraseña maestra (no recuperable).

Esta se guarda como hash (SHA-256), nunca en texto plano.

Menú principal

➕ Agregar contraseña: guarda un servicio (ej: Gmail, Facebook), usuario y clave. La contraseña se cifra antes de guardarse en la base de datos.

📋 Ver todas: muestra las contraseñas guardadas, con opción de eliminarlas.

🔍 Buscar por servicio: permite filtrar contraseñas por nombre (ej: "github").

🔁 Cambiar contraseña maestra: requiere la clave actual y la nueva.

🚪 Cerrar sesión: vuelve a la pantalla de login.

Base de datos y seguridad

Las contraseñas se almacenan en password_manager.db dentro de la tabla passwords.

Están cifradas con Fernet, por lo que en la base de datos aparecen como tokens.

Solo con la clave Fernet guardada en fernet.key se pueden descifrar.

Si se borra fernet.key, las contraseñas anteriores no podrán recuperarse.