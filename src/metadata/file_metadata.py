import datetime
import os
from dataclasses import dataclass


@dataclass
class FileMetadata:
    creation_time: datetime.datetime
    modification_time: datetime.datetime

    # def __post_init__(self):
    #     assert (
    #         self.creation_time <= self.modification_time
    #     ), "Creation time must be before modification time."
    #     assert (
    #         self.creation_time <= datetime.datetime.now()
    #     ), "Creation time must be in the past."
    #     assert (
    #         self.modification_time <= datetime.datetime.now()
    #     ), "Modification time must be in the past."

    def __str__(self):
        return f"Creation time: {self.creation_time}, Modification time: {self.modification_time}"

    @classmethod
    def from_file(cls, filepath: str) -> "FileMetadata":
        """
        Create a FileMetadata instance from a file path.
        Args:
            filepath (str): The path to the file.
        Returns:
            FileMetadata: An instance of FileMetadata containing the creation and modification times of the file.
        Prints:
            The file path, creation time, and modification time.
        """

        print(f"filepath = {filepath}")
        file_stats = os.stat(filepath)
        creation_time = datetime.datetime.fromtimestamp(file_stats.st_ctime)
        modification_time = datetime.datetime.fromtimestamp(file_stats.st_mtime)
        print(f"Creation time: {creation_time}")
        print(f"Modification time: {modification_time}")
        return cls(creation_time, modification_time)
