import sublime
import sublime_plugin
import re
import time

class InsertFileHeaderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        args = {}
        # Assigning this to a string to keep command shorter later.
        args['template'] = self.load_settings().get("snippet_file", "Packages/InsertFileHeader/InsertFileHeader.sublime-snippet")
        args['filename'] = self.get_filename()

        args = self.fetch_variables(args)
        options = self.populate_options(args)

        self.make_space()
        self.run_snippet(options)

        # print(self.load_settings().get('vars'))
        # public_props = (name for name in dir(self.load_settings()))
        # for name in public_props:
        #     print (name)

        # for item in self.load_settings():
        #     print(item.names)
        # [a for a in dir(sublime.Settings) if not a.startswith('__') and not callable(getattr(sublime.Settings,a))]

    def fetch_variables(self, args):
        settings = self.load_settings().get('vars')
        for name in settings:
            args[name] = settings.get(name, "<"+name+">")
        # args['created'] = time.ctime(time.time())
        args['created'] = time.strftime('%d-%m_%Y on %I:%M:%S %p IST')

        return args

    def make_space(self):
        # Moving insertion point to the beginning of the file.
        bof = self.view.text_point(0,0)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(bof))
        self.view.show(bof)

    def get_filename(self):
        # Looking for a name, first the buffer name, then the file name,
        # then finally a default value.
        buffname = self.view.name()
        longname = self.view.file_name()
        if buffname:
            return buffname
        elif longname:
            # Convert Windows slashes to Unix slashes (if any)
            longname = re.sub(r'\\', '/', longname)
            namechunks = longname.split('/')
            return namechunks[len(namechunks)-1]
        else:
            return '<filename>'

    def populate_options(self, args):
        options = {}

        for name in args:
            if name == 'template':
                options['name'] = args.get(name)
            else:
                options[name.upper()] = args.get(name)

        return options

    def run_snippet(self, args):
        # Inserting template/snippet
        self.view.run_command("insert_snippet", args)
        print('InsertFileHeader: Inserted header template.')

    def load_settings(self):
        # Getting a few fields from the settings file
        return sublime.load_settings('InsertFileHeader.sublime-settings')



# import shutil
# import sublime
# import sublime_plugin
# class SyncFileCommand(sublime_plugin.TextCommand):
#     def run(self, edit):
#         settings = sublime.load_settings('SyncFile.sublime-settings')
#         src_mappings = settings.get("mappings", [])
#         mappings = []
#         # Check if we have the correct value type
#     if not isinstance(src_mappings, list):
#         print("invalid value type, should be a list: %r" % src_mappings)
#         return
#     for mapping in src_mappings:
#         # Check if we have the correct value types for the mappings
#         if not isinstance(mapping, dict):
#             print("invalid mapping type, should be a dict: %r" % mapping)
#             continue
#         # Check if required keys exist
#         elif not all(name in mapping for name in ('source', 'dest')):
#             print("required key(s) missing: %r" % mapping)
#             continue
#         # Check if required keys have correct value type
#         elif not isinstance(mapping['source'], str) or not isinstance(mapping['dest'], str):
#             print("invalid type for required key(s), should be str: %r" % mapping)
#             continue
#         # Check if required keys are not empty
#         elif not mapping['source'] or not mapping['dest']:
#             print("required key(s) empty: %r" % mapping)
#             continue
#         else:
#             mappings.append(mapping)

#     # Check if there are valid mappings
#     if not mappings:
#         print("No valid mappings found")
#         return

#     source_name = self.view.file_name()

#     for mapping in mappings:
#         if source_name in mapping['source']:
#             shutil.copyfile(source_name, source_name.replace(mapping['source'], mapping['dest']))
#             return
#     else:
#         msg = 'Your current file location is not in one of your source locations '
#         msg += 'or the relevant dest location is empty. '
#         msg += 'Please set the settings file properly and retry.'
#         sublime.error_message(msg)
