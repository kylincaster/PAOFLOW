#
# PAOFLOW
#
# Utility to construct and operate on Hamiltonians from the Projections of DFT wfc on Atomic Orbital bases (PAO)
#
# Copyright (C) 2016-2018 ERMES group (http://ermes.unt.edu, mbn@unt.edu)
#
# Reference:
# M. Buongiorno Nardelli, F. T. Cerasoli, M. Costa, S Curtarolo,R. De Gennaro, M. Fornari, L. Liyanage, A. Supka and H. Wang,
# PAOFLOW: A utility to construct and operate on ab initio Hamiltonians from the Projections of electronic wavefunctions on
# Atomic Orbital bases, including characterization of topological materials, Comp. Mat. Sci. vol. 143, 462 (2018).
#
# This file is distributed under the terms of the
# GNU General Public License. See the file `License'
# in the root directory of the present distribution,
# or http://www.gnu.org/copyleft/gpl.txt .
#

import numpy as np
from mpi4py import MPI
import scipy.optimize as sp

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

_FD_THRESHOLD = 1e-8

_FD_THRESHOLD_GAP = 1e-3


def _fd_criterion_gen(threshold):
  
  def _fd_criterion(x):

    return 1. / (np.exp(x) + 1.) - threshold

  return _fd_criterion


def FD(ene,mu,temp):
  
  _FD_XMAX = sp.newton(_fd_criterion_gen(_FD_THRESHOLD), 0.)
  if temp == 0.:
    dela = ene-mu
    nruter = np.where(dela < 0., 1., 0.)
    nruter[np.isclose(dela, 0.)] = .5
  else:
    x = (ene-mu) / temp
    nruter = np.where(x < 0., 1., 0.)
    indices = np.logical_and(x > -_FD_XMAX, x < _FD_XMAX)
    nruter[indices] = 1. / (np.exp(x[indices]) + 1.)
  return nruter

def calc_N(data_controller,ene,dos, mu, temp, dosweight=2.):

 if rank == 0:
  if temp == 0.: 
    occ = np.where(ene < mu, 1., 0.)
    occ[ene == mu] = .5
  else:
    occ = FD(ene, mu, temp)
  de = ene[1] - ene[0]
  return -dosweight * np.sum(dos * occ) * de

def solve_for_mu(data_controller,ene,dos,N0,temp,refine=True,try_center=True,dosweight=2.):
	  
  _FD_XMAX_GAP = sp.newton(_fd_criterion_gen(_FD_THRESHOLD_GAP), 0.)
  
  dela = np.empty_like(ene)
  for i, e in enumerate(ene):
    dela[i] = calc_N(data_controller,ene, dos, e, temp, dosweight) + N0
  dela = np.abs(dela)
  pos = dela.argmin()
  mu = ene[pos]
  center = False
  if dos[pos] == 0.:
    lpos = -1
    hpos = -1
    for i in range(pos, -1, -1):
      if dos[i] != 0.:
        lpos = i
        break
    for i in range(pos, dos.size):
      if dos[i] != 0.:
         hpos = i
         break
    if -1 in (lpos, hpos):
      raise ValueError("mu0 lies outside the range of band energies")
    hene = ene[hpos]
    lene = ene[lpos]
    if (try_center and min(hene-mu, mu - lene) >= _FD_XMAX_GAP * temp / 2.):
      pos = int(round(.5 * (lpos + hpos)))
      mu = ene[pos]
      center = True
  if refine:
    if center:
      mu = .5 * (lene + hene)
    else:
     if rank == 0:
      residual = calc_N(data_controller,ene, dos, mu, temp, dosweight) + N0
      if np.isclose(residual, 0):
        lpos = pos
        hpos = pos
      elif residual > 0:
        lpos = pos
        hpos = min(pos + 1, ene.size - 1)
      else:
        lpos = max(0, pos - 1)
        hpos = pos
      if hpos != lpos:
        lmu = ene[lpos]
        hmu = ene[hpos]

        def calc_abs_residual(muarg):
         if rank == 0:
          return abs(calc_N(data_controller,ene, dos, muarg, T, dosweight) + N0)

        result = sp.minimize_scalar(calc_abs_residual,bounds=(lmu, hmu),method="bounded")
        mu = result.x
  return mu
	
