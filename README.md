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


# Custom EasyConfigs (diff to JSC/master, 2020/03/12)

```console
$ git diff --name-status master Golden_Repo/
A       Golden_Repo/2019a/d/DOLFIN/DOLFIN-2019.1.0.post0-intel-2019a-Python-3.6.8.eb
A       Golden_Repo/2019a/d/dijitso/dijitso-2019.1.0-intel-2019a-Python-3.6.8.eb
A       Golden_Repo/2019a/e/EasyBuild/EasyBuild-4.1.1.eb
A       Golden_Repo/2019a/f/FFC/FFC-2019.1.0.post0-intel-2019a-Python-3.6.8.eb
A       Golden_Repo/2019a/f/FIAT/FIAT-2019.1.0-intel-2019a-Python-3.6.8.eb
A       Golden_Repo/2019a/g/GC3Pie/GC3Pie-2.5.0-GCCcore-8.3.0.eb
A       Golden_Repo/2019a/g/GROMACS-Top/GROMACS-Top-2019.1-jlh-intel-2019a.eb
A       Golden_Repo/2019a/g/GROMACS-Top/GROMACS-Top-2019.3-jlh-intel-2019a.eb
A       Golden_Repo/2019a/l/LAMMPS/LAMMPS-24Jan2020-intel-2019a.eb
A       Golden_Repo/2019a/l/libxdrfile/libxdrfile-1.1.4-iccifort-2019.3.199-GCC-8.3.0.eb
A       Golden_Repo/2019a/m/MATIO/MATIO-1.5.12-iccifort-2019.3.199-GCC-8.3.0.eb
A       Golden_Repo/2019a/m/matscipy/matscipy-devel-intel-2019a-Python-3.6.8.eb
M       Golden_Repo/2019a/p/PLUMED/PLUMED-2.5.3-intel-2019a.eb
A       Golden_Repo/2019a/p/PLUMED/PLUMED-2.5.3-ld.gold.patch
A       Golden_Repo/2019a/p/PLY/PLY-3.11-intel-2019a-Python-3.6.8.eb
A       Golden_Repo/2019a/p/PyYAML/PyYAML-5.1.2-GCCcore-8.3.0-Python-2.7.16.eb
A       Golden_Repo/2019a/p/packmol/packmol-20.010-iccifort-2019.3.199-GCC-8.3.0.eb
A       Golden_Repo/2019a/p/patch/patch-2.7.6-GCCcore-8.3.0.eb
A       Golden_Repo/2019a/p/pdb-tools/pdb-tools-2.0.1-Python-3.6.8.eb
A       Golden_Repo/2019a/p/pybind11/pybind11-2.2.3-intel-2019a-Python-3.6.8.eb
A       Golden_Repo/2019a/s/slepc4py/slepc4py-3.11.0-intel-2019a-Python-3.6.8.eb
A       Golden_Repo/2019a/u/UFL/UFL-2019.1.0-intel-2019a-Python-3.6.8.eb
A       Golden_Repo/2019a/v/VMD-Plugins/VMD-Plugins-1.9.3-intel-2019a.eb
A       Golden_Repo/2019a/v/virtualenv/virtualenv-16.7.9-intel-2019a-Python-3.6.8.eb
```
