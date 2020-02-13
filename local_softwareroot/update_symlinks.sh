#!/bin/bash
GLOBAL_UI_ROOT=${SOFTWAREROOT}/stages/${STAGE}/UI
LOCAL_SOFTWAREROOT=${PROJECT}/common/juwels/easybuild
LOCAL_UI_ROOT=${LOCAL_SOFTWAREROOT}/stages/${STAGE}/UI


GLOBAL_SYMLINKS=$(find ${GLOBAL_UI_ROOT} -type l)
GLOBAL_SYMLINK_TARGETS=$(find ${GLOBAL_UI_ROOT} -type l -exec readlink -f '{}' \;)

# echo "--- SYMLINKS ---"
# for symlink in ${GLOBAL_SYMLINKS}; do
#   echo ${symlink/${SOFTWAREROOT}/${LOCAL_SOFTWAREROOT}}
# done

# echo "--- SYMLINK TARGETS ---"
# for symlink_target in ${GLOBAL_SYMLINK_TARGETS}; do
#   printf %s "${symlink_target/${SOFTWAREROOT}/${LOCAL_SOFTWAREROOT}}"
# done

# delete current links
find ${LOCAL_UI_ROOT} -type l -delete

# recreate
paste -d ' ' <(printf %s "${GLOBAL_SYMLINK_TARGETS}") <(printf %s "${GLOBAL_SYMLINKS}") \
 | sed "s|${SOFTWAREROOT}|${LOCAL_SOFTWAREROOT}|g" | xargs -n 2 ln -sf
# echo "${!GLOBAL_SYMLINKS[@]}"
# for symlink_target
# echo $GLOBAL_SYMLINKS
