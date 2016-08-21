import os
from shutil import copyfile

import exifread
import logging

from config import IMAGE_SRC, IMAGE_TMP, IMAGE_SLICE_SIZE


class ImageParser:
    logger = logging.getLogger("ImageParser")

    def __init__(self):
        self._thumb = None
        self._slice_tot = 0
        self._slice_num = 0

    def load_new_thumb(self):
        self.logger.debug("Loading new image")

        ret = False

        if not os.path.isfile(IMAGE_SRC):
            self.logger.warn("No latest JPEG to load")
            return ret

        self._slice_tot = 0
        self._slice_num = 0

        self.logger.debug("Copying latest image to temp file")
        copyfile(IMAGE_SRC, IMAGE_TMP)

        image = open(IMAGE_TMP, mode="rb")

        exif = exifread.process_file(image)
        if "JPEGThumbnail" in exif.keys():
            self.logger.debug("Reading thumb")

            data = exif.get("JPEGThumbnail")
            stop = data.find("\xff\xd9") + 2
            self._thumb = data[:stop]
            self._slice_tot = (len(self._thumb) / IMAGE_SLICE_SIZE) + 1
            self._slice_num = 0

            ret = True

        image.close()

        self.logger.debug("Removing temp file")
        os.remove(IMAGE_TMP)

        return ret

    def thumb(self):
        self.logger.debug("Reading thumb slice")
        if self._thumb is None:
            if not self.load_new_thumb():
                return None

        start = self._slice_num * IMAGE_SLICE_SIZE
        stop = (self._slice_num + 1) * IMAGE_SLICE_SIZE
        data = self._thumb[start:stop]
        ret = (self._slice_tot, self._slice_num + 1, data)

        self._slice_num += 1
        if self._slice_num == self._slice_tot:
            self._thumb = None
            self._slice_tot = 0
            self._slice_num = 0

        return ret
