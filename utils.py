from filters.players import PlayerIter, PlayerGenerator
from players.helpers import index_from_userid, index_from_playerinfo, playerinfo_from_index

from messages import SayText2
from messages import TextMsg
from commands import CommandReturn
from commands.client.manager import client_command_manager
from commands.server.manager import server_command_manager
from commands.say.manager import say_command_manager
from filters.errors import FilterError

from .colourizer import colourize, strip_colours

import collections


def target_filter(filterby, source=None, multitarget=True):
    """Processes a target string and resolves it to one or more players
    Args:
        filterby: A string filterby in the form of
                Name: "<playername>" ex: "necavi"
                Userid: "#<index>" ex: "#5"
                Multi-Filter: "@<filterby>" ex "@me"
        source: A player to consider the source, used for filters such as @me
    Returns:
        A list of players that fit the filterby string
    """
    playerlist = []
    if filterby == "":
        pass
    elif multitarget and filterby[0] == "@":
        if len(filterby) > 1 and filterby[1] == "!":
            if source is not None and len(filterby) > 2 and filterby[2:] == "me":
                source_index = source
                for index in PlayerIter():
                    if index != source_index:
                        playerlist.append(index)
            else:
                try:
                    playerlist = [x for x in PlayerIter(not_filters=filterby[2:], return_types="index")]
                except FilterError:
                    pass
        else:
            if source is not None and filterby[1:] == "me":
                playerlist.append(source)
            else:
                try:
                    playerlist = [x for x in PlayerIter(is_filters=filterby[1:], return_types="index")]
                except FilterError:
                    pass
    elif filterby[0] == "#":
        index = filterby[1:]
        if index.isnumeric():
            try:
                playerlist.append(index_from_userid(int(index)))
            except ValueError:
                pass
    else:
        for index in PlayerIter():
            playerinfo = playerinfo_from_index(index)
            filterby = filterby.casefold()
            if filterby in playerinfo.get_name().casefold():
                playerlist.append(index)
    return playerlist if multitarget else playerlist[0] if len(playerlist) == 1 else None


def message_server(message):
    print(strip_colours(message))


def message_client(index, message):
    SayText2(message=colourize(message)).send(index)

def message_all_clients(message):
    for index in PlayerIter("human"):
        message_client(index, message)

def message_console(index, message):
    TextMsg(message=strip_colours(message), destination=2).send(index)

def message_all_consoles(message):
    for index in PlayerIter("human"):
        message_console(index, message)

class CommandSourceProxy(object):
    def __init__(self, source,  index=None):
        self.source = source
        self.index = index

    def message(self, message):
        if self.source == "server":
            message_server(message)
        elif self.source == "console":
            message_console(self.index, message)
        elif self.source == "say":
            message_client(self.index, message)

command_list = []


class SayCommandProxy(object):
    def __init__(self, command):
        self.args = command.get_arg_string().strip("\"").split(" ")
        self.command = command

    def __getitem__(self, item):
        return self.args[item]

    def get_arg_count(self):
        return len(self.args)

    def get_arg_string(self):
        return " ".join(self.args[1:])

    def get_command_string(self):
        return " ".join(self.args)

    def get_arg(self, item):
        return self[item]

    def get_max_command_length(self):
        return self.command.get_max_command_length()


class Command(object):
    def __init__(self, names, *args, **kwargs):
        """Store the base values for the decorator."""
        self.names = names
        self.saynames = []
        if not isinstance(names, str) and isinstance(names, collections.Iterable):
            for name in self.names:
                self.saynames.append("." + name)
                self.saynames.append("/" + name)
        else:
            self.saynames.append("." + self.names)
            self.saynames.append("/" + self.names)
        self.args = args
        self.kwargs = kwargs

        command_list.append(self)

    def client_command_callback(self, player, command):
        return self.callback(CommandSourceProxy("console", index_from_playerinfo(player)), command)

    def server_command_callback(self, command):
        return self.callback(CommandSourceProxy("server"), command)

    def say_command_callback(self, player, teamonly, command):
        command = SayCommandProxy(command)
        silent = True if command.args[0].startswith("/") else False
        command.args[0] = command.args[0][1:]
        self.callback(CommandSourceProxy("say", index_from_playerinfo(player)), command)
        return CommandReturn.BLOCK if silent else CommandReturn.CONTINUE

    def __call__(self, callback):
        self.callback = callback
        client_command_manager.register_commands(self.names, self.client_command_callback, *self.args, **self.kwargs)
        server_command_manager.register_commands(self.names, self.server_command_callback, *self.args, **self.kwargs)
        say_command_manager.register_commands(self.saynames, self.say_command_callback, *self.args, **self.kwargs)
        return self

    def unload(self):
        client_command_manager.unregister_commands(self.names, self.client_command_callback)
        server_command_manager.unregister_commands(self.names, self.server_command_callback)
        say_command_manager.unregister_commands(self.saynames, self.say_command_callback)

def unload():
    for command in command_list:
        command.unload()
