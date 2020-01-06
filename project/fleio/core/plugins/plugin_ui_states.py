import logging
import os
from typing import Tuple

from fleio.core.plugins.plugin_ui_utils import PluginUIUtils


LOG = logging.getLogger(__name__)


class PluginUIStates(object):
    def __init__(self):
        self.frontend_files_path = None
        self.html_file_path = None
        self.js_file_path = None

    def initialize(
            self,
            frontend_files_path: str
    ):
        self.frontend_files_path = frontend_files_path
        self.js_file_path = os.path.join(
            self.frontend_files_path,
            'states.config.js'
        )

        return os.path.isfile(self.js_file_path)

    def get_javascript(self) -> Tuple[str, bool]:
        try:
            js = PluginUIUtils.read_file(path=self.js_file_path)
            return js, True
        except OSError:
            return '', False
