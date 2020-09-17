##
# Copyright 2020 Univerity of Freiburg
#
# This file is part of the https://github.com/jotelha/JSC/tree/hfr13 fork of
# JSC's public easybuild repository (https://github.com/easybuilders/jsc)
#
"""
EasyBuild support for Tcl packages via standard 'configure/make/make install'
procedure, implemented as an easyblock.

@author: Johannes Hoermann (University of Freiburg)
"""
from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.easyblocks.generic.tclpackage import TclPackage


class ConfigureMakeTclPackage(ConfigureMake, TclPackage):
    """
    Build a Tcl package and module via standard 'configuge/make/install' procedure.
    """
    @staticmethod
    def extra_options(extra_vars=None):
        """Extra easyconfig parameters for Python packages being installed with python configure/make/make install."""
        extra_vars = TclPackage.extra_options(extra_vars=extra_vars)
        return ConfigureMake.extra_options(extra_vars=extra_vars)

    # def __init__(self, *args, **kwargs):
    #    """Initialize with PythonPackage."""
    #    super(ConfigureMakeTclPackage, self).__init__(self, *args, **kwargs)
