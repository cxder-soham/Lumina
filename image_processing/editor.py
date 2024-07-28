from PIL import Image, ImageFilter, ImageEnhance


class ImageEditor:
    def __init__(self, image):
        self.image = image

    def crop(self, left, top, right, bottom):
        self.image = self.image.crop((left, top, right, bottom))

    def resize(self, width, height):
        self.image = self.image.resize((width, height))

    def rotate(self, degrees):
        self.image = self.image.rotate(degrees)

    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)

    def sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)

    def adjust_brightness(self, factor):
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(factor)

    def adjust_contrast(self, factor):
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(factor)

    def save(self, path):
        self.image.save(path)
