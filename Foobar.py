#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Plugin para Sublime Text 3"

__author__ = "Jorge Alberto Cricelli (jacricelli@gmail.com)"
__license__ = "MIT"

import os
import sublime
import sublime_plugin
import subprocess

# http://larsnordeide.com/2013/improve-sublime-text-2-part-1.html
class ResetFontSizeToUserDefaultsCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        preferences = sublime.load_settings('Preferences.sublime-settings')
        settings = sublime.load_settings('Foobar.sublime-settings')

        if not settings.has('default_font_size'):
            settings.set('default_font_size', 11)
            sublime.save_settings('Foobar.sublime-settings')

        preferences.set('font_size', settings.get('default_font_size'))
        sublime.save_settings('Preferences.sublime-settings')

    def is_enabled(self, args = []):
        return True

class OpenGitgCommand(sublime_plugin.WindowCommand):
    def run(self, paths = []):
        settings = sublime.load_settings('Foobar.sublime-settings')
        gitg = settings.get('path_to_gitg')

        if gitg is None or not os.path.isfile(gitg):
            gitg = subprocess.Popen("which gitg", shell=True, stdout=subprocess.PIPE).stdout.read()
            if gitg:
                gitg = gitg.decode('UTF-8').strip('\n')
            else:
                 sublime.error_message('Por favor, configure la ruta al binario de gitg.')
                 return False

        # https://github.com/wbond/sublime_terminal/blob/master/Terminal.py#L117
        if paths:
            path = paths[0]
        elif self.window.active_view() and self.window.active_view().file_name():
            path = self.window.active_view().file_name()
        elif self.window.folders():
            path = self.window.folders()[0]
        else:
            sublime.error_message('No es posible abrir gitg aquí.')
            return

        if os.path.isfile(path):
            path = os.path.dirname(path)

        subprocess.Popen([gitg, path], cwd=path)

    def is_enabled(self, args = []):
        return os.name != 'nt'
