import os
from collections import OrderedDict
from pbxproj import PBXGenericObject


class XCBuildConfigurationFlags:
    OTHER_CFLAGS = u'OTHER_CFLAGS'
    OTHER_LDFLAGS = u'OTHER_LDFLAGS'
    HEADER_SEARCH_PATHS = u'HEADER_SEARCH_PATHS'
    LIBRARY_SEARCH_PATHS = u'LIBRARY_SEARCH_PATHS'
    FRAMEWORK_SEARCH_PATHS = u'FRAMEWORK_SEARCH_PATHS'
    LD_RUNPATH_SEARCH_PATHS = u'LD_RUNPATH_SEARCH_PATHS'


class XCBuildConfiguration(PBXGenericObject):
    #调用这个接口后假如已经存在flag的话必定会变成数组
    def add_flags(self, flag_name, flags):
        if u'buildSettings' not in self:
            self[u'buildSettings'] = PBXGenericObject()

        current_flags = self.buildSettings[flag_name]
        if current_flags is None:
            self.set_flags(flag_name, flags)
            return

        if not isinstance(current_flags, list):
            current_flags = [current_flags]

        if not isinstance(flags, list):
            flags = [flags]

        self.set_flags(flag_name, current_flags + flags)

    def set_flags(self, flag_name, flags):
        if u'buildSettings' not in self:
            self[u'buildSettings'] = PBXGenericObject()

        if not isinstance(flags, list):
            flags = [flags]

        self.buildSettings[flag_name] = list(OrderedDict.fromkeys(flags))

    def remove_flags(self, flag_name, flags):
        if u'buildSettings' not in self or self.buildSettings[flag_name] is None:
            # nothing to remove
            return False

        current_flags = self.buildSettings[flag_name]
        if not isinstance(current_flags, list):
            current_flags = [current_flags]

        if flags is None:
            flags = current_flags

        if not isinstance(flags, list):
            flags = [flags]

        self.buildSettings[flag_name] = [x for x in current_flags if x not in flags]
        return True

    def add_search_paths(self, key, paths, recursive=False, escape=False):
        if not isinstance(paths, list):
            paths = [paths]

        # build the recursive/escaped strings and add the flags accordingly
        flags = []
        for path in paths:
            if path == '$(inherited)':
                escape = False
                recursive = False

            if escape:
                path = u'"{0}"'.format(path)

            if recursive and not path.endswith('/**'):
                path = os.path.join(path, '**')

            flags.append(path)

        self.add_flags(key, flags)

    def remove_search_paths(self, key, paths):
        return self.remove_flags(key, paths)
