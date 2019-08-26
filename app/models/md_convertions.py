import os
import tempfile
from pdf2image import convert_from_path

def convert_target(filename):   
    with tempfile.TemporaryDirectory() as path:
        images_from_path = convert_from_path(filename, output_folder=path, last_page=19, first_page =0)
    
    base_filename  =  os.path.splitext(os.path.basename(filename) + '.jpg')[0]
    base_filename = base_filename.split('.')[0]
    path_img =f'static/contratos_img/{base_filename}'
    if os.path.isdir(path_img):
        return path_img
    os.mkdir(path_img)

    
    save_dir = path_img
    
    for i,page in enumerate(images_from_path):
        page.save(os.path.join(save_dir, base_filename+f"_{i}.jpg"), 'JPEG')

    return base_filename        