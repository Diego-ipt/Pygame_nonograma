import os
import pygame

class AssetManager:
    def __init__(self,base_dir="assets"):
        self.base_dir = base_dir
        self.images = {}
        self.gifs = {}
        self.sounds = {}

    def cargar_imagen(self, name, sub_dir="images"):
        path = os.path.join(self.base_dir, sub_dir, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Imagen {name} no encontrada en: {path}")
        image = pygame.image.load(path)
        self.images[name] = image
        return image

    def cargar_sonido(self, name, sub_dir="sounds"):
        path = os.path.join(self.base_dir, sub_dir, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Sonido {name} no encontrado en: {path}")
        sound = pygame.mixer.Sound(path)
        self.sounds[name] = sound
        return sound

    def cargar_fotogramas(self, name, sub_dir="gifs"):
        path = os.path.join(self.base_dir, sub_dir, name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Carpeta {name} no encontrada en: {path}")

        fotogramas = []
        for archivo in sorted(os.listdir(path)):
            if archivo.endswith('.png'):
                img = pygame.image.load(os.path.join(path, archivo))
                fotogramas.append(img)

        self.gifs[name] = fotogramas
        return fotogramas

# Metodos getters para obtener los recursos cargados en la clase
    def get_image(self, name):
        return self.images.get(name)

    def get_sound(self, name):
        return self.sounds.get(name)

    def get_animation(self, name):
        return self.animations.get(name)