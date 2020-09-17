##
# Copyright 2020 Johannes Hoermann, University of Freiburg
# Copyright 2009-2020 Ghent University
#
# This file builds upon configuremake.py, part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# Flemish Research Foundation (FWO) (http://www.fwo.be/en)
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

##
"""
EasyBuild support for software that uses the GNU installation procedure,
i.e. configure/make/make install, but won't accept any --prefix option in its 
configure script, implemented as an easyblock.

@author: Johannes Hoermann (University of Freiburg)
@author: Stijn De Weirdt (Ghent University)
@author: Dries Verdegem (Ghent University)
@author: Kenneth Hoste (Ghent University)
@author: Pieter De Baets (Ghent University)
@author: Jens Timmerman (Ghent University)
@author: Toon Willems (Ghent University)
@author: Maxime Boissonneault (Compute Canada - Universite Laval)
@author: Alan O'Cais (Juelich Supercomputing Centre)
"""
import os

from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.easyblocks.generic.configuremake import AUTOCONF_GENERATED_MSG

from easybuild.tools.build_log import print_warning
from easybuild.tools.filetools import read_file
from easybuild.tools.run import run_cmd

DEFAULT_CONFIGURE_CMD = './configure'

class ConfigureMakeWithoutPrefix(ConfigureMake):
    """
    Support for building and installing applications with configure/make/make install,
    but without any --prefix option in the configure script. 
    """

    def configure_step(self, cmd_prefix=''):
        """
        Configure step
        - typically ./configure, without --prefix=/install/path style
        """

        if self.cfg.get('configure_cmd_prefix'):
            if cmd_prefix:
                tup = (cmd_prefix, self.cfg['configure_cmd_prefix'])
                self.log.debug("Specified cmd_prefix '%s' is overruled by configure_cmd_prefix '%s'" % tup)
            cmd_prefix = self.cfg['configure_cmd_prefix']

        if self.cfg.get('tar_config_opts'):
            # setting am_cv_prog_tar_ustar avoids that configure tries to figure out
            # which command should be used for tarring/untarring
            # am__tar and am__untar should be set to something decent (tar should work)
            tar_vars = {
                'am__tar': 'tar chf - "$$tardir"',
                'am__untar': 'tar xf -',
                'am_cv_prog_tar_ustar': 'easybuild_avoid_ustar_testing'
            }
            for (key, val) in tar_vars.items():
                self.cfg.update('preconfigopts', "%s='%s'" % (key, val))

        configure_command = cmd_prefix + (self.cfg.get('configure_cmd') or DEFAULT_CONFIGURE_CMD)

        # avoid using config.guess from an Autoconf generated package as it is frequently out of date;
        # use the version downloaded by EasyBuild instead, and provide the result to the configure command;
        # it is possible that the configure script is generated using preconfigopts...
        # if so, we're at the mercy of the gods
        build_type_option = ''
        host_type_option = ''

        # note: reading contents of 'configure' script in bytes mode,
        # to avoid problems when non-UTF-8 characters are included
        # see https://github.com/easybuilders/easybuild-easyblocks/pull/1817
        if os.path.exists(configure_command) and AUTOCONF_GENERATED_MSG in read_file(configure_command, mode='rb'):

            build_type = self.cfg.get('build_type')
            host_type = self.cfg.get('host_type')

            if build_type is None or host_type is None:

                # config.guess script may not be obtained yet despite the call in fetch_step,
                # for example when installing a Bundle component with ConfigureMake
                if self.config_guess is None:
                    self.config_guess = self.obtain_config_guess()

                if self.config_guess is None:
                    print_warning("No config.guess available, not setting '--build' option for configure step\n"
                                  "EasyBuild attempts to download a recent config.guess but seems to have failed!")
                else:
                    self.check_config_guess()
                    system_type, _ = run_cmd(self.config_guess, log_all=True)
                    system_type = system_type.strip()
                    self.log.info("%s returned a system type '%s'", self.config_guess, system_type)

                    if build_type is None:
                        build_type = system_type
                        self.log.info("Providing '%s' as value to --build option of configure script", build_type)

                    if host_type is None:
                        host_type = system_type
                        self.log.info("Providing '%s' as value to --host option of configure script", host_type)

            if build_type is not None and build_type:
                build_type_option = '--build=' + build_type

            if host_type is not None and host_type:
                host_type_option = '--host=' + host_type

        cmd = ' '.join([
            self.cfg['preconfigopts'],
            configure_command,
            build_type_option,
            host_type_option,
            self.cfg['configopts'],
        ])

        (out, _) = run_cmd(cmd, log_all=True, simple=False)

        return out
