"""
Sentinel Hub configuration
"""
import os

from sentinelhub import SHConfig


class sentinelhub_config:
    """Sentinel Hub Configuration file"""

    def __init__(self, log: isinstance = None) -> None:
        r"""Defining variables

        Args:\n
            log: custom logger ini file.
        """
        self.log = log

    def save(self, instance_id: str = "open-cosmos"):
        r"""Save the instance ID

        Args:\n
            instance_id: Provide an instance name
        """
        try:
            home_folder = os.path.expanduser("~")
            config_file = os.path.join(home_folder, ".config/sentinelhub/config.toml")
            assert os.path.exists(config_file)
        except AssertionError:
            self.log.error("Sentinel Hub config file does not exist")
            self.log.info("Run the following commands in the command terminal")
            self.log.info("sentinelhub.config --show")
        else:
            sh_client_id = os.environ["SH_CLIENT_ID"]
            sh_client_secret = os.environ["SH_CLIENT_SECRET"]

            try:
                assert instance_id is not None
                assert sh_client_id is not None
                assert sh_client_secret is not None
            except AssertionError:
                self.log.debug("Make sure to add an Instance ID")
                self.log.debug("Make sure to add Sentinel OAuth IDs to the env variables")
            else:
                self.config = SHConfig()
                self.config.instance_id = instance_id
                self.config.sh_client_id = sh_client_id
                self.config.sh_client_secret = sh_client_secret
                self.config.save("open-cosmos-profile")
                return self.config
