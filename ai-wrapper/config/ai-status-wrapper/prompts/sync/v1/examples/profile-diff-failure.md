Example for an explicit missing-yq failure. Apply this example only when the current stderr explicitly says that `yq` is missing; otherwise ignore it and diagnose the current evidence:

Main issue: The profile-diff step cannot run because `yq` is not available.
Evidence: stderr reports `line 87: yq: command not found`, names `yq` as the required unavailable executable, and the status records exit code 127.
Most likely root cause: The image used by the failing step does not contain Mike Farah `yq` v4 on `PATH`.
Recommended fix: Rebuild that step image with a pinned `yq` v4 binary for the image's OS and CPU architecture, verify its checksum while building, and put it on `PATH`. Do not use an unqualified distro `yq` package. If the binary must be prepared by another Tekton step, write it to a workspace or shared volume mounted by both steps and add that mounted directory to the failing step's `PATH`; their image filesystems are isolated.
Follow-up checks: In the failing step image, run `yq --version`, confirm it reports v4, then rerun the profile diff.
