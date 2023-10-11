from tempfile import SpooledTemporaryFile
from datetime import datetime
import os


def get_temp_file_from_disk(path: str) -> SpooledTemporaryFile:
    if not os.path.exists(path):
        raise Exception(f"File {path} not found")

    # Create a SpooledTemporaryFile
    spooled_temp_file = SpooledTemporaryFile(max_size=2000)
    # Open the file you want to read from filesystem
    with open(path, "rb") as f:
        # Read the content of the file
        data = f.read()
        # Write the content to the SpooledTemporaryFile
        spooled_temp_file.write(data)

    spooled_temp_file.seek(0)
    return spooled_temp_file


def save_uploaded_file_to_disk(in_file: SpooledTemporaryFile, filename):
    # https://stackoverflow.com/a/63581187/15965186
    current_time = datetime.now()
    current_time = current_time.strftime("%Y-%m-%d-%H-%M-%S")
    out_file_path = f"mails/{current_time}_{filename}"
    print(f"Saving file to {out_file_path}")

    with open(out_file_path, "wb") as out_file:
        while content := in_file.read(1024):  # read chunk
            out_file.write(content)  # write chunk
