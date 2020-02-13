-- Get stage currently used
local old_stage = os.getenv("STAGE")
if old_stage == nil then
    old_stage = "current"
end

-- Get global software root
local softwareroot = os.getenv("SOFTWAREROOT")
if softwareroot == nil then
    local systemname = capture("cat /etc/FZJ/systemname")
    --Sanitize systemname
    systemname = string.gsub(systemname, "\n", "")
    if systemname == "" or systemname == nil then
        LmodError("Can't read the system name!")
    else
        softwareroot = pathJoin("/gpfs/software", systemname)
    end
end

-- Get local software root
local local_softwareroot = os.getenv("LOCAL_SOFTWAREROOT")
if local_softwareroot == nil then
    local systemname = capture("cat /etc/FZJ/systemname")
    --Sanitize systemname
    systemname = string.gsub(systemname, "\n", "")
    if systemname == "" or systemname == nil then
        LmodError("Can't read the system name!")
    else
        projectroot  = os.getenv("PROJECT_chfr13")
        local_softwareroot = pathJoin(projectroot, "common", systemname, "easybuild")
    end
end

-- Set new stage variables
local stage = myModuleVersion()
local stageroot = pathJoin(local_softwareroot, "stages")
local pkgroot = pathJoin(stageroot, stage)

-- Export these so we can use them in any derived modules
setenv("STAGE", stage)
setenv("SOFTWAREROOT", softwareroot)
setenv("LOCAL_SOFTWAREROOT", local_softwareroot)

-- Lmod messaging functions
help([[  This module will reset your module environment for the requested stage ( ]] .. stage .. [[ ) ]])

whatis([[  Module to set up the environment for requested stage ( ]] .. stage .. [[ )]])

if mode() == "load" then
    LmodMessage([[
        Preparing the environment for use of requested stage ( ]] .. stage .. [[ ).
    ]])
end

-- Unload GCCcore and binutils, loaded by StdEnv. The changes in the MODULEPATH trigger the reloading of StdEnv itself
unload("GCCcore", "binutils")

-- Let's tidy things up a little and remove everything Stage/UI related
local old_modulepath = os.getenv("MODULEPATH")
-- Sanitize old_modulepath
if old_modulepath == nil then
    old_modulepath = ""
end
for i in string.gmatch(old_modulepath, "([^:]+)") do
    if string.find(i, "/Stages/") or
        string.find(i, "/stages/") or
        string.find(i, "/UI/Compilers") or
        string.find(i, "/UI/Tools") or
        string.find(i, "/UI/Defaults")
        then
        remove_path("MODULEPATH", i)
    end
end

-- Give access to new stage
prepend_path("MODULEPATH", pathJoin(pkgroot, "UI/Compilers"))
prepend_path("MODULEPATH", pathJoin(pkgroot, "UI/Tools"))
prepend_path("MODULEPATH", pathJoin(pkgroot, "UI/Defaults"))

-- Make the module 'sticky' so it is hard to unload
add_property("lmod", "sticky")

-- Mark the module as Booster/KNL ready
--add_property("arch", "sandybridge:knl")
