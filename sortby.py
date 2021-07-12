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

from .sorttype import SortType

bases = {'binary': 2, 'octal': 8, 'decimal': 10, 'hexadecimal': 16}


def natural_sort(mapped_regex_lines, reversed=False):
    """
    Sort the specified list, with the natural sort.

    A special thanks to Ned Batchelder for this function
    https://nedbatchelder.com/blog/200712/human_sorting.html
    :param reversed: Reverse the list, if true
    :param mapped_regex_lines: The unsorted lines
    :return: The sorted list
    """
    convertion = lambda e: int(e) if e.isdigit() else e.lower()
    return sorted(mapped_regex_lines, key=lambda key: [convertion(g) for g in re.split('([0-9]+)', key.value)],
                  reverse=reversed)


def put_end_lines(lines):
    """
    Method that adds a `\n` to each line
    :param lines:
    :return:
    """

    values = []
    for line in lines:
        values.append(str(line.encode('utf-8'), encoding='utf-8') + '\n')
    values[-1] = values[-1][:-1]
    return values


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


class SortParameters:
    """
    An object that contains the parameters for the sort
    """

    def __init__(self, sort, reversed, regex, settings):
        self.sort = sort
        self.reversed = reversed
        self.settings = settings
        self.regex = regex


class sublimeParameters:
    """
    An object that contains the parameters of sublime
    """

    def __init__(self, view, edit):
        self.view = view
        self.edit = edit
        self.have_selected_regions_of_text = None


class SrtbyliCommand(sublime_plugin.TextCommand):
    def sort_numbers(self, region, mapped_regex_lines, sort_parameters, sublime_parameters):
        """
        Sort the first number of each line, contained in the region
        :param region: The region
        :param mapped_regex_lines: The unsorted lines
        :param sort_parameters: The parameters
        :param sublime_parameters: The parameters for sublime
        """

        sorted_lines = []
        containers = []

        regex = sort_parameters.regex
        reversed = sort_parameters.reversed
        sort = sort_parameters.sort

        if regex is None:
            return

        for containerHelperRegex in mapped_regex_lines:
            full_line = containerHelperRegex.line
            group = containerHelperRegex.value

            number_match = re.search(regex, group)

            if number_match is None:
                containers.append(NumberSortContainerHelper(full_line, 0, sort))
            else:
                containers.append(NumberSortContainerHelper(full_line, number_match.group(), sort))

        containers.sort(key=lambda x: x.getNumber(), reverse=reversed)

        for line in containers:
            sorted_lines.append(line.getLine())

        self.write_to_view(region, sorted_lines, sublime_parameters)

    def sort_structures(self, region, mapped_regex_lines, sort_parameters, sublime_parameters):
        """
        Sort the first structure of each line, contained in the region
        :param region: The region
        :param mapped_regex_lines: The unsorted lines, contained into a ContainerHelper (value = found regex group)
        :param sort_parameters: The parameters
        :param sublime_parameters: The parameters for sublime
        """
        sorted_lines = []
        lines_to_sort = []

        sort = sort_parameters.sort
        reversed = sort_parameters.reversed

        if sort == 'semver':
            for containerHelperRegex in mapped_regex_lines:

                full_line = containerHelperRegex.line
                group = containerHelperRegex.value

                # The regex come from : https://semver.org/
                sem_ver_match = re.search(r'(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)'
                                          r'(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
                                          r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))'
                                          r'?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?', group)

                if sem_ver_match is None:
                    lines_to_sort.append(ContainerHelper(group, "0.0.0"))
                else:
                    major = sem_ver_match.group('major')
                    minor = sem_ver_match.group('minor')
                    patch = sem_ver_match.group('patch')
                    version = "{major}.{minor}.{patch}".format(major=major, minor=minor, patch=patch)
                    lines_to_sort.append(ContainerHelper(full_line, version))

            # Thanks to @eli-bendersky https://stackoverflow.com/a/2574090
            lines_to_sort.sort(key=lambda x: list(map(int, x.value.split('.'))), reverse=reversed)

        for current_line in lines_to_sort:
            sorted_lines.append(current_line.line)

        self.write_to_view(region, sorted_lines, sublime_parameters)

    def sort_strings(self, region, mapped_regex_lines, sort_parameters, sublime_parameters):
        """
        Sort the strings / lines, contained in the region
        :param region: The region
        :param mapped_regex_lines: The unsorted lines
        :param sort_parameters: The parameters
        :param sublime_parameters: The parameters for sublime
        """
        sorted_mapped_regex_line = None

        sort = sort_parameters.sort
        reversed = sort_parameters.reversed
        settings = sort_parameters.settings

        if sort == 'length':
            subsort_length = settings.get('subsort_length_of_line')
            if subsort_length is None:
                sorted_mapped_regex_line = \
                    sorted(mapped_regex_lines, key=lambda current_str: len(current_str.value), reverse=reversed)
            elif SortType.is_alphabetically_sort(subsort_length):
                sorted_mapped_regex_line = defaultdict(list)

                # Put all values in a defaultdict (Grouped by length)
                for value in sorted(mapped_regex_lines, key=lambda current_str: len(current_str.value)):
                    sorted_mapped_regex_line[len(value.group)].append(value)

                is_descending = SortType.is_alphabetically_descending(subsort_length)

                # Sort the groups alphabetically
                for index, values in sorted_mapped_regex_line.items():
                    sorted_mapped_regex_line[index] = \
                        sorted(values, key=lambda current_str: len(current_str.value), reverse=is_descending)

                # Sort the groups by length
                sorted_mapped_regex_line = \
                    sorted(sorted_mapped_regex_line.items(), key=lambda t: t[0], reverse=reversed)

                temp_container = []
                for index, values in sorted_mapped_regex_line:
                    for value in values:
                        temp_container.append(value)
                sorted_mapped_regex_line = temp_container
        elif sort == 'alphabetically':
            if settings.get('alphabetically_case_sensitive'):
                sorted_mapped_regex_line = \
                    sorted(mapped_regex_lines, key=lambda current_str: current_str.value, reverse=reversed)
            else:
                sorted_mapped_regex_line = \
                    sorted(mapped_regex_lines, key=lambda current_string: current_string.value.lower(),
                           reverse=reversed)
        elif sort == 'natural_order':
            sorted_mapped_regex_line = natural_sort(mapped_regex_lines, reversed)

        if sorted_mapped_regex_line is not None:
            real_lines = []
            for current_line in sorted_mapped_regex_line:
                real_lines.append(current_line.line)

            self.write_to_view(region, real_lines, sublime_parameters)

    def write_to_view(self, region, sorted_lines, sublime_parameters):
        """
        Method that write the specified dictionary into the view
        :param region: The selected region
        :param sorted_lines: The lines to be written to the region
        :param sublime_parameters: The parameters for sublime
        """

        view = sublime_parameters.view
        edit = sublime_parameters.edit

        if len(sorted_lines) != 0:
            if sublime_parameters.have_selected_regions_of_text:
                view.replace(edit, region, ''.join(put_end_lines(sorted_lines)))
            else:
                view.erase(edit, sublime.Region(0, view.size()))
                view.insert(edit, 0, ''.join(put_end_lines(sorted_lines)))
        else:
            print("SortBy error: No string found !")

    def run(self, edit, sort='length', reversed=False, regex=None):
        view = self.view
        selection = view.sel()
        settings = sublime.load_settings("SortBy.sublime-settings")

        sort_parameters = SortParameters(sort, reversed, regex, settings)
        sublime_parameters = sublimeParameters(view, edit)

        if selection is None or len(selection) == 0:  # Just is case
            print("SortBy error: No selection found !")
            return

        if len(selection) == 1 and selection[0].empty():  # No selection
            sublime_parameters.have_selected_regions_of_text = False
            region = selection[0].end()
            raw_lines = [x for x in view.substr(sublime.Region(0, view.size())).splitlines() if x != '']
            self.apply_sort_to_lines(raw_lines, region, sort_parameters, sublime_parameters)
        else:
            sublime_parameters.have_selected_regions_of_text = True
            for region in selection:
                if region.empty():
                    continue
                else:
                    region_to_write = None
                    if settings.get('handle_selected_part_of_line_as_full_selected_line'):
                        regions = view.lines(region)
                        first = regions[0]
                        last_region = regions[-1]
                        region_to_write = sublime.Region(first.begin(), last_region.end())
                        selection.add(region_to_write)
                    else:
                        region_to_write = region

                    raw_lines = [x for x in view.substr(region_to_write).splitlines() if x != '']
                    self.apply_sort_to_lines(raw_lines, region_to_write, sort_parameters, sublime_parameters)

    def apply_sort_to_lines(self, raw_lines, region, sort_parameters, sublime_parameters):
        sort = sort_parameters.sort

        mapped_regex_lines = self.map_regex_matches_with_lines(raw_lines, sort_parameters)

        if sort == 'decimal' or sort == 'octal' or sort == 'hexadecimal' or sort == 'binary':
            self.sort_numbers(region, mapped_regex_lines, sort_parameters, sublime_parameters)
        elif sort == 'length' or sort == 'alphabetically' or sort == 'natural_order':
            self.sort_strings(region, mapped_regex_lines, sort_parameters, sublime_parameters)
        elif sort == 'semver':
            self.sort_structures(region, mapped_regex_lines, sort_parameters, sublime_parameters)

    def map_regex_matches_with_lines(self, raw_lines, sort_parameters):
        """
        Map the raw line with the regex group, if present, or the raw line if not.
        :param raw_lines: The unsorted lines
        :param sort_parameters: The parameters
        :return:
        """

        values = []
        regex = sort_parameters.regex

        for line in raw_lines:
            if regex is None:  # No regex
                values.append(ContainerHelper(line, line))
                continue

            match = re.search(regex, line)

            if match is None:
                values.append(ContainerHelper(line, line))
            else:
                values.append(ContainerHelper(line, match.group()))

        return values
