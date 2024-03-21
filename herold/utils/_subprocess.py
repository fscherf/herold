import subprocess
import shlex


def run(command, **kwargs):
    if not isinstance(command, list):
        command = shlex.split(command)

    try:
        return 0, subprocess.check_output(
            args=command,
            stderr=subprocess.DEVNULL,
            **kwargs,
        ).decode().splitlines()

    except subprocess.CalledProcessError as exception:
        return exception.returncode, []
