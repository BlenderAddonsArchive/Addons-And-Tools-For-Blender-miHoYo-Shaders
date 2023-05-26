
from setup_wizard.texture_import_setup.game_texture_importers import GameTextureImporter


class TextureImporterService:
    def __init__(self, game_texture_importer: GameTextureImporter):
        self.game_texture_importer = game_texture_importer

    def import_textures(self):
        return self.game_texture_importer.import_textures()
