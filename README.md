# dtreq
[![PyPI](https://img.shields.io/pypi/v/dtreq.svg)]() [![license](https://img.shields.io/github/license/ketnipz/dtreq.svg)]()
dtreq is a Discord Webhook embed wrapper specifically designed for use with the [Twisted networking engine](https://twistedmatrix.com/trac/). It is based off of [kyb3r's dhooks](https://github.com/kyb3r/dhooks) wrapper and utilizes [treq](https://github.com/twisted/treq) for requests.

## Requirements

  - treq
  - twisted

## Usage
### Simple message
```py
from dtreq import Webhook

msg = Webhook(url, msg="Hello there! I'm a webhook")

def done(response):
    print(response.status)

def error(err):
    print(err)

msg.post().addCallback(done).addErrback(error)
```
### Advanced usage
```py
from dtreq import Webhook

url = 'WEBHOOK_URL'

embed = Webhook(url, color=123123)

embed.setAuthor(name='Author Goes Here', icon='https://i.imgur.com/rdm3W9t.png')
embed.setDesc('This is the **description** of the embed!')
embed.addField(name='Test Field',value='Value of the field')
embed.addField(name='Another Field',value='1234 😄')
embed.setThumbnail('https://i.imgur.com/rdm3W9t.png')
embed.setImage('https://i.imgur.com/f1LOr4q.png')
embed.setFooter(text='Here is my footer text',icon='https://i.imgur.com/rdm3W9t.png',ts=True)

def done(response):
    print(response.code)

def error(err):
    print(err)

embed.post().addCallback(done).addErrback(error)
```

## Installation
**dtreq** is available on the Python package index:
```
$ pip install dtreq
```
alternatively, you may clone the repository and import the module:
```
$ git clone https://github.com/ketnipz/dtreq 
```

```py
from dtreq import Webhook
```

## Credits
- [dhooks](https://github.com/kyb3r/dhooks) - Discord Webhook Embeds for Python

## Licence
MIT