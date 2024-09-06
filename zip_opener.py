import zipfile
from process_data import ProcessData


class ZipOpener:
    """
    A class to handle operations on a ZIP file containing text files.

    This class provides functionality to read and process text files within a ZIP archive.
    """

    def __init__(self, zip_file: str):
        """
        Initializes the ZipOpener with the specified ZIP file.

        Parameters:
            zip_file (str): The path to the ZIP file to be opened.
        """
        self.zip_file = zip_file
        self.zip = zipfile.ZipFile(zip_file, 'r')

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Ensures that the ZIP file is properly closed when exiting the context.
        """
        self.zip.close()

    def read(self, process_data: ProcessData) -> None:
        """
        Reads and processes all '.txt' files from the ZIP archive.

        For each text file in the ZIP, this method reads its content, splits it into
        lines, and processes each line using the provided ProcessData instance.

        Parameters:
            process_data (ProcessData): The data processor to handle the file content.
        """
        with zipfile.ZipFile(self.zip_file, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if not file_info.is_dir() and file_info.filename.endswith('.txt'):
                    with zip_ref.open(file_info) as file:
                        file_content = file.read().decode('utf-8')
                        rows = file_content.splitlines()
                        process_data.process(rows, file_info.filename)
