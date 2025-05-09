import numpy as np
from typing import List, Tuple
from PIL import Image
from svg.path import parse_path
from xml.dom import minidom

def image_to_svg(image_file: str, svg_file: str) -> None:
    """
    Convert an image to SVG format (with path) and save it to a file.
    
    Args:
        image_file: Path to the input image file.
        svg_file: Path to the output SVG file.
    """
    img = Image.open(image_file)
    img = img.convert("L")  # Convert to grayscale
    width, height = img.size
    data = np.array(img)

    # Create SVG path data
    path_data = []
    for y in range(height):
        for x in range(width):
            if data[y, x] < 128:  # Threshold for black pixels
                path_data.append(f"M{x},{y} L{x+1},{y}")

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">
        <path d="{' '.join(path_data)}" fill="none" stroke="black"/>
    </svg>"""

    with open(svg_file, "w") as f:
        f.write(svg_content)


def parse_svg_to_coordinates(svg_file: str, num_points: int = 1000, max_x: int = 800, max_y: int = 600) -> List[Tuple[float, float]]:
    doc = minidom.parse(svg_file)
    path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
    doc.unlink()
    
    if not path_strings:
        raise ValueError("No paths found in the SVG file")
    
    coordinates = []
    for path_string in path_strings:
        path = parse_path(path_string)
        path_length = path.length()
        
        # Sample evenly along the path
        for i in range(num_points):
            step = i / (num_points - 1) if num_points > 1 else 0
            point = path.point(step)
            coordinates.append((point.real, point.imag))

    # center the coordinates (0,0) is the center of the image
    x_coords, y_coords = zip(*coordinates)
    x_mean = np.mean(x_coords)
    y_mean = np.mean(y_coords)
    coordinates = [(x - x_mean + max_x / 2, y - y_mean + max_y / 2) for x, y in coordinates]

    # scale the coordinates to fit within the specified dimensions
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    x_range = x_max - x_min
    y_range = y_max - y_min
    scale_x = max_x / x_range if x_range > 0 else 1
    scale_y = max_y / y_range if y_range > 0 else 1
    scale = min(scale_x, scale_y)
    coordinates = [(x * scale, y * scale) for x, y in coordinates]

    return coordinates


def discrete_fourier_transform(coordinates: List[Tuple[float, float]]) -> List[Tuple[float, float, float]]:
    """
    Perform a discrete Fourier transform on the given coordinates. consider 0,0 as the top left corner
    
    Args:
        coordinates: List of (x, y) tuples representing the points.
        
    Returns:
        List of (amplitude, frequency, phase) tuples for each Fourier component.
    """
    n = len(coordinates)
    if n == 0:
        return []

    # Convert coordinates to complex numbers
    complex_coords = np.array([complex(x, y) for x, y in coordinates])
    
    # Perform DFT
    dft = np.fft.fft(complex_coords)

    # Calculate amplitude, frequency, and phase
    amplitudes = np.abs(dft)/n
    frequencies = np.fft.fftfreq(n)
    phases = np.angle(dft)

    # Normalize frequencies to be positive
    frequencies = (frequencies + 0.5) % 1 - 0.5
    frequencies = frequencies * n / (2 * np.pi)
    fourier_components = [(amplitude, frequency, phase) for amplitude, frequency, phase in zip(amplitudes, frequencies, phases)]

    # remove the DC component (frequency = 0)
    fourier_components = [comp for comp in fourier_components if comp[1] != 0]

    return fourier_components
    



    
