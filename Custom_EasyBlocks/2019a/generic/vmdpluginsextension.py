##
# Copyright 2020 University of Freiburg
# Copyright 2009-2020 Ghent University
# Copyright 2015-2020 Stanford University
#
# This file is part of the https://github.com/jotelha/JSC/tree/hfr13 fork of
# JSC's public easybuild repository (https://github.com/easybuilders/jsc).

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
import shutil

from easybuild.framework.easyconfig import CUSTOM
from easybuild.tools.build_log import EasyBuildError
from easybuild.tools.run import run_cmd
from easybuild.tools.modules import get_software_root, get_software_version
import easybuild.tools.environment as env

from easybuild.easyblocks.generic.configuremaketclpackage import ConfigureMakeTclPackage

# from Makefile snippet 'default_builddirs' via
#    cat default_builddirs | sed 's/\\//' | sed -E 's/^ +//' | xargs echo -n | tr ' ' '\n' | sed -E 's/^(.*)$/    "\1",/' > default_builddirs_formatted
DEFAULT_BUILD_DIRS = [
    "blast",
    "clustalw",
    "libbiokit",
    "multiseq",
    "multiseqdialog",
    "phylotree",
    "psipred",
    "seqdata",
    "seqedit",
    "stamp",
    "apbsrun",
    "alascanfep",
    "atomedit",
    "autoimd",
    "autoionize",
    "autopsf",
    "bdtk",
    "bendix",
    "bignum",
    "biocore",
    "bossconvert",
    "catdcd",
    "cgtools",
    "chirality",
    "cionize",
    "cispeptide",
    "cliptool",
    "clonerep",
    "colorscalebar",
    "contactmap",
    "dataimport",
    "demomaster",
    "dipwatch",
    "dowser",
    "exectool",
    "extendedpdb",
    "fftk",
    "gofrgui",
    "heatmapper",
    "hbonds",
    "hesstrans",
    "idatm",
    "ilstools",
    "imdmenu",
    "inorganicbuilder",
    "irspecgui",
    "mafft",
    "mdff",
    "membrane",
    "mergestructs",
    "molefacture",
    "moltoptools",
    "multimolanim",
    "multiplot",
    "multitext",
    "mutator",
    "namdenergy",
    "namdgui",
    "namdplot",
    "namdserver",
    "nanotube",
    "navfly",
    "navigate",
    "networkview",
    "nmwiz",
    "optimization",
    "palettetool",
    "paratool",
    "parsefep",
    "pbctools",
    "pdbtool",
    "plumed",
    "pmepot",
    "propka",
    "psfgen",
    "qmtool",
    "qwikmd",
    "ramaplot",
    "readcharmmpar",
    "readcharmmtop",
    "remote",
    "resptool",
    "rnaview",
    "rmsd",
    "rmsdtt",
    "rmsdvt",
    "ruler",
    "runante",
    "runsqm",
    "saltbr",
    "signalproc",
    "solvate",
    "ssrestraints",
    "stingtool",
    "structurecheck",
    "symmetrytool",
    "tablelist",
    "timeline",
    "topotools",
    "torsionplot",
    "trunctraj",
    "utilities",
    "vdna",
    "viewchangerender",
    "viewmaster",
    "volmapgui",
    "volutil",
    "vmddebug",
    "vmdlite",
    "vmdmovie",
    "vmdprefs",
    "vmdtkcon",
    "zoomseq",
]

class VMDPluginsExtension(ConfigureMakeTclPackage):
    """
    Easyblock for building and installing VMD-Plugins extensions
    (i.e. development versions of specific plugins) as modules.
    """

    @staticmethod
    def extra_options(extra_vars=None):
        """Extra easyconfig parameters specific to VMDPluginsExtension."""
        extra_vars = ConfigureMakeTclPackage.extra_options(extra_vars=extra_vars)
        extra_vars.update({
            'build_dirs': [DEFAULT_BUILD_DIRS, "Plugin dirs to build", CUSTOM],
        })
        return extra_vars

    def extract_step(self):
        """Custom extract step for VMDPluginsExtension."""
        super(VMDPluginsExtension, self).extract_step()

        # move all plugin build_dirs into plugin dir
        build_dirs = self.cfg['build_dirs']
        plugins_dir = 'plugins'
        for build_dir in build_dirs:
            self.log.info('Moving "%s" into "%s"', build_dir, plugins_dir)
            shutil.move(build_dir, plugins_dir)

    def build_step(self):
        """Custom build step for VMDPluginsExtension."""
        # make sure required dependencies are available
        deps = {}
        
        # NetCDF or Tcl not necessarily required, make optional
        for dep in ['netCDF', 'Tcl']:
            dep_root  = get_software_root(dep)
            if dep_root:
                deps[dep] = dep_root 

        build_dirs = ' '.join(self.cfg['build_dirs'])
        cmd = ' '.join([
            'make',
            "BUILDDIRS='%s'" % build_dirs,
            'LINUXAMD64',
        ])

        # specify Tcl/Tk locations & libraries
        if 'Tcl' in deps:
            tclinc = os.path.join(deps['Tcl'], 'include')
            tcllib = os.path.join(deps['Tcl'], 'lib')
            env.setvar('TCL_INCLUDE_DIR', tclinc)
            env.setvar('TCL_LIBRARY_DIR', tcllib)

            tclshortver = '.'.join(get_software_version('Tcl').split('.')[:2])
            self.cfg.update('buildopts', 'TCLLDFLAGS="-ltcl%s"' % tclshortver)

            cmd = ' '.join([
                cmd,
                "TCLINC='-I%s'" % tclinc,
                "TCLLIB='-L%s'" % tcllib,
                "TCLLDFLAGS='-ltcl%s'" % tclshortver,
            ])

        # Netcdf locations
        if 'netCDF' in deps:
            netcdfinc = os.path.join(deps['netCDF'], 'include')
            netcdflib = os.path.join(deps['netCDF'], 'lib')

            cmd = ' '.join([
                cmd,
                "NETCDFINC='-I%s'" % netcdfinc,
                "NETCDFLIB='-L%s'" % netcdflib,
            ])

        # compiler commands
        self.cfg.update('buildopts', 'CC="%s"' % os.getenv('CC'))
        self.cfg.update('buildopts', 'CCPP="%s"' % os.getenv('CXX'))

        cmd = ' '.join([
            cmd,
            self.cfg['buildopts'],
        ])

        run_cmd(cmd, log_all=True, simple=False)

    def install_step(self):
        """Custom build step for VMDPluginsExtension."""
        plugindir = self.installdir
        env.setvar('PLUGINDIR', plugindir)
        self.log.info("Generating VMD plugins in %s", plugindir)

        build_dirs = ' '.join(self.cfg['build_dirs'])
        cmd = ' '.join([
            'make',
            "BUILDDIRS='%s'" % build_dirs,
            "distrib",
            self.cfg['buildopts'],
        ])            
        run_cmd(cmd, log_all=True, simple=False)
