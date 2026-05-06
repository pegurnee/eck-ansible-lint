from ansiblelint.rules import AnsibleLintRule

class ECKRequireDataRole(AnsibleLintRule):
    id = "ECK001"
    shortdesc = "At least one node must have data role"
    severity = "HIGH"
    version_changed = "0.1.0"
    tags = ["kubernetes", "eck"]

    def matchtask(self, task):        
        node_sets = task.get("spec", {}).get("nodeSets", [])

        for ns in node_sets:
            roles = ns.get("config", {}).get("node.roles", [])
            if "data" in roles:
                return False

        return True