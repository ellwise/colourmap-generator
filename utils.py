# NOTE: This is taken/modified from scikit-image. Copyright notice below.
#
# License (Modified BSD)
#
# Copyright (C) 2011, the scikit-image team All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer. Redistributions in
#     binary form must reproduce the above copyright notice, this list of
#     conditions and the following disclaimer in the documentation and/or
#     other materials provided with the distribution. Neither the name of
#     skimage nor the names of its contributors may be used to endorse or
#     promote products derived from this software without specific prior
#     written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import numpy as np


xyz_from_rgb = np.array(
    [
        [0.412453, 0.357580, 0.180423],
        [0.212671, 0.715160, 0.072169],
        [0.019334, 0.119193, 0.950227],
    ]
)

rgb_from_xyz = np.linalg.inv(xyz_from_rgb)

illuminant = (0.95047, 1.0, 1.08883)


def lch2lab(lch):
    lch = _prepare_lab_array(lch)
    c, h = lch[..., 1], lch[..., 2]
    lch[..., 1], lch[..., 2] = c * np.cos(h), c * np.sin(h)
    return lch


def lab2lch(lab):
    lab = _prepare_lab_array(lab)
    a, b = lab[..., 1], lab[..., 2]
    lab[..., 1], lab[..., 2] = _cart2polar_2pi(a, b)
    return lab


def lab2rgb(lab):
    return xyz2rgb(lab2xyz(lab))


def rgb2lab(rgb):
    return xyz2lab(rgb2xyz(rgb))


def lab2xyz(lab):
    arr = _prepare_colorarray(lab).copy()

    L, a, b = arr[..., 0], arr[..., 1], arr[..., 2]
    y = (L + 16.0) / 116.0
    x = (a / 500.0) + y
    z = y - (b / 200.0)

    if np.any(z < 0):
        invalid = np.nonzero(z < 0)
        print("Color data out of range: Z < 0 in %s pixels" % invalid[0].size)
        z[invalid] = 0

    out = np.stack([x, y, z], axis=-1)

    mask = out > 0.2068966
    out[mask] = np.power(out[mask], 3.0)
    out[~mask] = (out[~mask] - 16.0 / 116.0) / 7.787

    # rescale to the reference white (illuminant)
    xyz_ref_white = get_xyz_coords()
    out *= xyz_ref_white
    return out


def xyz2rgb(xyz):
    arr = _convert(rgb_from_xyz, xyz)
    mask = arr > 0.0031308
    arr[mask] = 1.055 * np.power(arr[mask], 1 / 2.4) - 0.055
    arr[~mask] *= 12.92
    np.clip(arr, 0, 1, out=arr)
    return arr


def xyz2lab(xyz):
    arr = _prepare_colorarray(xyz)

    xyz_ref_white = get_xyz_coords()

    # scale by CIE XYZ tristimulus values of the reference white point
    arr = arr / xyz_ref_white

    # Nonlinear distortion and linear transformation
    mask = arr > 0.008856
    arr[mask] = np.cbrt(arr[mask])
    arr[~mask] = 7.787 * arr[~mask] + 16.0 / 116.0

    x, y, z = arr[..., 0], arr[..., 1], arr[..., 2]

    # Vector scaling
    L = (116.0 * y) - 16.0
    a = 500.0 * (x - y)
    b = 200.0 * (y - z)

    return np.concatenate([x[..., np.newaxis] for x in [L, a, b]], axis=-1)


def rgb2xyz(rgb):
    arr = _prepare_colorarray(rgb).copy()
    mask = arr > 0.04045
    arr[mask] = np.power((arr[mask] + 0.055) / 1.055, 2.4)
    arr[~mask] /= 12.92
    return arr @ xyz_from_rgb.T.astype(arr.dtype)


def _prepare_lab_array(arr, force_copy=True):
    arr = np.asarray(arr)
    shape = arr.shape
    if shape[-1] < 3:
        raise ValueError("Input array has less than 3 color channels")
    if force_copy:
        arr = arr.copy()
    return arr


def _cart2polar_2pi(x, y):
    r, t = np.hypot(x, y), np.arctan2(y, x)
    t += np.where(t < 0.0, 2 * np.pi, 0)
    return r, t


def _prepare_colorarray(arr, force_copy=False):
    arr = np.asanyarray(arr)

    if arr.shape[-1] != 3:
        raise ValueError(
            "Input array must have a shape == (..., 3)), " f"got {arr.shape}"
        )

    if force_copy:
        arr = arr.copy()
    return arr


def get_xyz_coords():
    return np.asarray(illuminant, dtype=float)


def _convert(matrix, arr):
    return arr @ matrix.T.astype(arr.dtype)
