import io
import os
from models.kdm_models import Kdm
import zipfile


def save_kdm(kdm: Kdm, destination_path: str):
    if (kdm.filename.lower().endswith(".zip")):
        with zipfile.ZipFile(io.BytesIO(kdm.file)) as zip_file:
            zip_file.extractall(destination_path)
            
    else:
        file_path = os.path.join(destination_path, kdm.filename)

        with open(file_path, 'wb') as file:
            file.write(kdm.file)


def save_kdms(kdms: list[Kdm], destination_path: str):
    for kdm in kdms:
        save_kdm(kdm, destination_path)
