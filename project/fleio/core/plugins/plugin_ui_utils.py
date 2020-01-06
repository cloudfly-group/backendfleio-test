MAX_FILE_SIZE = 1024 * 1024  # allow max 1MB file size for UI components


class PluginUIUtils(object):
    @classmethod
    def read_file(cls, path: str):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read(MAX_FILE_SIZE)
