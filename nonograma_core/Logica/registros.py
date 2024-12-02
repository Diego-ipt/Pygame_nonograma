import json
import os
from nonograma_core.Logica.tablero_nonograma import *

class Guardado:
    def __init__(self, nombre_nivel, game, identificador):
        self.nombre_nivel = nombre_nivel
        self.game = game
        self.identificador = identificador

    def Save_progress(self):
        # Ruta base calculada en función del archivo actual
        base_dir = os.path.join("levels", "Registros")
        test_name = self.identificador

        # Crea el directorio si no existe
        if not os.path.exists(base_dir):
            print(f"Creando el directorio: {base_dir}")
            os.makedirs(base_dir)

        name_nivel = f"{test_name}.json"
        file_path = os.path.join(base_dir, name_nivel)

        nivel_info = {
            "identificador": test_name,
            "avance": self.game.board.get_matrix(),  # Call the method to get the matrix
        }


        with open(file_path, 'w') as file:
            json.dump(nivel_info, file)
            print(f"Progreso guardado en {file_path}")


class Search_progress():
    def __init__(self):
        print("Inicializando buscador")
        self.avance = None

    def Search(self, identificador):
        base_dir = os.path.join("levels", "Registros")
        test_name = identificador
        name_nivel = f"{test_name}.json"
        file_path = os.path.join(base_dir, name_nivel)
        if os.path.exists(file_path):
            print(f"Progreso encontrado")
            with open(file_path, 'r') as file:
                level = json.load(file)
                self.avance = level["avance"]
            return True
        else:
            print(f"No se encontro progreso")
            return False
