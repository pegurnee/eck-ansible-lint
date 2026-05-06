from ansiblelint.rules import AnsibleLintRule

class ECKNoPlaintextSecrets(AnsibleLintRule):
    id = "ECK004"
    shortdesc = "Disallow plaintext secrets in env"
    severity = "HIGH"
    version_changed = "0.1.0"

    SENSITIVE_KEYS = ["PASSWORD", "SECRET", "TOKEN", "KEY"]

    def matchtask(self, task):
        spec = task.get("args", {}).get("definition", {}).get("spec", {})

        for ns in spec.get("nodeSets", []):
            containers = ns.get("podTemplate", {}).get("spec", {}).get("containers", [])
            for c in containers:
                for env in c.get("env", []):
                    name = env.get("name", "").upper()
                    if any(k in name for k in self.SENSITIVE_KEYS): 
                        if "value" in env: #TODO: check if hardcoded vs imported
                            return True

        return False