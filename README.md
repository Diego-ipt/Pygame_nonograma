# Proyecto_programacion_nonograma
Integrantes:  Javier Alberto Cadagán Parra, Diego Ignacio Pérez Torres, Antonia Renata Montero López

# NONOGRAMA
Nonograma es un juego de ingenio que consiste en colorear casillas en una cuadrícula para revelar una imagen oculta, siguiendo indicaciones numéricas ubicadas al lado del tablero. Estas indicaciones dan a conocer la cantidad de celdas consecutivas que deben colorearse en cada fila y columna. Se busca que el jugador interprete correctamente estas indicaciones para descubrir la imagen escondida y lograr la victoria.

Dentro de las funcionalidades que encontrarás serán: selección de niveles por dificultad, creación y administración de niveles personalizados, guardado de progreso en un nivel, sistema de pistas inteligente, deshacer/rehacer movimientos, entre otros.

Mediante la instalación de este proyecto, serás capaz de probar el juego a nuestro estilo.

## Prerrequisitos

Asegúrate de tener instalados los siguientes requisitos:
- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

Verifica las instalaciones:
En la terminal o bash:
python --version
pip --version

## Ejecutar el proyecto
### Clona el repositorio:
En la terminal o bash
git clone https://github.com/Diego-ipt/Pygame_nonograma.git
cd Pygame_nonograma

### Crear y activar el entorno virtual (windows):
Crear en la terminal o bash:
python -m venv .venv

Activar en la terminal o bash:
\.venv\Scripts\activate , o en su defecto, .\.venv\bin\activate

### Crear y activar el entorno virtual (linux):
En la terminal o bash:
python -m venv .venv
source .venv/bin/activate

### Instala las dependencias del proyecto con:
En la terminal o bash:
pip install -r requirements.txt

### Ejecuta el proyecto con:
En la terminal o bash:
python .\inicio.py

### Ejecutar pruebas:
En la terminal o bash:
pytest nombre_test.py
python -m unittest nombre_test.py
