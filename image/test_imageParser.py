from unittest import TestCase

from image.imageparser import ImageParser


class TestImageParser(TestCase):
    def test_image(self):
        parser = ImageParser()
        for i in range(55):
            print parser.thumb()
