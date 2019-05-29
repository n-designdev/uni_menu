
"""
A Houdini engine for Tank.
"""

import os
import sys
import ctypes
import shutil
import time

import sgtk

import hou

class AppCommandsUI(object):
    """Base class for interface elements that trigger command actions."""

    def __init__(self, engine, commands):
        self._engine = engine
        self._commands = commands

    def _get_context_name(self):
        """Returns a display name for the current context"""

        # these objects don't persist across context switches, so we should
        # only need to construct the context name once. if the engine is
        # changed to not do a full restart on context switch, then this will
        # not be the case.
        if not hasattr(self, '_context_name'):
            self._context_name = str(self._engine.context)

        return self._context_name

    def _group_commands(self):
        """ This method provides a consistent method for organizing commands.

        Used by the menu and shelf classes to collect the registered commands
        into groups. The method returns a tuple with the first item being
        a list of context-specific commands, the second item is a dictionary
        of commands organized by the app name, and the third item is a list
        of favourite commands as defined in the settings.

        """

        # should only need to group them once. this object won't persist across
        # context switches. if the engine changes to not do a full restart on
        # context switch, then this will need to change.
        if not hasattr(self, '_grouped_commands'):

            favourite_cmds = []
            context_cmds = []
            cmds_by_app = {}

            # favourites
            for fav in self._engine.get_setting("menu_favourites"):
                app_instance_name = fav["app_instance"]
                menu_name = fav["name"]

                for cmd in self._commands:
                    if (cmd.get_app_instance_name() == app_instance_name and \
                        cmd.name == menu_name):
                        cmd.favourite = True
                        favourite_cmds.append(cmd)

            # this is how the original, static menu logic worked for grouping
            # commands in the Shotgun menu in houdini. it was moved here so
            # that it could be used by the dynamic menu in houdini 15+ as well
            # as the Shotgun shelf.  Basically, make a list of context-based
            # commands and a dictionary of app-specific commands organized by
            # app name.
            for cmd in self._commands:
                if cmd.get_type() == "context_menu":
                    context_cmds.append(cmd)
                else:
                    app_name = cmd.get_app_name()
                    if app_name is None:
                        app_name = "Other Items"
                    cmds_by_app.setdefault(app_name, []).append(cmd)

            self._engine.logger.debug("Grouped registered commands.")
            self._grouped_commands = (context_cmds, cmds_by_app, favourite_cmds)

        return self._grouped_commands

class AppCommandsShelf(AppCommandsUI):
    def __init__(self, engine, commands=None, name='Shotgun', label='Shotgun'):
        super(AppCommandsShelf, self).__init__(engine, commands)

        self._name = name
        self._label = label

    def create_shelf(self, shelf_file):

        import hou


        shelf_dir = os.path.dirname(shelf_file)
        if not os.path.exists(shelf_dir):
            os.makedirs(shelf_dir)
        
        root = ET.Element("shelfDocument")
        doc = ET.ElementTree(root)
        doc.write(shelf_file, encoding="UTF-8")

        shelf = hou.shelves.shelves().get(self._name, None)
        if shelf:
            # existing shelf. point it to the new shelf file for this session
            self._engine.logger.debug("Using existing shelf.")
            self._engine.logger.debug("  Setting shelf file: %s" % shelf_file)
            shelf.setFilePath(shelf_file)
        else:
            self._engine.logger.debug("Creating new shelf: %s" % self._name)
            shelf = hou.shelves.newShelf(
                file_path=shelf_file,
                name=self._name,
                label=self._label
            )

        shelf_tools = []
        cmds_by_app = {}

        (context_cmds, cmds_by_app, favourite_cmds) = self._group_commands()

        for cmd in context_cmds:
            tool = self.create_tool(shelf_file, cmd)
            shelf_tools.append(tool)

        for cmd in favourite_cmds:
            tool = self.create_tool(shelf_file, cmd)
            shelf_tools.append(tool)

        for app_name in sorted(cmds_by_app.keys()):
            for cmd in cmds_by_app[app_name]:
                if not cmd.favourite:
                    tool = self.create_tool(shelf_file, cmd)
                    shelf_tools.append(tool)

        shelf.setTools(shelf_tools)

ryuusei = AppcommandsShelf()

ryuusei.create_shelf('E:\temp\test.xml')