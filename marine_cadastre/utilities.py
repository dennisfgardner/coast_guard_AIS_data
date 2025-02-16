from pathlib import Path

"a collection of utility functions"


def list_files_by_type(data_dir: Path, filetype: str) -> list:
    """
    Return filenames containing the specified filetype in given directory.

    Args:
        data_dir: Directory to search for files
        filetype: File extension to search for (e.g., '.txt', '.csv')

    Returns:
        filenames with the specified filetype
    """
    return [path.name for path in Path(data_dir).rglob(f'*{filetype}')]


def is_mmsi_vessel(input_mmsi: int) -> bool:
    """
    Returns True if input is vessle MMSI, else False.

    The first digit of the catagorizes the emitter idetity: 2 - 7 are for
    individual vessels.
    https://en.wikipedia.org/wiki/Maritime_Mobile_Service_Identity

    Args:
        input_mmsi: value to check

    Returns:
        boolean
    """
    assert isinstance(input_mmsi, int), "MMSI must be a integer"
    if 200000000 <= input_mmsi <= 799999999:
        return True
    return False


def is_sog_valid(input_sog: float, max_knots: float = 40.0) -> bool:
    """
    Returns True if input is valid speed over ground (SOG) value, else False.

    SOG must be non-negative and less than or equal to 30 knots.

    Args:
        input_sog: value to check

    Returns:
        boolean
    """
    assert isinstance(input_sog, float), "SOG must be a float"
    if 0.0 <= input_sog <= max_knots:
        return True
    return False


def apply_cog_correction(input_cog: float) -> float:
    """
    Add 406.9 to negative COG values per Marine Cadastre FAQ on COG values.


    Qutote from FAQ: "For data beginning in 2015, COG values that are less than
    0 (negative) are known to be incorrect and can be corrected by adding 409.6
    """
    assert isinstance(input_cog, float), "COG must be a float"
    if input_cog < 0.0:
        return input_cog + 409.6
    return input_cog


def is_cog_valid(input_cog: float) -> bool:
    """
    Returns True if input is valid course over ground (COG) value, else False.

    COG must be greater than or equal to zero and less than 360 degs per FAQ.

    Qutote from FAQ: "Values of 360.0 refer to the COG being unavailable and
    can be ignored."

    Args:
        input_cog: value to check

    Returns:
        boolean
    """
    assert isinstance(input_cog, float), "COG must be a float"
    if 0.0 <= input_cog < 360.0:
        return True
    return False
