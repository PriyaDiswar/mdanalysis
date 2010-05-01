# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.40
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.
# This file is compatible with both classic and new-style classes.

"""

:Author:  Oliver Beckstein <orbeckst@gmail.com>
:Year:    2010
:Licence: GNU LESSER GENERAL PUBLIC LICENSE Version 3 (or higher)


:mod:`libxdrfile` --- the Gromacs xtc/trr library
=================================================

:mod:`libxdrfile` provides an interface to some high-level functions in the
Gromacs_ `XTC Library`_ version 1.1. Only functions required for reading and
processing whole trajectories are exposed at the moment; low-level routines to
read individual numbers are not provided.

The functions querying the numbers of atoms in a trajectory frame
(:func:`read_xtc_natoms` and func:`read_trr_natoms`) open a file themselves and
only require the file name.

All other functions operate on a *XDRFILE* object, which is a special file
handle for xdr files.  Any xdr-based trajectory file (xtc or trr format) always
has to be opened with :func:`xdrfile_open`. When done, close the trajectory
with :func:`xdrfile_close`.

The functions fill or read existing arrays of coordinates; they never allocate
these arrays themselves. Hence they need to be setup outside libxdrfile as
numpy arrays.


.. _Gromacs: http://www.gromacs.org
.. _XTC Library: http://www.gromacs.org/Developer_Zone/Programming_Guide/XTC_Library


Example: Reading from a xtc
---------------------------

In the example we read coordinate frames from an existing xtc trajectory::

  import numpy as np
  from libxdrfile import xdrfile_open, xdrfile_close, read_xtc_natoms, read_xtc, DIM, exdrOK
  xtc = 'md.xtc'
  
  # get number of atoms
  natoms = read_xtc_natoms(xtc)

  # allocate coordinate array of the right size and type
  # (the type float32 is crucial to match the underlying C-code!!)
  x = np.zeros((natoms, DIM), dtype=np.float32)
  # allocate unit cell box
  box = np.zeros((DIM, DIM), dtype=np.float32)

  # open file
  XTC = xdrfile_open(xtc, 'r')

  # loop through file until return status signifies end or a problem
  # (it should become exdrENDOFFILE on the last iteration)
  status = exdrOK
  while status == exdrOK:
     status,step,time,prec = read_xtc(XTC, box, x)
     # do something with x
     centre = x.mean(axis=0)
     print 'Centre of geometry at %(time)g ps: %(centre)r' % vars()

  # finally close file
  xdrfile_close(XTC)

Note that only the *contents* of the coordinate and unitcell arrays *x* and
*box* change.


Functions and constants
-----------------------

The module defines a number of constants such as :data:`DIM` or the
`Status symbols`_.

.. data:: DIM

          The number of cartesian dimensions for which the underlying C-code
          was compiled; this is most certainly 3.


Status symbols
~~~~~~~~~~~~~~

A number of symbols are exported; they all start with the letters
``exdr``. Important ones are listed here:

.. data:: exdrOK

          Success of xdr file read/write operation.

.. data:: exdrCLOSE
 
          xdr file is closed

.. data:: exdrENDOFFILE

          end of file was reached (response of :func:`read_xtc` and
          :func:`read_trr` after the last read frame)

.. data:: exdrFILENOTFOUND

          :func:`xdrfile_open` cannot find the requested file


Opening and closing of XDR files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two low-level functions are used to obtain a *XDRFILE* object (a file handle)
to access xdr files such as xtc or trr trajectories.

.. function:: xdrfile_open(path, mode) -> XDRFILE

              Open *path* and returns a *XDRFILE* handle that is required by other
              functions.

              :Arguments:
		  *path*
		     file name
		  *mode*
		     'r' for reading and 'w' for writing
	      :Returns: *XDRFILE* handle

.. function:: xdrfile_close(XDRFILE) -> status

              Close the xdrfile pointed to by *XDRFILE*. 

              .. Warning:: Closing an already closed file will lead to a 
                           crash with a double-free pointer error.

XTC functions
~~~~~~~~~~~~~

The XTC trajectory format is a lossy compression format that only stores
coordinates. Compression level is determined by the *precision* argument to the
:func:`write_xtc` function. Coordinates (Gromacs_ uses nm natively) are
multiplied by *precision* and truncated to the integer part. A typical value is
1000.0, which gives an accuracy of 1/100 of an Angstroem.

The advantage of XTC over TRR is its significantly reduced size.


.. function:: read_xtc_natoms(fn) -> natoms

              Read the number of atoms *natoms* from a xtc file *fn*.

              :Arguments:
                *fn*
                   file name of an xtc file

              :Raises: :exc:`IOError` if the supplied filed is not a XTC 
                       or if it is not readable.

.. function:: read_xtc(XDRFILE, box, x) -> (status, step, time, precision)

              Read the next frame from the opened xtc trajectory into *x*.

              :Arguments:
                *XDRFILE*
                   open *XDRFILE* object
                *box*
                   pre-allocated numpy ``array((DIM,DIM),dtype=numpy.float32)`` which
                   is filled with the unit cell box vectors
                *x*
                   pre-allocated numpy ``array((natoms, DIM),dtype=numpy.float32)``
                   which is updated with the coordinates from the frame

              :Returns: The function returns a tuple containing
                *status*
                   integer status (0 = exdrOK), see `Status symbols`_ for other
                   values)
                *step*
                   simulation step
                *time*
                   simulation time in ps
                *precision*
                   precision of the lossy xtc format (typically 1000.0)

.. function:: write_xtc(XDRFILE, step, time, box, x, prec) -> status

              Write the next frame *x* to the opened xtc trajectory.

              :Arguments:
                *XDRFILE*
                   open *XDRFILE* object (writable)
                *step*
                   simulation step
                *time*
                   time step in ps
                *box*
                   numpy ``array((DIM,DIM),dtype=numpy.float32)`` which contains 
                   the unit cell box vectors
                *x*
                   numpy ``array((natoms, DIM),dtype=nump.float32)``
                   which contains the coordinates from the frame
                *precision*
                   precision of the lossy xtc format (typically 1000.0)

              :Returns: *status*, integer status (0 = OK), see the ``libxdrfile.exdr*`` 
                        constants under `Status symbols`_ for other values)

TRR functions
~~~~~~~~~~~~~

TRR is the Gromacs_ native full-feature trajectory storage format. It can contain position 
coordinates, velocities and forces, and the lambda value for free energy perturbation 
calculations. Velocities and forces are optional in the sense that they can be all zero.

.. function:: read_trr_natoms(fn) -> natoms

              Read the number of atoms *natoms* from a trr file *fn*.

              :Arguments:
                *fn*
                   file name of a trr file

              :Raises: :exc:`IOError` if the supplied filed is not a TRR
                       or if it is not readable.

.. function:: read_trr(XDRFILE, box, x, v, f) -> (status, step, time, lambda)

              Read the next frame from the opened trr trajectory into *x*, *v*, and *f*.

              :Arguments:
                *XDRFILE*
                   open *XDRFILE* object
                *box*
                   pre-allocated numpy ``array((DIM,DIM),dtype=numpy.float32)`` which
                   is filled with the unit cell box vectors
                *x*
                   pre-allocated numpy ``array((natoms, DIM),dtype=nump.float32)``
                   which is updated with the **coordinates** from the frame
                *v*
                   pre-allocated numpy ``array((natoms, DIM),dtype=nump.float32)``
                   which is updated with the **velocities** from the frame
                *f*
                   pre-allocated numpy ``array((natoms, DIM),dtype=nump.float32)``
                   which is updated with the **forces** from the frame

              :Returns: The function returns a tuple containing
                *status*
                   integer status (0 = exdrOK), see the ``libxdrfile.exdr*`` constants 
                   under `Status symbols`_ for other values)
                *step*
                   simulation step
                *time*
                   simulation time in ps
                *lambda*
                   current lambda value (only interesting for free energy perturbation)

.. function:: write_trr(XDRFILE, step, time, lambda, box, x, v, f) -> status

              Write the next frame to the opened trr trajectory.

              :Arguments:
                *XDRFILE*
                   open *XDRFILE* object (writable)
                *step*
                   simulation step
                *time*
                   time step in ps
                *lambda*
                   free energy lambda value (typically 0.0)
                *box*
                   numpy ``array((DIM,DIM),dtype=numpy.float32)`` which contains 
                   the unit cell box vectors
                *x*
                   numpy ``array((natoms, DIM),dtype=nump.float32)``
                   which contains the **coordinates** from the frame
                *v*
                   numpy ``array((natoms, DIM),dtype=nump.float32)``
                   which contains the **velocities** from the frame
                *f*
                   numpy ``array((natoms, DIM),dtype=nump.float32)``
                   which contains the **forces** from the frame
 
              :Returns: *status*, integer status (0 = OK), see the ``libxdrfile.exdr*`` 
                        constants under `Status symbols`_ for other values)


"""

from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_libxdrfile', [dirname(__file__)])
        except ImportError:
            import _libxdrfile
            return _libxdrfile
        if fp is not None:
            try:
                _mod = imp.load_module('_libxdrfile', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _libxdrfile = swig_import_helper()
    del swig_import_helper
else:
    import _libxdrfile
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


exdrOK = _libxdrfile.exdrOK
exdrHEADER = _libxdrfile.exdrHEADER
exdrSTRING = _libxdrfile.exdrSTRING
exdrDOUBLE = _libxdrfile.exdrDOUBLE
exdrINT = _libxdrfile.exdrINT
exdrFLOAT = _libxdrfile.exdrFLOAT
exdrUINT = _libxdrfile.exdrUINT
exdr3DX = _libxdrfile.exdr3DX
exdrCLOSE = _libxdrfile.exdrCLOSE
exdrMAGIC = _libxdrfile.exdrMAGIC
exdrNOMEM = _libxdrfile.exdrNOMEM
exdrENDOFFILE = _libxdrfile.exdrENDOFFILE
exdrFILENOTFOUND = _libxdrfile.exdrFILENOTFOUND
exdrNR = _libxdrfile.exdrNR

def xdrfile_open(*args):
  """xdrfile_open(path, mode) -> XDRFILE"""
  return _libxdrfile.xdrfile_open(*args)

def xdrfile_close(*args):
  """xdrfile_close(fp) -> int"""
  return _libxdrfile.xdrfile_close(*args)

def read_xtc_natoms(*args):
  """read_xtc_natoms(fn) -> int"""
  return _libxdrfile.read_xtc_natoms(*args)

def read_trr_natoms(*args):
  """read_trr_natoms(fn) -> int"""
  return _libxdrfile.read_trr_natoms(*args)
DIM = _libxdrfile.DIM

def read_xtc(*args):
  """read_xtc(XDRFILE, box, x) -> (status, step, time, precision)"""
  return _libxdrfile.read_xtc(*args)

def read_trr(*args):
  """read_trr(XDRFILE, box, x, v, f) -> (status, step, time, lambda)"""
  return _libxdrfile.read_trr(*args)

def write_xtc(*args):
  """write_xtc(XDRFILE, step, time, box, x, prec) -> status"""
  return _libxdrfile.write_xtc(*args)

def write_trr(*args):
  """write_xtc(XDRFILE, step, time, lambda, box, x, v, f) -> status"""
  return _libxdrfile.write_trr(*args)


