from pathlib import Path

import numpy as np


def main() -> None:
    data_path = Path(__file__).resolve().parent.parent / "datos" / "readings.csv"
    readings = np.loadtxt(data_path, delimiter=",", skiprows=1, ndmin=2)
    print(f"Shape: {readings.shape}")
    print(f"Dimensions: {readings.ndim}")
    print(f"Data type: {readings.dtype}")
    print(f"Elements: {readings.size}")
    print(f"Data bytes: {readings.nbytes}")
    print(f"First reading: {readings[0].tolist()}")


if __name__ == "__main__":
    main()
