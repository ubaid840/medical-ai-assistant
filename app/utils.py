from pathlib import Path
import shutil


def save_uploaded_file(uploaded_file, data_dir):
    """
    Save uploaded PDF into data directory.
    """

    data_dir = Path(data_dir)
    data_dir.mkdir(exist_ok=True)

    file_path = data_dir / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def get_pdf_files(data_dir):
    """
    Get all PDFs from data directory.
    """

    data_dir = Path(data_dir)

    if not data_dir.exists():
        return []

    return list(data_dir.glob("*.pdf"))


def delete_file(file_path):
    """
    Delete selected file.
    """

    file_path = Path(file_path)

    if file_path.exists():
        file_path.unlink()