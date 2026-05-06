from eck_lint.rules.ECK001_data_role import ECKRequireDataRole
from eck_lint.rules.ECK002_volume_mounts import ECKVolumeMountsRequired
from eck_lint.rules.ECK003_mount_paths import ECKMountPaths
from eck_lint.rules.ECK004_secrets import ECKNoPlaintextSecrets
from pathlib import Path

import yaml

def test_interview_yaml():
    PROJECT_DIR = Path(__file__).parent
    path = PROJECT_DIR / "./es.yaml"

    with open(path, 'r') as yamlFile:
        task = yaml.safe_load(yamlFile)

        assert ECKNoPlaintextSecrets().matchtask(task) is True
        assert ECKVolumeMountsRequired().matchtask(task) is True
        assert ECKRequireDataRole().matchtask(task) is True
        assert ECKMountPaths().matchtask(task) is True


if __name__ == "__main__":
    test_interview_yaml()