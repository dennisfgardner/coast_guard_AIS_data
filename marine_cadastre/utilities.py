from pathlib import Path

"a collection of utility functions"


def list_files_by_type(data_dir, filetype):
    """
    Return filenames list containing the specified filetype in given directory.

    Args:
        data_dir: Directory to search for files
        filetype: File extension to search for (e.g., '.txt', '.csv')

    Returns:
        List of filenames with the specified filetype
    """
    return [path.name for path in Path(data_dir).rglob(f'*{filetype}')]
