''' EMMA - Enhanced Modeling & Mesh Assets (See clickup)
    
    NOTE: TEMPORARY all-emma file. 
    - Should organize and move things around when it gets crowded in here
    
    '''
import os
import re
from print_tricks import pt
import open3d as o3d
    
class GetModelsAndTextures:
    
    @classmethod
    def process_models_and_textures(cls, folder_path):
        models = cls.get_models_from_folder(folder_path)
        models_and_textures = {}

        for model in models:
            original_texture = cls.get_texture_from_mtl(model, folder_path)
            if original_texture:
                models_and_textures[model] = {"original": original_texture}
                
        return models_and_textures

    @staticmethod
    def get_texture_from_mtl(model, folder_path):
        base_name = os.path.splitext(model)[0]

        mtl_file_name = os.path.join(folder_path, f'{base_name}.mtl')
        try:
            with open(mtl_file_name, 'r') as f:
                mtl = f.read()
        except FileNotFoundError:
            pt(f"Can't find the texture for {model}")
            return None

        match = re.search(r'map_kd\s+(.*\.(?:png|jpg|jpeg|tga|bmp))', mtl, re.IGNORECASE)
        if match:
            full_texture_path = match.group(1)
            texture_file_name = os.path.split(full_texture_path)[-1]

            return texture_file_name
        else:
            pt(f"Can't find the texture for {model}")
            return None

    @staticmethod
    def get_models_from_folder(folder_path):
        return [f for f in os.listdir(folder_path) if f.endswith('.obj')]
    
if __name__ == '__main__':
    folder_path = "./assets/"
    models_and_textures = GetModelsAndTextures.process_models_and_textures(folder_path)