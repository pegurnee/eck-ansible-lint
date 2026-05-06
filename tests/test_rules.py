from eck_lint.rules import ECKVolumeMountsRequired

def make_task(definition):
    return {
        "action": {"__ansible_module__": "kubernetes.core.k8s"},
        "args": {"definition": definition},
    }

def test_missing_mounts_fails():
    rule = ECKVolumeMountsRequired()

    task = make_task({
        "spec": {
            "nodeSets": [{
                "podTemplate": {
                    "spec": {
                        "volumes": [{"name": "data"}],
                        "containers": [{"name": "es"}]
                    }
                }
            }]
        }
    })

    assert rule.matchtask(task) is True
