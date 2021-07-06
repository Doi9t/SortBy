#     Copyright 2014 - 2021 Yannick Watier
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import re
from collections import defaultdict

import sublime
import sublime_plugin

bases = {'binary': 2, 'octal': 8, 'decimal': 10, 'hexadecimal': 16}


# Thanks to Ned Batchelder for this function
# http://nedbatchelder.com/blog/200712/human_sorting.html
def natural_sort(list_to_sort):
    """
    Sort the specified list, with the natural sort
    :param list_to_sort: the list to sort
    :return: The sorted list
    """
    convertion = lambda e: int(e) if e.isdigit() else e.lower()
    key1 = lambda key: [convertion(g) for g in re.split('([0-9]+)', key)]
    return sorted(list_to_sort, key=key1)


def putEndLines(lines):
    """
    Method that adds a `\n` to each line
    :param lines:
    :return:
    """
    lines = [str(x.encode('utf-8'), encoding='utf-8') + '\n' for x in lines]
    lines[-1] = lines[-1][:-1]
    return lines


class ContainerHelper(object):
    """
    An object that contains the selected value & full line.
    """

    def __init__(self, line, value):
        self.line = str(line).strip()
        self.value = value

    def getLine(self):
        return self.line

    def getValue(self):
        return self.value


class NumberSortContainerHelper(ContainerHelper):
    """
    An object that contains the number & full line.
    """

    def __init__(self, line, number, base):
        super().__init__(line, number)
        self.base = base

    def getNumber(self):
        number = self.getValue()
        if number == 0:
            return 0
        else:
            current_base = bases[self.base]
            if current_base == 10:
                return float(number)
            else:
                return int(number, current_base)


class SrtbyliCommand(sublime_plugin.TextCommand):
    def sortNumbers(self, region, lines, sort):
        """
        Sort the first number of each line, contained in the region
        :param region: The region
        :param lines: The lines
        :param sort: The type of the sort
        """
        sorted_lines = []
        obj = []

        for line in lines:
            numberMatch = None

            if sort == 'decimal':
                numberMatch = re.search(r'[+-]?\d+(?:\.\d+)?', line)
            elif sort == 'octal':
                numberMatch = re.search(r'[0-7]+', line)
            elif sort == 'hexadecimal':
                numberMatch = re.search(r'(?:0[xX])?[0-9a-fA-F]+', line)
            elif sort == 'binary':
                numberMatch = re.search(r'[01]+', line)

            if numberMatch is None:
                obj.append(NumberSortContainerHelper(line, 0, sort))
            else:
                obj.append(NumberSortContainerHelper(line, numberMatch.group(), sort))

        obj.sort(key=lambda x: x.getNumber(), reverse=self.reversed)

        for line in obj:
            sorted_lines.append(line.getLine())

        self.writeToView(region, sorted_lines)

    def sortStructures(self, region, lines, sort):
        """
        Sort the first structure of each line, contained in the region
        :param region: The region
        :param lines: The lines
        :param sort: The type of the sort
        """
        sorted_lines = []
        lines_to_sort = []

        if sort == 'semver':
            for line in lines:
                # The regex come from : https://semver.org/
                semVerMatch = re.search(r'(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)'
                                        r'(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
                                        r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))'
                                        r'?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?', line)

                if semVerMatch is None:
                    lines_to_sort.append(ContainerHelper(line, "0.0.0"))
                else:
                    major = semVerMatch.group('major')
                    minor = semVerMatch.group('minor')
                    patch = semVerMatch.group('patch')
                    version = "{major}.{minor}.{patch}".format(major=major, minor=minor, patch=patch)
                    lines_to_sort.append(ContainerHelper(line, version))

            # Thanks to @eli-bendersky https://stackoverflow.com/a/2574090
            lines_to_sort.sort(key=lambda x: list(map(int, x.getValue().split('.'))), reverse=self.reversed)

        for line in lines_to_sort:
            sorted_lines.append(line.getLine())

        self.writeToView(region, sorted_lines)

    def sortStrings(self, region, lines, sort):
        """
        Sort the strings / lines, contained in the region
        :param region: The region
        :param lines: The lines
        :param sort: The type of the sort
        """
        sorted_lines = None

        if sort == 'length':
            if self.settings.get('length_alphabetically_enabled'):
                sorted_lines = defaultdict(list)

                # Put all values in a defaultdict (Grouped by length)
                for value in sorted(lines, key=lambda current_str: len(current_str)):
                    sorted_lines[len(value)].append(value)

                # Sort the groups alphabetically
                for index, values in sorted_lines.items():
                    sorted_lines[index] = sorted(values, reverse=self.settings.get('length_alphabetically_reversed'))

                # Sort the groups by length
                sorted_lines = sorted(sorted_lines.items(), key=lambda t: t[0], reverse=self.reversed)

                tempContainer = []
                for index, values in sorted_lines:
                    for value in values:
                        tempContainer.append(value)
                sorted_lines = tempContainer
            else:
                sorted_lines = sorted(lines, key=lambda current_str: len(current_str), reverse=self.reversed)

        elif sort == 'string':
            if self.settings.get('case_sensitive'):
                sorted_lines = sorted(lines, reverse=self.reversed)
            else:
                sorted_lines = sorted(lines, key=lambda current_string: current_string.lower(), reverse=self.reversed)

        elif sort == 'naturalOrder':
            sorted_lines = natural_sort(lines)

        if sorted_lines is not None:
            self.writeToView(region, sorted_lines)

    def writeToView(self, region, sorted_lines):
        """
        Method that write the specified dictionary into the view
        :param region: The selected region
        :param sorted_lines: The lines to be written to the region
        """

        if len(sorted_lines) != 0:
            if self.haveSelectedRegionsOfText:
                self.view.replace(self.edit, region, ''.join(putEndLines(sorted_lines)))
            else:
                self.view.erase(self.edit, sublime.Region(0, self.view.size()))
                self.view.insert(self.edit, 0, ''.join(putEndLines(sorted_lines)))
        else:
            print("SortBy error: No string found !")

    def run(self, edit, sort='length', reversed=False):
        self.edit = edit
        view = self.view
        self.reversed = reversed
        SrtbyliCommand.edit = edit
        self.settings = sublime.load_settings("SortBy.sublime-settings")

        selection = view.sel()

        if selection is None or len(selection) == 0:  # Just is case
            print("SortBy error: No selection found !")
            return

        if len(selection) == 1 and selection[0].empty():  # No selection
            self.haveSelectedRegionsOfText = False
            region = selection[0].end()
            raw_lines = [x for x in view.substr(sublime.Region(0, self.view.size())).splitlines() if x != '']
            self.apply_sort_from_type(raw_lines, region, sort)
        else:
            self.haveSelectedRegionsOfText = True
            for region in selection:
                if region.empty():
                    continue
                else:
                    region_to_write = None
                    if self.settings.get('handle_selected_part_of_line_has_full_selected_line'):
                        regions = view.lines(region)
                        first = regions[0]
                        last_region = regions[-1]
                        region_to_write = sublime.Region(first.begin(), last_region.end())
                        selection.add(region_to_write)
                    else:
                        region_to_write = region

                    raw_lines = [x for x in view.substr(region_to_write).splitlines() if x != '']
                    self.apply_sort_from_type(raw_lines, region_to_write, sort)

    def apply_sort_from_type(self, raw_lines, region, sort):
        if sort == 'length' or sort == 'string' or sort == 'naturalOrder':
            self.sortStrings(region, raw_lines, sort)
        elif sort == 'decimal' or sort == 'octal' or sort == 'hexadecimal' or sort == 'binary':
            self.sortNumbers(region, raw_lines, sort)
        elif sort == 'semver':
            self.sortStructures(region, raw_lines, sort)
