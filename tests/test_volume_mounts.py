from eck_lint.rules import ECKVolumeMountsRequired


def make_task(definition, module="kubernetes.core.k8s"):
    return {
        "action": {"__ansible_module__": module},
        "args": {"definition": definition},
    }


def test_non_k8s_module_returns_false():
    """Covers early exit when module is not k8s"""
    rule = ECKVolumeMountsRequired()

    task = make_task({}, module="copy")

    assert rule.matchtask(task) is False


def test_volumes_without_mounts_returns_true():
    """Covers failure case: volumes exist but no volumeMounts"""
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


def test_volumes_with_mounts_returns_false():
    """Covers success case: volumes exist and mounts are present"""
    rule = ECKVolumeMountsRequired()

    task = make_task({
        "spec": {
            "nodeSets": [{
                "podTemplate": {
                    "spec": {
                        "volumes": [{"name": "data"}],
                        "containers": [{
                            "name": "es",
                            "volumeMounts": [{"name": "data", "mountPath": "/data"}]
                        }]
                    }
                }
            }]
        }
    })

    assert rule.matchtask(task) is False