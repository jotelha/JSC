##
# Copyright 2020 University of Freiburg
# Copyright 2009-2020 Ghent University
# Copyright 2015-2020 Stanford University
#
# This file is based on vmd.py, part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# https://github.com/easybuilders/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for VMD, implemented as an easyblock

@author: Johannes Hoermann (University of Freiburg)
@author: Stephane Thiell (Stanford University)
@author: Kenneth Hoste (HPC-UGent)
"""
import os

from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.tools.build_log import EasyBuildError
from easybuild.tools.run import run_cmd
from easybuild.tools.modules import get_software_root, get_software_version
import easybuild.tools.environment as env


class EB_VMD_minus_Plugins(ConfigureMake):
    """Easyblock for building and installing VMD-Plugins"""

    def __init__(self, *args, **kwargs):
        """Initialize VMD-specific variables."""
        super(EB_VMD_minus_Plugins, self).__init__(*args, **kwargs)


    def build_step(self):
        """Custom build step for VMD."""
        # make sure required dependencies are available
        deps = {}
        for dep in ['netCDF', 'Tcl']:
            deps[dep] = get_software_root(dep)
            if deps[dep] is None:
                raise EasyBuildError("Required dependency %s is missing", dep)

        # specify Tcl/Tk locations & libraries
        tclinc = os.path.join(deps['Tcl'], 'include')
        tcllib = os.path.join(deps['Tcl'], 'lib')
        env.setvar('TCL_INCLUDE_DIR', tclinc)
        env.setvar('TCL_LIBRARY_DIR', tcllib)

        tclshortver = '.'.join(get_software_version('Tcl').split('.')[:2])
        self.cfg.update('buildopts', 'TCLLDFLAGS="-ltcl%s"' % tclshortver)

        # Netcdf locations
        netcdfinc = os.path.join(deps['netCDF'], 'include')
        netcdflib = os.path.join(deps['netCDF'], 'lib')

        # compiler commands
        self.cfg.update('buildopts', 'CC="%s"' % os.getenv('CC'))
        self.cfg.update('buildopts', 'CCPP="%s"' % os.getenv('CXX'))

        cmd = ' '.join([
            'make',
            'LINUXAMD64',
            "TCLINC='-I%s'" % tclinc,
            "TCLLIB='-L%s'" % tcllib,
            "TCLLDFLAGS='-ltcl%s'" % tclshortver,
            "NETCDFINC='-I%s'" % netcdfinc,
            "NETCDFLIB='-L%s'" % netcdflib,
            self.cfg['buildopts'],
        ])
        run_cmd(cmd, log_all=True, simple=False)


    def install_step(self):
        """Custom build step for VMD-Plugins."""
        # create plugins distribution
        plugindir = self.installdir
        env.setvar('PLUGINDIR', plugindir)
        self.log.info("Generating VMD plugins in %s", plugindir)
        run_cmd("make distrib %s" % self.cfg['buildopts'], log_all=True, simple=False)
