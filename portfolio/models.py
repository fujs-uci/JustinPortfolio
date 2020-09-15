from django.db import models
from .utils import SectionItems
import json


class SocialMedia(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(max_length=300)
    link = models.CharField(max_length=300)
    alt = models.CharField(max_length=50, default="This")

    def img(self):
        return str(self.image)

    class Meta:
        db_table = "portfolio_social_media"
        verbose_name_plural = "Social Media"

    def __str__(self):
        return self.alt

    @property
    def image_url(self):
        return "portfolio/img/{}".format(self.image.url)


class Section(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    layout = models.ForeignKey('Layout', on_delete=models.SET_NULL, null=True)
    data = models.TextField(default="{}")
    styles = models.TextField(default='{"style":[]}')
    menu = models.BooleanField(default=True)
    home = models.BooleanField(default=True)
    link = models.CharField(max_length=100, default="#")
    order = models.IntegerField(default=0)

    # data keys refer to hard coded names in layout
    # data values refer to textbody or imagefile ids
    # data structure depends on layout.data

    class Meta:
        db_table = "portfolio_section"
        verbose_name = "Section"

    def __str__(self):
        return self.name

    @property
    def get_link(self):
        if self.home and self.menu and self.link == "#":
            self.link = "#{}".format(self.name)
            self.save()
        return self.link

    @property
    def get_styles(self):
        styles = json.loads(self.styles)
        return " ".join(styles.get("style"))

    def set_data_keys(self):
        if self.layout:
            self.data = self.layout.get_data()
            self.save()
            return True
        return False

    def get_data(self):
        for i, j in json.loads(self.data).items():

            if 'img' in i and j != "":
                item = ImageFile.objects.filter(id=int(j)).first()
            elif 'text' in i and j != "":
                item = TextBody.objects.filter(id=int(j)).first()
            elif 'link' in i and j != "":
                item = Page.objects.filter(id=int(j)).first()
            else:
                item = None
            setattr(self, i, item)

    @property
    def view_all(self):
        show_view_all = False
        for i, j in json.loads(self.data).items():
            attr_name, attr_num = i.split("_")
            if int(attr_num) == 3:
                show_view_all = True
                break
        return show_view_all

    @property
    def items(self):
        count = 1
        attr_temp = {}
        attr_list = []
        for i, j in json.loads(self.data).items():
            attr_name, attr_num = i.split("_")

            if count == 4:
                break

            if int(attr_num) != count:
                attr_list.append(SectionItems(img=attr_temp.get('img'),
                                              text=attr_temp.get('text'),
                                              link=attr_temp.get('link')))
                attr_temp = dict()
                count += 1

            if 'img' in attr_name and j != "":
                item = ImageFile.objects.filter(id=int(j)).first()
                attr_temp[attr_name] = item
            elif 'text' in attr_name and j != "":
                item = TextBody.objects.filter(id=int(j)).first()
                attr_temp[attr_name] = item
            elif 'link' in attr_name and j != "":
                item = Page.objects.filter(id=int(j)).first()
                attr_temp[attr_name] = item

        if attr_temp:
            attr_list.append(SectionItems(img=attr_temp.get('img'),
                                          text=attr_temp.get('text'),
                                          link=attr_temp.get('link')))
        return attr_list


class TextBody(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    section = models.ForeignKey('Section', on_delete=models.CASCADE)

    class Meta:
        db_table = "portfolio_text_body"
        verbose_name = "Text Body"

    def __str__(self):
        return self.text


class ImageFile(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(max_length=300)
    image_resize = models.ImageField(max_length=300, default=None, null=True, blank=True)
    section = models.ForeignKey('Section', on_delete=models.CASCADE)

    class Meta:
        db_table = "portfolio_image_file"
        verbose_name = "Image File"

    def __str__(self):
        return str(self.image)

    @property
    def image_url(self):
        return "portfolio/img/{}".format(self.image.url)


class Layout(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(default="", max_length=100)
    template = models.CharField(max_length=1000)
    data = models.TextField(default="")

    class Meta:
        db_table = "portfolio_layout"
        verbose_name = "Layout"

    # Data is a dict that controls where the images and texts belong
    # depending on the layout, the data will be organized differently
    # users will fill out the data dict to organize the content in the layout

    # the keys of the data determine the position of text/images in the layout
    # the values will be determined by the user

    # eventually the user will be able to create the layout and set the keys
    def __str__(self):
        return self.name

    def set_data(self, data):
        self.data = json.dumps(data)
        self.save()
        return True

    def get_data(self):
        return json.loads(self.data)


class Page(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    data = models.TextField(default="{}")
    layout = models.ForeignKey('Layout', on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        db_table = "portfolio_page"
        verbose_name = "Page"

    def __str__(self):
        return self.name

    @staticmethod
    def url_to_name(url_name):
        return " ".join(url_name.split("-"))

    @property
    def name_url(self):
        return "-".join(self.name.split(" "))

    def set_data_keys(self):
        if self.layout:
            self.data = self.layout.get_data()
            self.save()
            return True
        return False

    def get_data(self):
        for i, j in json.loads(self.data).items():

            if 'img' in i and j != "":
                item = ImageFile.objects.filter(id=int(j)).first()
            elif 'text' in i and j != "":
                item = TextBody.objects.filter(id=int(j)).first()
            elif 'link' in i and j != "":
                item = Page.objects.filter(id=int(j)).first()
            else:
                item = None
            setattr(self, i, item)

