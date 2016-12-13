#
# AFLOWpi_TB
#
# Utility to construct and operate on TB Hamiltonians from the projections of DFT wfc on the pseudoatomic orbital basis (PAO)
#
# Copyright (C) 2016 ERMES group (http://ermes.unt.edu)
# This file is distributed under the terms of the
# GNU General Public License. See the file `License'
# in the root directory of the present distribution,
# or http://www.gnu.org/copyleft/gpl.txt .
#
#
# References:
# Luis A. Agapito, Andrea Ferretti, Arrigo Calzolari, Stefano Curtarolo and Marco Buongiorno Nardelli,
# Effective and accurate representation of extended Bloch states on finite Hilbert spaces, Phys. Rev. B 88, 165127 (2013).
#
# Luis A. Agapito, Sohrab Ismail-Beigi, Stefano Curtarolo, Marco Fornari and Marco Buongiorno Nardelli,
# Accurate Tight-Binding Hamiltonian Matrices from Ab-Initio Calculations: Minimal Basis Sets, Phys. Rev. B 93, 035104 (2016).
#
# Luis A. Agapito, Marco Fornari, Davide Ceresoli, Andrea Ferretti, Stefano Curtarolo and Marco Buongiorno Nardelli,
# Accurate Tight-Binding Hamiltonians for 2D and Layered Materials, Phys. Rev. B 93, 125137 (2016).
#
# Pino D'Amico, Luis Agapito, Alessandra Catellani, Alice Ruini, Stefano Curtarolo, Marco Fornari, Marco Buongiorno Nardelli, 
# and Arrigo Calzolari, Accurate ab initio tight-binding Hamiltonians: Effective tools for electronic transport and 
# optical spectroscopy from first principles, Phys. Rev. B 94 165166 (2016).
# 

from scipy import fftpack as FFT
import numpy as np
import cmath
import sys

from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE

from write_velocity_eigs import write_velocity_eigs
#from kpnts_interpolation_mesh import *
from kpnts_interpolation_mesh import *
from do_non_ortho import *
from do_momentum import *
from load_balancing import *

# initialize parallel execution
comm=MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def do_velocity_calc(dHRaux,E_k,v_kp,R,ibrav,alat,a_vectors,b_vectors,dkres):
    # Compute bands on a selected path in the BZ
    # Define k-point mesh for bands interpolation
    kq = kpnts_interpolation_mesh(ibrav,alat,a_vectors,dkres)
    nkpi=kq.shape[1]
    for n in xrange(nkpi):
        kq[:,n]=kq[:,n].dot(b_vectors)

    # Load balancing
    ini_ik, end_ik = load_balancing(size,rank,nkpi)

    _,nawf,nawf,nktot,nspin = dHRaux.shape
    dHks  = np.zeros((3,nawf,nawf,nkpi,nspin),dtype=complex) # final data arrays
    Hks_aux  = np.zeros((3,nawf,nawf,nkpi,nspin),dtype=complex) # read data arrays from tasks

    Hks_aux[:,:,:,:,:] = band_loop_dH(ini_ik,end_ik,nspin,nawf,nkpi,dHRaux,kq,R)

    comm.Reduce(Hks_aux,dHks,op=MPI.SUM)

    # Compute momenta
    pks = np.zeros((nkpi,3,nawf,nawf,nspin),dtype=complex)
    for ik in xrange(nkpi):
        for ispin in xrange(nspin):
            for l in xrange(3):
                pks[ik,l,:,:,ispin] = np.conj(v_kp[ik,:,:,ispin].T).dot \
                            (dHks[l,:,:,ik,ispin]).dot(v_kp[ik,:,:,ispin])

    # Compute Berry curvature
    ########NOTE The indeces of the polarizations (x,y,z) should be changed according to the direction of the magnetization
    deltab = 0.05
    Om_znk = np.zeros((nkpi,nawf),dtype=float)
    Om_zk = np.zeros((nkpi),dtype=float)
    for ik in xrange(nkpi):
        for n in xrange(nawf):
            for m in xrange(nawf):
                if m!= n:
                    #Om_znk[ik,n] += -2.0*np.imag(pks[ik,2,n,m,0]*pks[ik,1,m,n,0]) / \
                    #((E_k[ik,m,0] - E_k[ik,n,0])**2 + deltab**2)
                    Om_znk[ik,n] += -2.0*np.imag(pks[ik,2,n,m,0]*pks[ik,1,m,n,0]-pks[ik,1,n,m,0]*pks[ik,2,m,n,0]) / \
                    ((E_k[ik,m,0] - E_k[ik,n,0])**2 + deltab**2)
        Om_zk[ik] = np.sum(Om_znk[ik,:]*(0.5 * (-np.sign(E_k[ik,:,0]) + 1)))  # T=0.0K

    if rank == 0:
        f=open('Omega_z'+'.dat','w')
        for ik in xrange(nkpi):
            f.write('%3d  %.5f \n' %(ik,-Om_zk[ik]))
        f.close()

    return(pks)

def band_loop_dH(ini_ik,end_ik,nspin,nawf,nkpi,dHRaux,kq,R):

    auxh = np.zeros((3,nawf,nawf,nkpi,nspin),dtype=complex)

    for ik in xrange(ini_ik,end_ik):
        for ispin in xrange(nspin):
            for l in xrange(3):
                auxh[l,:,:,ik,ispin] = np.sum(dHRaux[l,:,:,:,ispin]*np.exp(2.0*np.pi*kq[:,ik].dot(R[:,:].T)*1j),axis=2)

    return(auxh)
