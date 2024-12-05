"""
Copyright (C) 2023, Johannes Dora, johannes.dora@desy.de

"""

from skimage.draw import disk
import numpy as np
import torch


def forward_propagation_holo(z01, z02):
    """
    1)
    Messaufbau: Fresnel-Zahl -> Deketorpixelgröße, z1 und z2, Wellenlänge Beleuchtung

    Forwardsimulation => Forwardmodel/Problem simulation davon
    Fresnel-prop. ist approx. von Free-space prop. Obj. zu Detektor
    Eigentlich nur für parallelen Strahl (nicht Kegel), Daher
    Fesnel-scaling theorem: Vergrößerung durch kegelstrahl:
        (z01 + z12) / z01 =: M(agnification)

    Fr = Detektorpixelgröße^2 / (Wellenl. * z12 * M)    ---> Fr \approx 10e-3
    """

    dx = 6500  # nm
    lam = 1.2389 / 11  # nm / keV (11 or 17)

    M = z02 / z01
    Fr = dx**2 / (lam * (z02 - z01) * M)

    print(Fr)

    """
    2) Beleuchtung#
    Intensität I = Amplitude^2 => A
    A = np.zeros(2048)

    """
    A = np.ones((2048, 2048), dtype=np.float32)  # ohne phi array cfloat
    A_0 = 1.0  # mean constant :( of illumination
    # flatfield correction, damit A am Ende 1 ergibt, sonst ist es irgendwas. Und dann auch A_0 = 1

    phi = np.ones((2048, 2048), dtype=np.float32)
    phi_0 = 0.0
    probe = A_0 * A * np.exp(1j * phi_0 * phi)

    """
    3) Objekt
    Phantoms
    delta/beta IMMER Konstant abh. material und Energie, aber NICHT Dicke
    """

    d = 20e-6  # 20µm
    transmission = 0.947805
    O_mu = -np.log(
        transmission
    )  # Absorption coeffictient; some kind of integral over beta

    delta, beta = (
        2.97202632e-06,
        2.40418405e-08,
    )  # looked up at https://henke.lbl.gov/optical_constants/getdb2.html
    C = delta / beta
    O_phi = -C * O_mu  # phase shift (similar to absorption)

    O_shape = np.zeros((2048, 2048))
    O_shape[disk((1023, 1023), radius=128)] = 1

    noise = np.random.normal(0, 1, size=O_shape.shape)
    # O_shape += 0.01*noise   # TODO: maybe just gaussian blur to remove edges and then renormalize

    O_ref = (
        (O_phi + 1j * O_mu) * O_shape
    )  # refractive, transmission function, irgendwas mit P multiplizieren -> Scattering

    obj = np.exp(1j * O_ref)

    """
    4) Wellenfeld (direkt) hinter dem Objekt

    """

    psi_exit = obj * probe

    """
    5) Wellenfeld am Detektor
    """
    running_device = torch.device("cpu")

    sample_grid = torch.meshgrid(
        torch.fft.fftfreq(obj.shape[0], device=running_device, dtype=torch.float),
        torch.fft.fftfreq(obj.shape[1], device=running_device, dtype=torch.float),
        indexing="ij",
    )

    xi, eta = sample_grid

    kernel_func = torch.exp((-1j * np.pi) / Fr * (xi * xi + eta * eta)).type(
        torch.cfloat
    )

    psi_det = torch.fft.ifft2(
        torch.fft.fft2(torch.tensor(psi_exit, device=running_device)) * kernel_func
    )

    """
    6) Hologram

    -> Betragsquadrant
    """

    holo = torch.abs(psi_det)

    return holo, obj
