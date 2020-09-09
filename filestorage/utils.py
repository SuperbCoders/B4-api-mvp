import mimetypes
import subprocess
import tempfile
from uuid import uuid4

from filestorage import consts


class FileInfo:

    @staticmethod
    def get_data(file):
        data = {'type': '', 'sub_type': '', 'duration': None}
        mime, encoding = mimetypes.guess_type(file.path)

        if mime:
            data['type'], data['sub_type'] = mime.split('/')
        else:
            data['type'] = consts.OTHER

        if data['type'] in [consts.VIDEO, consts.AUDIO]:
            fh, temp_path = tempfile.mkstemp()
            with open(temp_path, "wb") as temp_file:
                temp_file.write(file.read())

            result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                     "format=duration", "-of",
                                     "default=noprint_wrappers=1:nokey=1", temp_path],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            data['duration'] = float(result.stdout)

        return data


def file_upload_to(instance, filename):
    *filenames, ext = filename.split('.')
    hex = uuid4().hex
    return '/'.join(['apifiles', hex[0], hex[1], hex[2], hex + '.' + ext])
