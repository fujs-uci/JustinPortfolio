class SectionItems:
    def __init__(self, img=None, text=None, link=None):
        self.img = img
        self.text = text
        self.link = link

    def __str__(self):
        return "({}, {}, {})".format(self.img, self.text, self.link)
