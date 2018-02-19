import json, time, datetime
from collections import defaultdict
from treq import post


class WebhookEmptyPayloadException(Exception):
    pass


class Webhook:
    def __init__(self, url, **kwargs):
        self.url = url
        self.msg = kwargs.get('msg')
        self.color = kwargs.get('color')
        self.title = kwargs.get('title')
        self.titleUrl = kwargs.get('title_url')
        self.author = kwargs.get('author')
        self.authorIcon = kwargs.get('author_icon')
        self.authorUrl = kwargs.get('author_url')
        self.desc = kwargs.get('desc')
        self.fields = kwargs.get('fields', [])
        self.image = kwargs.get('image')
        self.thumbnail = kwargs.get('thumbnail')
        self.footer = kwargs.get('footer')
        self.footerIcon = kwargs.get('footer_icon')
        self.ts = kwargs.get('ts')

    def addField(self, **kwargs):
        name = kwargs.get('name')
        value = kwargs.get('value')
        inline = kwargs.get('inline', True)

        field = {
            'name': name,
            'value': value,
            'inline': inline
        }

        self.fields.append(field)

    def setDesc(self, desc):
        self.desc = desc

    def setAuthor(self, **kwargs):
        self.author = kwargs.get('name')
        self.authorIcon = kwargs.get('icon')
        self.authorUrl = kwargs.get('url')

    def setTitle(self, **kwargs):
        self.title = kwargs.get('title')
        self.titleUrl = kwargs.get('url')

    def setThumbnail(self, url):
        self.thumbnail = url

    def setImage(self, url):
        self.image = url

    def setFooter(self, **kwargs):
        self.footer = kwargs.get('text')
        self.footerIcon = kwargs.get('icon')
        ts = kwargs.get('ts')
        self.ts = str(datetime.datetime.utcfromtimestamp(time.time() if ts else ts))

    def delField(self, index):
        self.fields.pop(index)

    @property
    def json(self, *arg):
        data = dict()

        data["embeds"] = []
        embed = defaultdict(dict)
        if self.msg: data["content"] = self.msg
        if self.author: embed["author"]["name"] = self.author
        if self.authorIcon: embed["author"]["icon_url"] = self.authorIcon
        if self.authorUrl: embed["author"]["url"] = self.authorUrl
        if self.color: embed["color"] = self.color
        if self.desc: embed["description"] = self.desc
        if self.title: embed["title"] = self.title
        if self.titleUrl: embed["url"] = self.titleUrl
        if self.image: embed["image"]['url'] = self.image
        if self.thumbnail: embed["thumbnail"]['url'] = self.thumbnail
        if self.footer: embed["footer"]['text'] = self.footer
        if self.footerIcon: embed['footer']['icon_url'] = self.footerIcon
        if self.ts: embed["timestamp"] = self.ts

        if self.fields:
            embed["fields"] = []
            for field in self.fields:
                f = dict()
                f["name"] = field['name']
                f["value"] = field['value']
                f["inline"] = field['inline']
                embed["fields"].append(f)

        data["embeds"].append(dict(embed))

        empty = all(not d for d in data["embeds"])

        if empty and 'content' not in data:
            raise WebhookEmptyPayloadException("You cannot send an empty payload")
        if empty: data['embeds'] = []

        return json.dumps(data, indent=4)

    def post(self):
        headers = {'Content-Type': 'application/json'}

        resultDeferred = post(self.url, data=self.json, headers=headers)
        return resultDeferred