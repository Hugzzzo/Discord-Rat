# Discord Bot Executable & Build Guide (Educational Project)

> ** AVISO IMPORTANTE Y RENUNCIA DE RESPONSABILIDAD**  
> Este proyecto ha sido desarrollado **exclusivamente con fines educativos y de concienciación sobre seguridad informática**. Muestra cómo estructurar un bot de Discord, compilarlo en un ejecutable y por qué **nunca** se deben incrustar credenciales dentro del binario.

---

##  Descripción del Proyecto

Este repositorio contiene la plantilla básica para un bot de Discord desarrollado en Python. Incluye las instrucciones necesarias para convertir el script en un ejecutable monolítico (`.exe`) con icono personalizado y sin ventana de consola, utilizando **PyInstaller**.
Debes añadir el Token de tu Bot en secret.py elimina las x y pegalo, despues ya estas listo para compilar!!!!
---

##  Requisitos Previos

> [!NOTE]
> **Requisitos del sistema:**
> - Python 3.10 o superior
> - `pip` (gestor de paquetes de Python)
> - Una cuenta de Discord con acceso al Portal de Desarrolladores

---

##  Paso 1: Configurar el Bot en Discord

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PASOS PARA CREAR EL BOT EN DISCORD                   │
├─────────────────────────────────────────────────────────────────────────┤
│ 1. Ve a https://discord.com/developers/applications                     │
│ 2. Haz clic en "New Application" y asigna un nombre.                   │
│ 3. En el menú lateral, entra a "Bot" -> Haz clic en "Reset Token".      │
│ 4. COPIA EL TOKEN y guárdalo (no lo reveles a nadie).                   │
│ 5. En "Privileged Gateway Intents", activa "Message Content Intent".    │
│ 6. En "OAuth2" -> "URL Generator":                                      │
│    - Marca la casilla "bot"                                             │
│    - Selecciona permisos (Send Messages, Read Message History, etc.)    │
│    - Copia la URL generada y abre tu navegador para invitarlo.        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

##  Paso 2: Instalación del Repositorio

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/TU_REPOSOTORIO.git
cd TU_REPOSOTORIO

# 2. Crear y activar entorno virtual
python -m venv venv

# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

# 3. Instalar dependencias necesarias (incluyendo PyInstaller)
pip install -r requirements.txt
pip install pyinstaller
```

---

##  Paso 3: Compilación a Ejecutable (`.exe`)

Para empaquetar todo el código y sus dependencias en un solo ejecutable sin consola visible e incluyendo un icono personalizado, ejecuta el siguiente comando:

```bash
pyinstaller --onefile --noconsole --icon=icono.ico main.py
```

> [!TIP]
> **Explicación de los parámetros:**
> - `--onefile`: Empaqueta todo en un único archivo ejecutable `.exe`.
> - `--noconsole`: Oculta la ventana negra de la consola de comandos al ejecutar la aplicación.
> - `--icon=icono.ico`: Define el icono gráfico del archivo `.exe`.
> - `main.py`: Archivo principal con el código fuente de tu bot.

El ejecutable resultante se guardará automáticamente en la carpeta `dist/ main.exe`.

---

##  ADVERTENCIA DE SEGURIDAD: Extracción de Tokens desde el Bytecode

> [!CAUTION]
> **RIESGO CRÍTICO DE SEGURIDAD**
>
> **NUNCA incrustes (hardcodees) tu Token de Discord directamente en el código de Python antes de compilar.**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                  ¿CÓMO ALGUIEN PUEDE EXTRAER EL TOKEN DEL `.EXE`?               │
├─────────────────────────────────────────────────────────────────────────────────┤
│ PyInstaller NO "compila" el código a lenguaje máquina binario real (C/C++).    │
│ En su lugar, empaqueta el intérprete de Python junto con el código traducido    │
│ a Bytecode (.pyc). Un atacante o analista puede revertirlo fácilmente:          │
│                                                                                 │
│ ┌─────────────────────────────────────────────────────────────────────────────┐ │
│ │ CASILLA 1: Desempaquetado del archivo (.exe -> .pyc)                        │ │
│ │ Usando herramientas de ingeniería inversa como `pyinstxtractor.py`,        │ │
│ │ cualquiera puede extraer el contenido del binario y obtener los archivos    │ │
│ │ de bytecode (.pyc) en segundos.                                             │ │
│ └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│ ┌─────────────────────────────────────────────────────────────────────────────┐ │
│ │ CASILLA 2: Decompilación de Bytecode a Python (.pyc -> .py)                │ │
│ │ Mediante decompiler de bytecode como `pycdc` (decompyle++) o `uncompyle6`, │ │
│ │ el archivo `.pyc` se transforma de nuevo en código Python casi exacto al    │ │
│ │ fuente original, dejando el Token visible en texto plano.                   │ │
│ └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
│ ┌─────────────────────────────────────────────────────────────────────────────┐ │
│ │ CASILLA 3: Inspección de Cadenas de Texto (Strings Extraction)             │ │
│ │ Sin siquiera decompilar, ejecutando comandos de búsqueda de cadenas como:   │ │
│ │ `strings dist/main.exe | grep -E "MTA|OTA|NTA"`                             │ │
│ │ las cadenas con formato de Token de Discord aparecen directamente impresas. │ │
│ └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```


---

