"""Auditor's independent recomputation of the primary 1G-E/1G-F variance at 8 h^-1 Mpc.

Model being checked (as stated in the successor Sec. 4 / frozen 1G-F Sec. 10):
  C1 clock, shell-crossing barrier, collapse delta_c, Boolean balls with the volume-weighted
  size shape of the excursion-set population, covered fraction = tracker f_v0, empty voids,
  wall field = linear field at growth D_wall compressed by s = D_wall (photon frame).
  sigma^2 = sigma_part^2 + sigma_int^2 (empty voids, mass-conserving weight 1).
Own implementations: size distribution from exact bin masses of the closed-form absorption
probability (indep_f.P_void), pair density P_R(r) = (3r^2/R^3)(1 - 3r/4R + r^3/16R^3), Boolean
xi_w = (1-f)^(-E_V[gamma~]) - 1, Simpson quadratures on dense grids (explicit sizes below).
"""
import json
import math
import sys

import numpy as np
from scipy.integrate import simpson

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import indep_f as F  # auditor's module (no project imports)

N_RL = 3000          # Lagrangian-radius bins (log) for the size distribution
RL_RANGE = (1e-4, 400.0)
N_R = 6001           # r nodes on [0, 2R] (Simpson)
N_K = 6001           # k nodes, x = kR in [1e-4, 400] (Simpson in ln k)
N_LNK_SIGMA = 2 ** 15


def sigma_grid(R, omega):
    """Vectorised sigma(R) per unit growth & unit A_s on a dense ln k grid (cross-checked vs quad)."""
    lnk = np.linspace(math.log(1e-7), math.log(5e4), N_LNK_SIGMA)
    k = np.exp(lnk)
    d2 = F.delta2_unit(k, omega)
    out = np.empty(len(R))
    for i0 in range(0, len(R), 200):
        RR = R[i0:i0 + 200, None]
        out[i0:i0 + 200] = np.sqrt(simpson(d2[None, :] * F.W_tophat(k[None, :] * RR) ** 2, x=lnk, axis=1))
    return out


def run(name, fv0, H0, out):
    tr = F.tracker(fv0, H0)
    gL = F.lcdm_growth_today(F.PL["Om"])
    anchor = F.PL["sigma8"] / (F.sigma_unit(8 / F.PL["h"], F.PL["omega_m"]) * gL)
    sc = F.shell_crossing_independent()
    dv, x = abs(sc["delta_v"]), sc["one_plus_delta_sc"]
    dc = 0.6 * (1.5 * math.pi) ** (2 / 3)
    D = tr["frame"](1.0)                      # C1 clock at t0 = D_wall
    h = tr["h"]
    # size distribution: exact masses between Lagrangian edges
    edges = np.geomspace(*RL_RANGE, N_RL + 1)
    sig_edges = anchor * D * sigma_grid(edges, tr["omega_eff"])
    # check the vectorised sigma against quad at 3 radii
    chk = [abs(anchor * D * F.sigma_unit(R, tr["omega_eff"]) / (anchor * D * sigma_grid(np.array([R]), tr["omega_eff"])[0]) - 1) for R in (0.01, 1.0, 30.0)]
    P = F.P_void(sig_edges ** 2, dv, dc)          # mass with R_L > edge
    m_bins = P[:-1] - P[1:]                        # mass in (edge_i, edge_{i+1})
    m_tot = dc / (dc + dv)
    RL_mid = np.sqrt(edges[:-1] * edges[1:])
    rho = D * x ** (-1 / 3) * RL_mid               # Eulerian void radius, photon-comoving Mpc
    pV = m_bins / m_tot                            # volume weights (constant x)
    R = 8.0 / h
    r = np.linspace(0.0, 2 * R, N_R)
    u = r[:, None] / rho[None, :]
    gt = np.where(u < 2, 1 - 0.75 * u + u ** 3 / 16, 0.0)
    EV = (gt * pV[None, :]).sum(axis=1)
    xi = (1 - fv0) ** (-EV) - 1
    PR = 3 * r ** 2 / R ** 3 * (1 - 0.75 * r / R + (r / R) ** 3 / 16)
    s2_part = simpson(PR * xi, x=r)
    norm_PR = simpson(PR, x=r)
    # sigma_int
    xk = np.geomspace(1e-4, 400.0, N_K)
    k = xk / R
    K = np.empty_like(k)
    wgt = PR * (1 + xi)
    for i0 in range(0, len(k), 500):
        kk = k[i0:i0 + 500, None]
        K[i0:i0 + 500] = simpson(wgt[None, :] * np.sinc(kk * r[None, :] / math.pi), x=r, axis=1)
    s = D
    d2E = F.delta2_unit(k * s, tr["omega_eff"]) * (anchor * D) ** 2
    s2_int = simpson(d2E * K, x=np.log(k))
    sig = math.sqrt(s2_part + s2_int)
    out[name] = dict(D_wall=D, h=h, omega_eff=tr["omega_eff"], m_resolved=float(m_bins.sum()), m_total=m_tot,
                     pair_density_norm=norm_PR, sigma_part=math.sqrt(s2_part), sigma_int=math.sqrt(s2_int),
                     sigma_total=sig, wall_share=s2_int / sig ** 2, sigma_vectorised_vs_quad=max(chk),
                     boolean_grain_volume_density=-math.log(1 - fv0),
                     grain_to_excursion_volume_ratio=-math.log(1 - fv0) / ((m_tot / x) / (1 - m_tot + m_tot / x)))


if __name__ == "__main__":
    res = {}
    for name, c in F.CASES.items():
        run(name, c["fv0"], c["H0"], res)
    print(json.dumps(res, indent=1))
    with open(sys.argv[1], "wb") as fh:
        fh.write((json.dumps(res, indent=1) + "\n").encode())
