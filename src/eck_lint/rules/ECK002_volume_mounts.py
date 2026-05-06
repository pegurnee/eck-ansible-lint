from ansiblelint.file_utils import Lintable
from ansiblelint.rules import AnsibleLintRule

class ECKVolumeMountsRequired(AnsibleLintRule):
    id = "ECK002"
    shortdesc = "Volumes must be mounted"
    severity = "HIGH"
    version_changed = "0.1.0"

    def matchtask(self, task):
        spec = task.get("spec", {})

        for ns in spec.get("nodeSets", []):
            pod = ns.get("podTemplate", {}).get("spec", {})
            volumes = pod.get("volumes", [])
            containers = pod.get("containers", [])

            if volumes:
                for c in containers:
                    if not c.get("volumeMounts"):
                        return True

        return False
