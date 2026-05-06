from ansiblelint.rules import AnsibleLintRule

class ECKSnapshotRepoMount(AnsibleLintRule):
    id = "ECK003"
    shortdesc = "path.repo must have matching mountPath"
    severity = "HIGH"
    version_changed = "0.1.0"

    def matchtask(self, task):
        spec = task.get("args", {}).get("definition", {}).get("spec", {})

        for ns in spec.get("nodeSets", []):
            config = ns.get("config", {})
            repo_paths = config.get("path", {}).get("repo", [])

            if not repo_paths:
                continue

            containers = ns.get("podTemplate", {}).get("spec", {}).get("containers", [])
            for c in containers:
                mounts = [m.get("mountPath") for m in c.get("volumeMounts", [])]
                for path in repo_paths:
                    if path not in mounts:
                        return True

        return False