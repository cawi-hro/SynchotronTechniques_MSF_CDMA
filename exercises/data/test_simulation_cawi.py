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
    sod=0.2,
    sdd=1,
    detector_pixel_size=6500,
    beam_energy=11,
    beta=2.3862e-08,
    delta=2.9720e-06,
    density=1.74,
    object_thickness=0.05,
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
    - beta: Absorptioncoefficient of the material.
    - delta: Diffraction coefficient of the material.
    - density: Density of the material (in g/cm^3).
    - detector_pixel_size: Size of the detector (in micro m).
    - object_shape_type: Type of object shape to simulate. 'disk' for a circular object, 'rectangle' for a rectangular object, 'triangle' for a triangular object.

    Returns:
    - holo: The hologram captured at the detector.
    - obj: The complex representation of the object.
    - para: Additional parameters of the simulation.

    Example:
    - holo, obj = forward_propagation_holo(sod=0.05, sdd=20, detector_pixel_size=6500, beam_energy=11, beta=2.3862e-08, delta=2.9720e-06, object_thickness=0.05, add_noise=False, object_shape_type="disk")
      for Mg and 11keV and object thickness of 0.05mm
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

    # Create the illumination function
    illumination = np.ones(SCREEN_SIZE, dtype=np.float32)  # Uniform illumination
    constant_illumination = 1.0

    # Phase shift (set to zero for this example)
    phase_shift = np.ones(SCREEN_SIZE, dtype=np.float32)
    phi_0 = 0.0  # Initial phase
    probe = constant_illumination * illumination * np.exp(1j * phi_0 * phase_shift)

    # linear attenuation coefficient in 1/m
    lin_att_coeff = 4 * np.pi * beta / (wavelength)
    # mass attenuation coefficient in m^2/kg
    mass_att_coeff = lin_att_coeff / (density * 1e3)

    # calculate attenuation
    attenuation = 1 - np.exp(-lin_att_coeff * object_thickness / 1e3)

    # Calculate transmission
    transmission = 1 - attenuation
    # absorption_coefficient = lin_att_coeff
    absorption_coefficient = -np.log(attenuation)  # Absorption coefficient
    phase_shift_object = (
        -delta / beta * absorption_coefficient
    )  # Phase shift caused by the object

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

    # output parameters
    para = (
        f"Fresnel Number: {Fresnel_number:.4f}\n"
        f"Magnification: {magnification}\n"
        f"Wavelength: {wavelength:.2e} m\n"
        f"Attenuation: {attenuation:.4f}\n"
        f"Transmission: {transmission:.4f}\n"
        f"Linear attenuation coefficient: {lin_att_coeff / 1e3:.2f} 1/m\n"
        f"HVL {np.log(2) / lin_att_coeff * 1e3:.2f} mm\n"
    )

    return (
        holo,
        obj,
        para,
    )  # Return the hologram, the object representation and additional parameters
