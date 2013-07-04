# -*- coding: utf-8 -*-
"""Plugin example.

Plugin filename and class name must follow the naming convention
defined in plugin_base.py.

"""

from plugin_base import PluginBase


class Example(PluginBase):
    """Plugin example.

    Plugin filename and class name must follow the naming convention
    defined in plugin_base.py.

    """
    def __init__(self, bot):
        """Overload PluginBase __init__ method.

        You have to call super() and then define the pairs ('command': function)
        the plugin will respond to, in the appropriate dictionaries.

        For example, this plugin will handle the received data if:
            * RFC command contains 'PING'.
            * custom_command in msg contains 'herp'.
            * custom_command in msg contains 'what' and sender is a bot admin.

        It will then call the function matching the command as follow:
            * RFC command -> function(sender, params, msg)
            * user_command -> function(sender, params, recipient)
            * admin_command -> function(sender, params, recipient)

        Where:
            * params is a list containing command parameters (if any).
            * recipient is either a channel if it's a channel message or
              equivalent to sender in case someone PM'ed the bot.

        The functions you'll call via the dictionaries should always have
        all the parameters even if they do not use them, else the dispatch
        will throw an exception.

        Then all you have to do is do your business -- and remember you can
        and should use self.bot.{whichever function defined in core.py}
        to interact with the bot and the server it is connected to.

        For more complex operations, you may even want to overload the dispatch
        function! An example can be found in admin.py.

        """
        super(Example, self).__init__(bot)
        self.commands = {'PING': self.ping}
        self.user_commands = {'herp': self.herp}
        self.admin_commands = {'what': self.what}

    def ping(sender, params, msg):
        """Called if RFC command contains 'PING'.

        All the parameters (sender, params, msg) should be present even if
        we do not use them.

        """
        # We are hipsters, we'll respond with a 'GNOP' instead of 'PONG'.
        print "I'm too edgy for you."
        self.bot.write('GNOP', msg)

    def herp(sender, params, recipient):
        """Called if custom_command in msg contains 'herp'.

        All the parameters (sender, params, recipient) should be present even if
        we do not use them.

        """
        self.bot.privmsg(recipient, 'Derp.')

    def what(sender, params, recipient):
        """Called if custom_command in msg contains 'what' and sender is a bot admin.

        All the parameters (sender, params, recipient) should be present even if
        we do not use them.

        """
        # Say "what" again! Say! "what"! again! I dare you!
        # I double-dare you, motherfucker! Say "what" one more goddamn time!
        answer = 'Say "what" again! Say! "what"! again!\n'
        answer += 'I dare you! I double-dare you, motherfucker!\n'
        answer += 'Say "what" one more goddamn time!\n'
        self.bot.privmsg(recipient, answer)