WrexBot
=======

Simple Python IRC Bot written for fun.

The name comes from a Mass Effect players running joke, where characters Shepard
and Wrex would... well, a video is worth a thousand words:
http://www.youtube.com/watch?v=piD_mLWrEe0&hd=1

As you can guess, the bot was primarily written to imitate that behaviour
each time someone said either "Wrex" or "Shepard".

Installation
------------

TODO

The Shepard Machine
-------------------

```python
from wrex_bot import WrexBot

wrex_bot = WrexBot('BotName', '#channels', '#to', '#join')
wrex_bot.shepard('irc.server.address')
```
And from now whoever says "Wrex" or "Shepard" will never feel alone :)

Plugins
-------

TODO