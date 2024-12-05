"""
Copyright (C) 2023, Johannes Dora, johannes.dora@desy.de
Modified by Carsten Wickmann, carsten.wickmann@uni-rostock.de


This script simulates the forward propagation of a holographic signal through a Fresnel-based model.
It consists of the following steps:
1. Defines parameters and setup for the simulation.
2. Creates an illumination function.
3. Defines the object to be imaged.
4. Simulates the wave field exiting the object.
5. Computes the wave field at the detector.
6. Generates the hologram.

"""

from skimage.draw import disk, rectangle, polygon
import numpy as np
import torch
from scipy.constants import h, c  # in J/s and m/s


def forward_propagation_holo(
    sod=1,
    sdd=1,
    detector_pixel_size=1,
    beam_energy=1,
    beta=1,
    delta=1,
    object_thickness=1,
    add_noise=False,
    object_shape_type="disk",
):
    """
    Simulates the forward propagation of x-rays through an optical system.

    Parameters:
    - sod: Distance from the x-ray source to the object (in m).
    - sdd: Distance from the object to the detector (in m).
    - add_noise: Boolean flag to add noise to the object shape.
    - beam_energy: Energy of the incident beam (in keV).
    - object_thickness: Thickness of the object (in mm).
    - beta:  coefficient of the material.
    - delta: Diffraction coefficient of the material.
    - detector_pixel_size: Size of the detector (in micro m).
    - object_shape_type: Type of object shape to simulate. 'disk' for a circular object, 'rectangle' for a rectangular object, 'triangle' for a triangular object.

    Returns:
    - holo: The hologram captured at the detector.
    - obj: The complex representation of the object.
    """

    SCREEN_SIZE = (2000, 2000)  # Size of the detector screen (in pixels)

    # Optical parameters
    wavelength = (h * c) / (
        beam_energy * 1e3 * 1.602e-19
    )  # Wavelength in m | lambda = h*c / E | 1 eV = 1.602e-19 J

    # Magnification calculation using Fresnel number
    magnification = sdd / sod
    Fresnel_number = (detector_pixel_size * 1e-9) ** 2 / (
        wavelength * (sdd - sod) * magnification
    )

    print("Fresnel Number:", Fresnel_number)
    print("Magnification:", magnification)
    print("Wavelength:", wavelength)

    # Create the illumination function
    illumination = np.ones(SCREEN_SIZE, dtype=np.float32)  # Uniform illumination
    constant_illumination = 1.0

    # Phase shift (set to zero for this example)
    phase_shift = np.ones(SCREEN_SIZE, dtype=np.float32)
    phi_0 = 0.0  # Initial phase
    probe = constant_illumination * illumination * np.exp(1j * phi_0 * phase_shift)

    # Define the object to be imaged
    alpha = (
        4 * np.pi * beta / (wavelength)
    )  # Absorption coefficient of the material (in 1/m)
    # Calculate transmission
    transmission = np.exp(-alpha * object_thickness / 1e3)
    print("Transmission:", transmission)

    absorption_coefficient = -np.log(transmission)  # Absorption coefficient
    C = delta / beta
    phase_shift_object = -C * absorption_coefficient  # Phase shift caused by the object

    # Create the object shape (disk)
    object_shape = np.zeros(SCREEN_SIZE)

    if object_shape_type == "disk":
        object_shape[disk((1000, 1000), radius=200)] = 1  # Circular object
    elif object_shape_type == "rectangle":
        start = (700, 900)  # Starting point (row, col)
        extent = (500, 500)  # Height and width
        object_shape[rectangle(start, extent=extent, shape=object_shape.shape)] = (
            1  # Rectangle object
        )
    elif object_shape_type == "triangle":
        # Define triangle vertices
        triangle_vertices = np.array([[1000, 950], [900, 1200], [1100, 1200]])
        rr, cc = polygon(
            triangle_vertices[:, 0], triangle_vertices[:, 1], object_shape.shape
        )
        object_shape[rr, cc] = 1  # Triangle object

    # Add noise to the object shape if needed (commented out for now)
    if add_noise:
        noise = np.random.normal(0, 1, size=object_shape.shape)
        object_shape += 0.01 * noise  # Optionally add noise

    # Create complex representation of the object (refractive and absorption)
    complex_object = (phase_shift_object + 1j * absorption_coefficient) * object_shape
    obj = np.exp(1j * complex_object)  # Exponential to represent wavefront

    # Compute the wavefield exiting the object
    psi_exit = obj * probe

    # Compute the wavefield at the detector using FFT
    running_device = torch.device("cpu")  # Set device to CPU

    # Create sample grid for FFT
    sample_grid = torch.meshgrid(
        torch.fft.fftfreq(obj.shape[0], device=running_device, dtype=torch.float),
        torch.fft.fftfreq(obj.shape[1], device=running_device, dtype=torch.float),
        indexing="ij",
    )

    xi, eta = sample_grid  # Sample coordinates in Fourier space

    # Kernel function for Fresnel propagation
    kernel_function = torch.exp((-1j * np.pi) / Fresnel_number * (xi**2 + eta**2)).type(
        torch.cfloat
    )

    # Compute the detector wavefield
    psi_det = torch.fft.ifft2(
        torch.fft.fft2(torch.tensor(psi_exit, device=running_device)) * kernel_function
    )

    # Compute the hologram by taking the absolute value
    holo = torch.abs(psi_det)

    return holo, obj  # Return the hologram and the object representation
