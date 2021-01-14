# Jülich Supercomputing Centre easyconfig repository

* This is the *PUBLIC* easybuild repository of JSC.
* This repository and its files are based on the upstream EasyBuild repository (https://github.com/easybuilders/easybuild-easyconfigs, https://github.com/easybuilders/easybuild-easyblocks and https://github.com/easybuilders/easybuild-framework), and heavily modified and extended to fit JSC's requirements.
* This repository is provided as-is. No compatibility with the upstream repository is guaranteed (actually it is almost guaranteed that you'll run into problems if you use it naïvely)
* To try to ensure that everything is working properly and avoiding collisions with the upstream easyconfigs, it is recommended to use the `--robot` and `--robot-paths` options, as set up in the `Developers/InstallSoftware-2017.lua` module. For more info take a look at http://easybuild.readthedocs.io/en/latest/Using_the_EasyBuild_command_line.html#controlling-the-robot-search-path
* All credits go to the original authors (and to the maintainers) of each file, be they JSC employees or otherwise.

This fork integrates easybuild configs in project hfr13

# Local (user/project) software stack modifications

Modeled analogous to global software stack at `/gpfs/software`
with the purpose to allow EasyBuild to find both global and local software,
building new software locally without rebuilding globally available software.

Within `$SOFTWAREROOT/stages/$STAGE`, 

* eb_repo contains EasyConfig files of all installed modules
* modules contains all module files
* software contains the actual builds
* UI contains symlinks, making software available in a flatter
  hierarchy from within the user interface

In order to use EasyBuild locally AND
emulate the global user interface as close as possible, we must
intitialize 'eb_repo', 'modules' and 'UI'
within `$LOCAL_SOFTWAREROOT/stages/$STAGE`
as clones of the global stage's originals,
where `$LOCAL_SOFTWAREROOT` is some subdirectory within `$PROJECT`, i.e.
`$PROJECT/commond/juwels/easybuild/stages/2019a`. Next, two bash snippets
help to apply necessary modifications:

* `update_symlinks.sh` creates user interface symlinks below the UI folder,
  reflecting gloabl stack
* `update_modulepaths.sh` changes all modifications to the `MODULEPATH` within 
  modulefiles to point to the local stack

Some compiler version entries below 'modules' do not meet the format as
expected by EasyBuild (what am I missing here?).
This issue can be aleviated by creating symbolic links manually, i.e. 
2019.3.199-GCC-8.3.0 -> 2019-GCC-8.3.0 wherever applicable.

`$LOCAL_SOFTWAREROOT/otherstages/Stages` needs modified stage module
files that point to local software stack.
Within this repository, `local_softwareroot` offers a template for the
directory hierarchy described above, including bash snippets
and modified stage module sample.

In order to install software within local stack, a
modified `InstallSoftware` module is required for setting
up easybuild parameters. 
`dev_modules/Developers/InstallSoftware-2019-hfr13-custom.lua`
contains the hfr13 customization.

To use the local software stack, a member may add

```bash
jutil env activate -p chfr13
module use $PROJECT/common/juwels/easybuild/otherstages
module load Stages/2019a
```

to their `.bashrc` (here for project chfr13).


# Progress of EasyConfig diet

Reducing custom EasyConfigs to minimal foss toolchains where possible.


* Golden_Repo/2019a/a/ASE/ASE-devel-iimpi-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/a/ASE/ASE-devel-mod-iimpi-2019a-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/a/ansible/ansible-2.9.6-intel-2019a-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/a/arrow/arrow-0.15.5-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/d/DOLFIN/DOLFIN-2019.1.0.post0-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/d/dijitso/dijitso-2019.1.0-intel-2019a-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/d/dill/dill-0.3.1.1-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/e/EasyBuild/EasyBuild-4.1.1.eb
* Golden_Repo/2019a/f/FFC/FFC-2019.1.0.post0-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/f/FIAT/FIAT-2019.1.0-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/f/FireWorks/FireWorks-1.9-intel-2019a-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/f/FireWorks/FireWorks-1.9.5-intel-2019a-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/f/FireWorks/FireWorks-1.9.5-mod-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/g/GC3Pie/GC3Pie-2.5.0-GCCcore-8.3.0.eb
* Golden_Repo/2019a/g/GROMACS-Top/GROMACS-Top-2019.1-jlh-intel-2019a.eb
* Golden_Repo/2019a/g/GROMACS-Top/GROMACS-Top-2019.3-jlh-intel-2019a.eb
* Golden_Repo/2019a/g/GromacsWrapper/GromacsWrapper-0.8.0-intel-2019a-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/h/hunter/hunter-3.1.3-intel-2019a-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/i/igraph/igraph-0.7.1-intel-2019a.eb
* Golden_Repo/2019a/i/igraph/igraph-0.8.0-intel-2019a.eb
* Golden_Repo/2019a/i/imteksimcs/imteksimcs-devel-intel-2019a-Python-3.6.8.eb
* DONE, possible conflicts: Golden_Repo/2019a/i/imteksimcs/imteksimcs-devel-local-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/i/imteksimfw/imteksimfw-0.1.0-intel-2019a-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/i/imteksimfw/imteksimfw-devel-intel-2019a-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/i/imteksimfw/imteksimfw-devel-local-intel-2019a-Python-3.6.8.eb
* DONE, possible issue with Intel-dependent scipy stack: Golden_Repo/2019a/i/imteksimpyenv/imteksimpyenv-devel-intel-2019a-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/j/jinja2-time/jinja2-time-0.2.0-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/l/LAMMPS/LAMMPS-24Jan2020-intel-2019a.eb
* Golden_Repo/2019a/l/libxdrfile/libxdrfile-1.1.4-iccifort-2019.3.199-GCC-8.3.0.eb
* Golden_Repo/2019a/m/MATIO/MATIO-1.5.12-iccifort-2019.3.199-GCC-8.3.0.eb
* Golden_Repo/2019a/m/matscipy/matscipy-devel-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/m/matscipy/matscipy-devel-mod-intel-2019a-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/m/mock-ssh-server/mock-ssh-server-0.8.1-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/p/PLUMED/PLUMED-2.5.3-intel-2019a.eb
* Golden_Repo/2019a/p/PLUMED/PLUMED-2.5.3-ld.gold.patch
* DONE: Golden_Repo/2019a/p/PLY/PLY-3.11-intel-2019a-Python-3.6.8.eb
* DONE, possible issue with Intel-dependent scipy stack: Golden_Repo/2019a/p/ParmEd/ParmEd-3.1.0-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/p/Pmw/Pmw-2.0.1-gcccoremkl-8.3.0-2019.3.199-Python-3.6.8.eb
* Golden_Repo/2019a/p/PyMOL/PyMOL-2.3.0-mod-gcccoremkl-8.3.0-2019.3.199-Python-3.6.8.eb
* Golden_Repo/2019a/p/PyYAML/PyYAML-5.1.2-GCCcore-8.3.0-Python-2.7.16.eb
* GCC 8.3.0: Golden_Repo/2019a/p/packmol/packmol-20.010-iccifort-2019.3.199-GCC-8.3.0.eb
* Golden_Repo/2019a/p/patch/patch-2.7.6-GCCcore-8.3.0.eb
* ALREADY GCCcore (rename?): Golden_Repo/2019a/p/pdb-tools/pdb-tools-2.0.1-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/p/pid/pid-3.0.0-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/p/pybind11/pybind11-2.2.3-intel-2019a-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/p/python-daemon/python-daemon-2.2.4-intel-2019a-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/p/python-igraph/python-igraph-0.7.1.post6-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/p/python-igraph/python-igraph-0.8.0-intel-2019a-Python-3.6.8.eb
* DONE: Golden_Repo/2019a/r/ruamel.yaml/ruamel.yaml-0.16.10-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/s/slepc4py/slepc4py-3.11.0-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/u/UFL/UFL-2019.1.0-intel-2019a-Python-3.6.8.eb
* Golden_Repo/2019a/v/VMD-Plugins/VMD-Plugins-1.9.3-intel-2019a.eb
* DONE: Golden_Repo/2019a/v/virtualenv/virtualenv-16.7.9-intel-2019a-Python-3.6.8.eb

# Possibly obsolete

Possible redundancies in need for recheck marked by (?).
```
A	Golden_Repo/2019a/a/ansible/ansible-2.9.6-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/a/arrow/arrow-0.15.5-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/a/asgiref/asgiref-3.3.1-intel-2019-Python-3.6.8.eb
A	Golden_Repo/2019a/c/click-plugins/click-plugins-1.1.1-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dill/dill-0.3.1.1-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dtool-lookup-api/dtool-lookup-api-0.1.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dtool-smb/dtool-smb-0.1.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dtool-smb/dtool-smb-devel-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dtool/dtool-3.25.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/e/EasyBuild/EasyBuild-4.1.1.eb
A	Golden_Repo/2019a/f/FireWorks/FireWorks-1.9.5-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/f/FireWorks/FireWorks-1.9.5-mod-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/f/FireWorks/FireWorks-1.9.6-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/f/FireWorks/FireWorks-1.9.6-mod-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/g/GC3Pie/GC3Pie-2.5.0-GCCcore-8.3.0.eb
? A	Golden_Repo/2019a/g/gsd/gsd-2.1.1-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/h/hunter/hunter-3.1.3-intel-2019a-Python-3.6.8.eb
? A	Golden_Repo/2019a/i/igraph/igraph-0.7.1-GCCcore-8.3.0.eb
? A	Golden_Repo/2019a/i/igraph/igraph-0.7.1-intel-2019a.eb
? A	Golden_Repo/2019a/i/igraph/igraph-0.8.0-intel-2019a.eb
A	Golden_Repo/2019a/i/imteksimfw/imteksimfw-devel-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/i/imteksimfw/imteksimfw-devel-local-intel-2019a-Python-3.6.8.eb
? A	Golden_Repo/2019a/i/imteksimpyenv/imteksimpyenv-devel-GCCcore-8.3.0-Python-3.6.8.eb
? A	Golden_Repo/2019a/i/imteksimpyenv/imteksimpyenv-devel-intel-2019a-Python-3.6.8.eb
? A	Golden_Repo/2019a/j/jinja2-time/jinja2-time-0.2.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/p/PLY/PLY-3.11-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/p/ParmEd/ParmEd-3.1.0-intel-2019a-Python-3.6.8.eb
? A	Golden_Repo/2019a/p/packmol/packmol-20.010-GCC-8.3.0.eb
? A	Golden_Repo/2019a/p/packmol/packmol-20.010-iccifort-2019.3.199-GCC-8.3.0.eb
A	Golden_Repo/2019a/p/parse/parse-1.15.0-intel-2019a-Python-3.6.8.eb
? A	Golden_Repo/2019a/p/pdb-tools/pdb-tools-2.0.1-Python-3.6.8.eb
? A	Golden_Repo/2019a/p/pdb-tools/pdb-tools-devel-mod-Python-3.6.8.eb
A	Golden_Repo/2019a/p/pid/pid-3.0.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/p/pysmb/pysmb-1.1.28-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/p/python-daemon/python-daemon-2.2.4-intel-2019a-Python-3.6.8.eb
? A	Golden_Repo/2019a/p/python-igraph/python-igraph-0.7.1.post6-GCCcore-8.3.0-Python-3.6.8.eb
? A	Golden_Repo/2019a/p/python-igraph/python-igraph-0.7.1.post6-intel-2019a-Python-3.6.8.eb
? A	Golden_Repo/2019a/p/python-igraph/python-igraph-0.8.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/r/ruamel.yaml/ruamel.yaml-0.16.10-intel-2019a-Python-3.6.8.eb
? A	Golden_Repo/2019a/s/sortedcontainers/sortedcontainers-2.1.0-intel-2019a-Python-3.6.8.eb
? A	Golden_Repo/2019a/v/virtualenv/virtualenv-16.7.9-GCCcore-8.3.0-Python-3.6.8.eb
? A	Golden_Repo/2019a/v/virtualenv/virtualenv-16.7.9-intel-2019a-Python-3.6.8.eb

# Extraction of custom EasyConfigs under conservation of directory tree

```
git checkout hfr13
git diff --name-status master Golden_Repo/ | awk '{ print $2 }' > diff
rsync -va --files-from=diff . $DESTINATION

git diff --name-status master Custom_EasyBlocks/ | awk '{ print $2 }' > diff
rsync -va --files-from=diff . $DESTINATION
```

# Custom EasyConfigs (diff to JSC/master, 2020/03/18)

```console
$ git diff --name-status master Golden_Repo/
A	Golden_Repo/2019a/a/ASE/ASE-devel-iimpi-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/a/ASE/ASE-devel-mod-iimpi-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/a/aiohttp/aiohttp-3.7.3-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/a/ansible/ansible-2.9.6-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/a/ansible/ansible-2.9.6-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/a/arrow/arrow-0.15.5-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/a/arrow/arrow-0.15.5-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/a/asgiref/asgiref-3.3.1-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/a/asgiref/asgiref-3.3.1-intel-2019-Python-3.6.8.eb
A	Golden_Repo/2019a/b/Biopython/Biopython-1.76-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/c/charmm2lammps/charmm2lammps-29Oct2020-GCCcore-8.3.0.eb
A	Golden_Repo/2019a/c/click-plugins/click-plugins-1.1.1-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/c/click-plugins/click-plugins-1.1.1-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/d/DOLFIN/DOLFIN-2019.1.0.post0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dijitso/dijitso-2019.1.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dill/dill-0.3.1.1-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dill/dill-0.3.1.1-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dtool-ecs/dtool-ecs-0.4.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dtool-lookup-api/dtool-lookup-api-0.1.0-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dtool-lookup-api/dtool-lookup-api-0.1.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dtool-lookup-client/dtool-lookup-client-devel-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dtool-smb/dtool-smb-0.1.0-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dtool-smb/dtool-smb-0.1.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dtool-smb/dtool-smb-devel-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dtool/dtool-3.25.0-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/d/dtool/dtool-3.25.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/e/EasyBuild/EasyBuild-4.1.1.eb
A	Golden_Repo/2019a/f/FFC/FFC-2019.1.0.post0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/f/FIAT/FIAT-2019.1.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/f/FireWorks/FireWorks-1.9.5-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/f/FireWorks/FireWorks-1.9.5-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/f/FireWorks/FireWorks-1.9.5-mod-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/f/FireWorks/FireWorks-1.9.5-mod-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/f/FireWorks/FireWorks-1.9.6-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/f/FireWorks/FireWorks-1.9.6-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/f/FireWorks/FireWorks-1.9.6-mod-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/f/FireWorks/FireWorks-1.9.6-mod-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/f/fwrlm/fwrlm-0.1.1-GCCCore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/g/GC3Pie/GC3Pie-2.5.0-GCCcore-8.3.0.eb
A	Golden_Repo/2019a/g/GROMACS-Top/GROMACS-Top-2019.1-jlh-intel-2019a.eb
A	Golden_Repo/2019a/g/GROMACS-Top/GROMACS-Top-2019.3-jlh-intel-2019a.eb
A	Golden_Repo/2019a/g/GromacsWrapper/GromacsWrapper-0.8.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/g/gsd/gsd-2.1.1-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/h/hunter/hunter-3.1.3-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/h/hunter/hunter-3.1.3-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/i/igraph/igraph-0.7.1-GCCcore-8.3.0.eb
A	Golden_Repo/2019a/i/igraph/igraph-0.7.1-intel-2019a.eb
A	Golden_Repo/2019a/i/igraph/igraph-0.8.0-intel-2019a.eb
A	Golden_Repo/2019a/i/imteksimcs/imteksimcs-devel-gpsmpi-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/i/imteksimcs/imteksimcs-devel-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/i/imteksimcs/imteksimcs-devel-local-gpsmpi-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/i/imteksimcs/imteksimcs-devel-local-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/i/imteksimfw/imteksimfw-0.1.2-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/i/imteksimfw/imteksimfw-0.1.3-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/i/imteksimfw/imteksimfw-0.1.4-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/i/imteksimfw/imteksimfw-0.1.5-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/i/imteksimfw/imteksimfw-devel-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/i/imteksimfw/imteksimfw-devel-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/i/imteksimfw/imteksimfw-devel-local-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/i/imteksimfw/imteksimfw-devel-local-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/i/imteksimpyenv/imteksimpyenv-devel-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/i/imteksimpyenv/imteksimpyenv-devel-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/j/jinja2-time/jinja2-time-0.2.0-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/j/jinja2-time/jinja2-time-0.2.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/j/joblib/joblib-0.14.1-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/l/LAMMPS/LAMMPS-24Jan2020-intel-2019a.eb
A	Golden_Repo/2019a/l/libxdrfile/libxdrfile-1.1.4-iccifort-2019.3.199-GCC-8.3.0.eb
A	Golden_Repo/2019a/m/MATIO/MATIO-1.5.12-iccifort-2019.3.199-GCC-8.3.0.eb
A	Golden_Repo/2019a/m/MDAnalysis/MDAnalysis-0.20.1-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/m/matscipy/matscipy-devel-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/m/matscipy/matscipy-devel-mod-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/m/mergetools/VMD-Plugins-1.9.3_Makefile.patch
A	Golden_Repo/2019a/m/mergetools/VMD-Plugins-1.9.3_make-arch.patch
A	Golden_Repo/2019a/m/mergetools/mergetools-0.1-GCCcore-8.3.0-Tcl-8.6.9.eb
A	Golden_Repo/2019a/m/mergetools/mergetools-0.2-GCCcore-8.3.0-Tcl-8.6.9.eb
A	Golden_Repo/2019a/m/mergetools/mergetools-devel-GCCcore-8.3.0-Tcl-8.6.9.eb
A	Golden_Repo/2019a/m/mmtf-python/mmtf-python-1.1.2-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/m/mock-ssh-server/mock-ssh-server-0.8.1-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/m/mock-ssh-server/mock-ssh-server-0.8.1-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/m/msgpack/msgpack-1.0.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/o/ovito/ovito-3.1.2-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/o/ovito/ovito-3.3.4-GCCcore-8.3.0-Python-3.6.8.eb
M	Golden_Repo/2019a/p/PLUMED/PLUMED-2.5.3-intel-2019a.eb
A	Golden_Repo/2019a/p/PLUMED/PLUMED-2.5.3-ld.gold.patch
A	Golden_Repo/2019a/p/PLY/PLY-3.11-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/p/PLY/PLY-3.11-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/p/ParmEd/ParmEd-3.1.0-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/p/ParmEd/ParmEd-3.1.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/p/Pmw/Pmw-2.0.1-gcccoremkl-8.3.0-2019.3.199-Python-3.6.8.eb
A	Golden_Repo/2019a/p/PyMOL/PyMOL-2.3.0-mod-gcccoremkl-8.3.0-2019.3.199-Python-3.6.8.eb
A	Golden_Repo/2019a/p/PySide2/PySide2-5.12.2-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/p/PySide2/PySide2-5.15.2-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/p/PyYAML/PyYAML-5.1.2-GCCcore-8.3.0-Python-2.7.16.eb
A	Golden_Repo/2019a/p/packmol/packmol-20.010-GCC-8.3.0.eb
A	Golden_Repo/2019a/p/packmol/packmol-20.010-iccifort-2019.3.199-GCC-8.3.0.eb
A	Golden_Repo/2019a/p/parse/parse-1.15.0-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/p/parse/parse-1.15.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/p/patch/patch-2.7.6-GCCcore-8.3.0.eb
A	Golden_Repo/2019a/p/pbctools/VMD-Plugins-1.9.3_Makefile.patch
A	Golden_Repo/2019a/p/pbctools/VMD-Plugins-1.9.3_make-arch.patch
A	Golden_Repo/2019a/p/pbctools/pbctools-devel-GCCcore-8.3.0-Tcl-8.6.9.eb
A	Golden_Repo/2019a/p/pbctools/pbctools-devel-mod-GCCcore-8.3.0-Tcl-8.6.9.eb
A	Golden_Repo/2019a/p/pdb-tools/pdb-tools-2.0.1-Python-3.6.8.eb
A	Golden_Repo/2019a/p/pdb-tools/pdb-tools-devel-mod-Python-3.6.8.eb
A	Golden_Repo/2019a/p/pid/pid-3.0.0-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/p/pid/pid-3.0.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/p/pybind11/pybind11-2.2.3-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/p/pysmb/pysmb-1.1.28-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/p/pysmb/pysmb-1.1.28-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/p/python-daemon/python-daemon-2.2.4-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/p/python-daemon/python-daemon-2.2.4-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/p/python-igraph/python-igraph-0.7.1.post6-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/p/python-igraph/python-igraph-0.7.1.post6-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/p/python-igraph/python-igraph-0.8.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/r/rlwrap/rlwrap-0.43-GCCcore-8.3.0.eb
A	Golden_Repo/2019a/r/ruamel.yaml/ruamel.yaml-0.16.10-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/r/ruamel.yaml/ruamel.yaml-0.16.10-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/s/slepc4py/slepc4py-3.11.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/s/sortedcontainers/sortedcontainers-2.1.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/t/tcllib/tcllib-1.20-GCCcore-8.3.0-Tcl-8.6.9.eb
A	Golden_Repo/2019a/t/topotools/VMD-Plugins-1.9.3_Makefile.patch
A	Golden_Repo/2019a/t/topotools/VMD-Plugins-1.9.3_make-arch.patch
A	Golden_Repo/2019a/t/topotools/topotools-1.8a-GCCcore-8.3.0-Tcl-8.6.9.eb
A	Golden_Repo/2019a/t/topotools/topotools-devel-GCCcore-8.3.0-Tcl-8.6.9.eb
A	Golden_Repo/2019a/u/UFL/UFL-2019.1.0-intel-2019a-Python-3.6.8.eb
A	Golden_Repo/2019a/v/VMD-Plugins/VMD-Plugins-1.9.3-intel-2019a-Tcl-8.6.9.eb
A	Golden_Repo/2019a/v/VMD-Plugins/VMD-Plugins-1.9.3_Makefile.patch
A	Golden_Repo/2019a/v/VMD-Plugins/VMD-Plugins-1.9.3_make-arch.patch
A	Golden_Repo/2019a/v/VMD/VMD-1.9.3-intel-2019a-Python-2.7.16-Tcl-8.6.9.eb
A	Golden_Repo/2019a/v/VMD/VMD-1.9.3_configure.patch
A	Golden_Repo/2019a/v/VMD/VMD-1.9.3_configure_plugindir.patch
A	Golden_Repo/2019a/v/VMD/VMD-1.9.3_plugins.patch
A	Golden_Repo/2019a/v/VMD/VMD-1.9.3_stride_MAX_AT_IN_RES.patch
A	Golden_Repo/2019a/v/VMD/VMD-1.9.3_stride_Makefile.patch
A	Golden_Repo/2019a/v/VMD/VMD-1.9.3_surf_Makefile.patch
A	Golden_Repo/2019a/v/VMD/VMD-1.9.3_surf_bad_printfs.patch
A	Golden_Repo/2019a/v/VMD/VMD-pluginless-text-1.9.3-intel-2019a-Python-2.7.16.eb
A	Golden_Repo/2019a/v/VMD/VMD-text-1.9.3-intel-2019a-Python-2.7.16-Tcl-8.6.9.eb
A	Golden_Repo/2019a/v/VMD/VMD-text-1.9.3.eb
A	Golden_Repo/2019a/v/virtualenv/virtualenv-16.7.9-GCCcore-8.3.0-Python-3.6.8.eb
A	Golden_Repo/2019a/v/virtualenv/virtualenv-16.7.9-intel-2019a-Python-3.6.8.eb
```
