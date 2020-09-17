##
# Copyright 2020 University of Freiburg
#
# This file is part of the https://github.com/jotelha/JSC/tree/hfr13 fork of
# JSC's public easybuild repository (https://github.com/easybuilders/jsc)
##
"""
EasyBuild support for Tcl packages, implemented as an easyblock

@author: Johannes Hoermann (University of Freiburg)
"""
import os
import re

from easybuild.framework.easyblock import EasyBlock
from easybuild.framework.easyconfig import CUSTOM


# for distinguishing module syntax
from easybuild.tools.module_generator import ModuleGeneratorLua  # , ModuleGeneratorTcl

# regex and replacement pattern for customizing path separator in Lua module files
UPDATE_PATH_REGEX = '^(append|prepend)_path\("([^"]+)", (.*)\)$'
UPDATE_PATH_REPLACEMENT = r'\1_path("\2", \3, " ")'

class TclPackage(EasyBlock):
    """Easyblock for building and installing tcl packages."""

    @staticmethod
    def extra_options(extra_vars=None):
        """Extra easyconfig parameters specific to TclPackage."""
        extra_vars = EasyBlock.extra_options(extra=extra_vars)
        extra_vars.update({
            'tcllibpath': [None, "Plugin dirs to build", CUSTOM],
        })
        return extra_vars

    def make_module_extra(self):
        """
        Set TCLLIBPATH environment variable. Other than standard path variables,
        this list of paths is whitespace-separated."""

        txt = super(TclPackage, self).make_module_extra()

        if 'tcllibpath' in self.cfg and self.cfg['tcllibpath'] is not None:
            tcllibpath = self.cfg['tcllibpath']
            delim = ' '

            # module_generator.prepend_paths should have option for specifiying separator
            extra_txt = self.module_generator.prepend_paths('TCLLIBPATH', tcllibpath)
                        
            if isinstance(self.module_generator, ModuleGeneratorLua):
                p = re.compile(UPDATE_PATH_REGEX, re.MULTILINE)
                statements = [p.sub(UPDATE_PATH_REPLACEMENT, line) for line in extra_txt.splitlines()]
            else:
                # TODO: straight forward for Tcl modules as well
                NotImplementedError("Lua modules only.")
            
            statements.append('')
            txt += '\n'.join(statements)

        return txt
