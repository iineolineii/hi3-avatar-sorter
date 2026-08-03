from pathlib import Path

from .enums import PartIDFormat


def main(
    source_folder: str | Path,
    output_folder: str | Path = "output",
    part_id_format: "PartIDFormat | None" = None
) -> None:
    # TODO: implement main entry point
    raise NotImplementedError("WIP")


if __name__ == "__main__":
    main(input("Enter source folder path: "))
