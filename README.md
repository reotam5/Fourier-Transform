# Fourier Series Visualization

A Python application that visualizes Fourier series by drawing complex paths using rotating needles. This project demonstrates how any complex shape can be approximated by a sum of circular motions.

## Overview

This application uses the Fourier transform to break down paths (from SVG images) into rotating vectors (needles) that, when added together, recreate the original path. The visualization shows each needle rotating at different frequencies and amplitudes, with the endpoint tracing the desired shape.

## Features

- Parse SVG files to extract path coordinates
- Apply Discrete Fourier Transform to decompose paths into circular motions
- Visualization of the Fourier series using Pygame
- Adjust parameters like number of coefficients, speed, and scale

## Requirements

The following Python packages are required:

- numpy
- pygame
- pillow
- svg.path

## Installation

1. Clone this repository
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Place your SVG file as image.svg in the project directory
2. Run the application:

```bash
python main.py
```

## How it works

1. The program reads an SVG path or converts an image to an SVG path
2. It calculates Fourier coefficients using the Discrete Fourier Transform
3. Each coefficient becomes a rotating needle with specific amplitude, frequency, and phase
4. When all needles are connected tip-to-tail and rotate at their respective frequencies, the endpoint traces the original path
