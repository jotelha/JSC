help([[
This module will load the environment you need to install new software with EasyBuild in a hierarchy.
]])

whatis("Module to set up the environment for development within EasyBuild")

-- Terminal colors
local red = "\027\[01;31m"
local yellow = "\027\[01;33m"
local green = "\027\[01;32m"
local normal = "\027\[0m"

-- Check first if "Stages" has been loaded. If not print a message and assert it with prereq
if mode()=="load" then
    if not isloaded("Stages") then
        LmodMessage(yellow.."You must have a stage loaded to set the build variables... "..normal)
    end
end

prereq("Stages")

-- Set local variables, taken from the environment
local software_root = os.getenv("SOFTWAREROOT")
local stage =  os.getenv("STAGE")
local is_devel = false
if string.find(stage, "Devel") or string.find(stage, "Stage1")  then
    is_devel = true
end
non_devel_stage = string.gsub(stage, 'Devel%-', "")

local global_stage_path = pathJoin(software_root, "stages", stage)
local global_repo_path  = pathJoin(global_stage_path, "eb_repo")
local project_root      = os.getenv("PROJECT")
-- Allow members of the software group to install *just* in the Devel stage
local user = capture("id -u -n")
-- Sanitize input
user = string.gsub(user, "\n", "")

local common_eb_path   = pathJoin(project_root, "common", "juwels", "easybuild")
local local_stage_path = pathJoin(common_eb_path, "stages", stage)
local local_repo_path  = pathJoin(local_stage_path, "eb_repo")
local user_eb_path     = pathJoin(project_root, user, "easybuild")
local user_jsc_eb_path = pathJoin(project_root, user, "git", "JSC")
local sources_path = pathJoin(user_eb_path, "sources")

local gr_path = pathJoin(user_jsc_eb_path, "Golden_Repo", non_devel_stage)
local custom_easyblocks_path = pathJoin(user_jsc_eb_path, "Custom_EasyBlocks", non_devel_stage)
local custom_toolchains_path = pathJoin(user_jsc_eb_path, "Custom_Toolchains", non_devel_stage)
local custom_mns_path = pathJoin(user_jsc_eb_path, "Custom_MNS", non_devel_stage)


io.stderr:write("software_root:     ",software_root,"\n")
io.stderr:write("stage:             ",stage,"\n")
io.stderr:write("non_devel_stage:   ",non_devel_stage,"\n")
io.stderr:write("global_stage_path: ",global_stage_path,"\n")
io.stderr:write("global_repo_path:  ",global_repo_path,"\n")
io.stderr:write("project_root:      ",project_root,"\n")
io.stderr:write("user:              ",user,"\n")
io.stderr:write("common_eb_path:    ",common_eb_path,"\n")
io.stderr:write("local_stage_path:  ",local_stage_path,"\n")
io.stderr:write("local_repo_path:   ",local_repo_path,"\n")
io.stderr:write("user_eb_path:      ",user_eb_path,"\n")
io.stderr:write("user_jsc_eb_path:  ",user_jsc_eb_path,"\n")
io.stderr:write("sources_path:      ",sources_path,"\n")
io.stderr:write("gr_path:           ",gr_path,"\n")

local contact = "johannes.hoermann@imtek.uni-freiburg.de"

-- Print header
if mode()=="load" then
    LmodMessage(green.."** LOADING DEVELOPER CONFIGURATION **"..normal.."\n"..
                "Preparing the environment for software installation via EasyBuild into stage "..stage.."\n"..
                "\n"..
                "  - Unloading preloaded modules \n"..
                "  - Adding our license servers to LM_LICENSE_FILE \n"..
                "  - Setting environment variables for group installations\n"..
                "    (EASYBUILD_SET_GID_BIT, EASYBUILD_STICKY_BIT, EASYBUILD_UMASK, EASYBUILD_GROUP_WRITABLE_INSTALLDIR)\n"..
                "  - Setting environment variable for where sources are stored\n"..
                "    (EASYBUILD_SOURCEPATH)\n"..
                "  - Setting environment variable for installation location\n"..
                "    (EASYBUILD_INSTALLPATH)\n"..
                "  - Setting environment variable for build location (EASYBUILD_BUILDPATH)\n"..
                "  - Giving priority to our custom Toolchains (EASYBUILD_INCLUDE_TOOLCHAINS)\n"..
                "  - Giving priority to our custom EasyBlocks (EASYBUILD_INCLUDE_EASYBLOCKS)\n"..
                "  - Storing all installed EasyConfigs in a unique repository\n"..
                "    (EASYBUILD_REPOSITORY, EASYBUILD_REPOSITORYPATH)\n"..
                "  - To keep module view clean, hiding some dependencies (GCCcore is made invisible with modulerc)\n"..
                "    (EASYBUILD_HIDE_DEPS)\n"..
                "  - Setting the robot path just to our golden repository\n"..
                "    (EASYBUILD_ROBOT)\n"..
                "  - Setting the filter to don't include irrelevant environment information in test reports\n"..
                "    (EASYBUILD_TEST_REPORT_ENV_FILTER)\n")
end

-- Unload some modules for convenience
unload("binutils")
unload("GCCcore")
unload("StdEnv")

-- EASYBUILD ENVIRONMENT

-- This should be set to only look in the golden repo. We need this here to prepend overlays if needed
-- setenv("EASYBUILD_ROBOT", gr_path)
setenv("EASYBUILD_ROBOT_PATHS", gr_path)

-- Fail if there are EB related modules loaded
setenv("EASYBUILD_DETECT_LOADED_MODULES", "error")
-- Whitelist GC3Pie and EasyBuild itself
setenv("EASYBUILD_ALLOW_LOADED_MODULES", "GC3Pie,EasyBuild")

-- Limit the number of threads
local nproc = capture("nproc")
-- Sanitize input
nproc = string.gsub(nproc, "\n", "")
if tonumber(nproc) > 64 then
    -- Limit the number of threads, to don't go crazy and use 256+
    local maxparallel = "64"
    pushenv("EASYBUILD_PARALLEL", maxparallel)
    if mode()=="load" then
        LmodMessage(yellow.."   - Setting EASYBUILD_PARALLEL to "..maxparallel..normal)
    end
end

-- Read systemname to know if we should prepend an overlay
local systemname = capture("cat /etc/FZJ/systemname")
--Sanitize systemname
systemname = string.gsub(systemname, "\n", "")

-- Set optarch options for easybuild
local architecture = os.getenv("ARCHITECTURE")
-- Booster
if architecture == "KNL" or systemname == "jurecabooster" then
    local opt="GCCcore:march=haswell -mtune=haswell;GCC:march=knl -mtune=knl -ftree-vectorize;Intel:xMIC-AVX512"
    if mode()=="load" then
        LmodMessage(yellow.."  - Setting EASYBUILD_OPTARCH to "..opt..normal)
    end
    pushenv("EASYBUILD_OPTARCH", opt)

    -- Prepend the overlay
    gr_overlay_path = pathJoin(gr_path, "knl_overlay")
    -- prepend_path("EASYBUILD_ROBOT", gr_overlay_path)
    prepend_path("EASYBUILD_ROBOT_PATHS", gr_overlay_path)
-- JUWELS
elseif systemname == "juwels" then
    local opt="GCCcore:march=haswell -mtune=haswell"
    if mode()=="load" then
        LmodMessage(yellow.."  - Setting EASYBUILD_OPTARCH to "..opt..normal)
    end
    pushenv("EASYBUILD_OPTARCH", opt)
    -- Prepend the overlay
    gr_overlay_path = pathJoin(gr_path, "juwels_overlay")
    -- prepend_path("EASYBUILD_ROBOT", gr_overlay_path)
    prepend_path("EASYBUILD_ROBOT_PATHS", gr_overlay_path)
    pushenv("EASYBUILD_PARALLEL", "40")
-- Juropa3
elseif architecture == "SandyBridge" then
    local opt="GCC:march=sandybridge -mtune=sandybridge;Intel:xAVX"
    if mode()=="load" then
        LmodMessage(yellow.."   - Setting EASYBUILD_OPTARCH to "..opt..normal)
    end
    pushenv("EASYBUILD_OPTARCH", opt)
-- Jureca
elseif architecture == "Haswell" then
    local opt="GCCcore:march=haswell -mtune=haswell;GCC:march=haswell -mtune=haswell;Intel:xCORE-AVX2"
    if mode()=="load" then
        LmodMessage(yellow.."   - Setting EASYBUILD_OPTARCH to "..opt..normal)
    end
    pushenv("EASYBUILD_OPTARCH", opt)
-- Default
else
    if mode()=="load" then
        LmodMessage("  - "..yellow.."No particular architecture loaded. Unsetting EASYBUILD_OPTARCH (if set)\n"..normal)
    end
    unsetenv("EASYBUILD_OPTARCH")
end

-- Add license servers. Done in 3 separate groups to avoid useless servers in the environment
-- We shuffle the servers too to distribute the load. Not that it matters a lot but....
prepend_path("INTEL_LICENSE_FILE", "1702@licsrv11.zam.kfa-juelich.de:".. -- Intel compilers
                                   "1702@licsrv12.zam.kfa-juelich.de:".. -- Intel compilers
                                   "1702@licsrv13.zam.kfa-juelich.de"   -- Intel compilers
            )
prepend_path("PGROUPD_LICENSE_FILE", "1706@licsrv12.zam.kfa-juelich.de:".. -- PGI compilers
                                     "1706@licsrv13.zam.kfa-juelich.de:".. -- PGI compilers
                                     "1706@licsrv11.zam.kfa-juelich.de"   -- PGI compilers
            )
prepend_path("LM_LICENSE_FILE", "1703@licsrv13.zam.kfa-juelich.de:".. -- TotalView debugger
                                "1703@licsrv11.zam.kfa-juelich.de:".. -- TotalView debugger
                                "1703@licsrv12.zam.kfa-juelich.de"    -- TotalView debugger
            )

-- Set up exactly where we put our installations
-- First: where are the sources stored/downloaded 
setenv("EASYBUILD_SOURCEPATH", sources_path)

-- Make sure that people build in a unique space so we avoid stepping on each others toes as much as possible
setenv("EASYBUILD_BUILDPATH", pathJoin("/dev/shm", user, architecture))

-- We add our custom Toolchains directory, it must be appended so as not to interfere with the EasyBuild installation
setenv("EASYBUILD_INCLUDE_TOOLCHAINS", pathJoin(custom_toolchains_path, "\*.py")..','..pathJoin(custom_toolchains_path, "fft", "\*.py")..','..pathJoin(custom_toolchains_path, "compiler", "\*.py"))

-- Finally we add our custom EasyBlock directory, it must be appended so as not to interfere with the EasyBuild installation
setenv("EASYBUILD_INCLUDE_EASYBLOCKS", pathJoin(custom_easyblocks_path, "\*.py")..","..
                                       pathJoin(custom_easyblocks_path, "generic", "\*.py"))

-- Store all installed EasyConfigs in a system-unique repository
setenv("EASYBUILD_REPOSITORY", "FileRepository")
setenv("EASYBUILD_REPOSITORYPATH", local_repo_path)

-- Always hide these dependencies to keep 'module avail' clean
local hidden_deps = ""
if isFile(gr_path.."/hidden_deps.txt") then
    hidden_deps = capture("tr '\n' ',' < "..gr_path.."/hidden_deps.txt")
end

setenv("EASYBUILD_HIDE_DEPS", hidden_deps)

setenv("EASYBUILD_HIDE_TOOLCHAINS", "GCCcore")

-- Managing permissions and expanding robot path
-- Setting variables to allow for a group install space
setenv("EASYBUILD_SET_GID_BIT", "1")

if is_devel and (isloaded("Stages/"..stage) or isloaded("Stages/Devel")) then
    if mode()=="load" then
        LmodMessage("  - Installing in Devel stage, therefore expanding dependency searching\n"..
                    "  - To allow collaboration in the development process, "..red.."all installations are\n"..
                    "    group-writable!"..normal.." (EASYBUILD_GROUP_WRITABLE_INSTALLDIR)")
    end
    -- Tell the robot where to search there when looking for missing dependencies
    -- append_path("EASYBUILD_ROBOT", global_repo_path)
    prepend_path("EASYBUILD_ROBOT_PATHS", global_repo_path)
    setenv("EASYBUILD_GROUP_WRITABLE_INSTALLDIR", "1")
    setenv("EASYBUILD_UMASK", "002")
    -- We need to allow people to clean out an installation in Devel
    setenv("EASYBUILD_STICKY_BIT", "0")
else
    -- The default is to have user-only write access to files/dirs
    setenv("EASYBUILD_UMASK", "022")

    setenv("EASYBUILD_STICKY_BIT", "1")
end

-- The following are details, no need to inform the installer.

-- Indicate that we (currently) use Lmod module tool and lua modules
setenv("EASYBUILD_MODULES_TOOL", "Lmod")
setenv("EASYBUILD_MODULE_SYNTAX", "Lua")

-- Set the prefix for EasyBuild
setenv("EASYBUILD_PREFIX", local_stage_path)

-- Second: where are the software and modules stored 
setenv("EASYBUILD_INSTALLPATH", local_stage_path)
setenv("EASYBUILD_INSTALLPATH_MODULES", pathJoin(local_stage_path, "modules"))
setenv("EASYBUILD_INSTALLPATH_SOFTWARE", pathJoin(local_stage_path, "software"))

-- Finally we tell EasyBuild to build hierarchical modules using our custom scheme
setenv("EASYBUILD_INCLUDE_MODULE_NAMING_SCHEMES", pathJoin(custom_mns_path, "\*.py"))
-- setenv("EASYBUILD_MODULE_NAMING_SCHEME", "FlexibleCustomHierarchicalMNS")
setenv("EASYBUILD_MODULE_NAMING_SCHEME", "CustomHierarchicalMNS")

-- Used a fixed installation subdir so that we can change naming schemes later if we want
setenv("EASYBUILD_FIXED_INSTALLDIR_NAMING_SCHEME", "1")

-- Let's make sure we are using minimal toolchains and experimental features
setenv("EASYBUILD_EXPERIMENTAL", "1")
-- This forces EB to do a bottom-top dependency resolution
setenv("EASYBUILD_MINIMAL_TOOLCHAINS", "1")
-- This tells EB to check first if there is a module available that matches any of the subtoolchains, and use it. If
-- multiple exist, the picked up one depends on the order of the paths in MODULEPATH (typically, toolchains higher in
-- the hierarchy will have "preference")
setenv("EASYBUILD_USE_EXISTING_MODULES", "1")

-- Filter for test reports
setenv("EASYBUILD_TEST_REPORT_ENV_FILTER", "\\*PS1\\*|PROMPT\\*|\\*LICENSE\\*")

-- Let's set things up to use the job submission system to install the software
if not isloaded("GC3Pie") then
    if mode()=="load" then
        LmodMessage(green..
                    "** CONFIGURING DIRECT SUBMISSION TO SLURM **\n"..normal..
                    "Configuring EasyBuild to allow submission of builds as jobs to the devel\n"..
                    "partition (using GC3Pie).\n"..
                    "  - "..yellow.."Loading latest GC3Pie module"..normal.."\n"..
                    "  - Submission configured for SLURM (EASYBUILD_JOB_BACKEND_CONFIG)\n"..
                    "  - Telling EasyBuild to use 32 cores and 1 hour time limit\n"..
                    "    (EASYBUILD_JOB_CORES, EASYBUILD_JOB_MAX_WALLTIME)\n"..
                    yellow.."To access this feature you must add the argument --job to your eb command.\n"..normal..
                    "Please note that execution nodes are *not* connected to the internet so\n"..
                    "software that requires internet access will not build on the back-end.")
    end
--    load("GC3Pie")
    setenv("EASYBUILD_JOB_BACKEND", "GC3Pie")
    -- The backend are regular nodes. We have to be careful, some packages might need to be compiled on KNL nodes
    setenv("EASYBUILD_JOB_BACKEND_CONFIG", "/usr/local/software/FZJ/gc3pie.cfg")
    setenv("EASYBUILD_JOB_CORES", "48")
    setenv("EASYBUILD_JOB_MAX_WALLTIME", "1")
end

-- If not loaded, load the default EasyBuild module
if not isloaded("EasyBuild") then
    if mode()=="load" then
        LmodMessage("  - Loading default (typically latest) EasyBuild module")
    end
    load("EasyBuild")
    -- Enable bash completion in bash
    local shell = capture("echo $SHELL | xargs basename")
    -- Sanitize input
    shell = string.gsub(shell, "\n", "")
end

-- Let's repeat where we're installing if they've chosen one of the soft-linked Stages
if mode()=="load" then
    if not is_devel then
        LmodMessage("\n"..red.."Warning! You are installing software into a production stage. This\n"..
                    "should typically only be done (rarely!) for bug fixes and verified builds.\n"..normal)
    else
        LmodMessage("You are installing software in the development stage, this is a testing area and\n"..
                    "(group writable) collaboration space to create and verify a build.")
    end
end
