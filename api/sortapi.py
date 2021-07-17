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

from .subsorts import SubSorts

bases = {'binary': 2, 'octal': 8, 'decimal': 10, 'hexadecimal': 16}


class SortSettings(object):
    """
    An object that contains the settings for the sorts
    """

    def __init__(self, alphabetically_case_sensitive, handle_selected_part_of_line_as_full_selected_line,
                 subsort_length_of_line):
        self.alphabetically_case_sensitive = alphabetically_case_sensitive,
        self.handle_selected_part_of_line_as_full_selected_line = handle_selected_part_of_line_as_full_selected_line,
        self.subsort_length_of_line = subsort_length_of_line


class _ContainerHelper(object):
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


class _NumberSortContainerHelper(_ContainerHelper):
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


class SortApi:
    def __sort_numbers(self, mapped_regex_lines, sort, reversed, regex):
        """
        Sort the first number of each line, contained in the region
        :param regex: The selector for the number
        :param reversed: Is the reversed order
        :param sort: The sort
        :param mapped_regex_lines: The unsorted lines
        """

        sorted_lines = []
        containers = []

        if regex is None:
            return

        for containerHelperRegex in mapped_regex_lines:
            full_line = containerHelperRegex.line
            group = containerHelperRegex.value

            number_match = re.search(regex, group)

            if number_match is None:
                containers.append(_NumberSortContainerHelper(full_line, 0, sort))
            else:
                containers.append(_NumberSortContainerHelper(full_line, number_match.group(), sort))

        containers.sort(key=lambda x: x.getNumber(), reverse=reversed)

        for line in containers:
            sorted_lines.append(line.getLine())

        return sorted_lines

    def __natural_sort(self, mapped_regex_lines, reversed=False):
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

    def __sort_structures(self, mapped_regex_lines, sort, reversed):
        """
        Sort the first structure of each line, contained in the region
        :param mapped_regex_lines: The unsorted lines, contained into a ContainerHelper (value = found regex group)
        :param sort: The selector for the number
        :param reversed: Is the reversed order
        """
        sorted_lines = []
        lines_to_sort = []

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
                    lines_to_sort.append(_ContainerHelper(group, "0.0.0"))
                else:
                    major = sem_ver_match.group('major')
                    minor = sem_ver_match.group('minor')
                    patch = sem_ver_match.group('patch')
                    version = "{major}.{minor}.{patch}".format(major=major, minor=minor, patch=patch)
                    lines_to_sort.append(_ContainerHelper(full_line, version))

            # Thanks to @eli-bendersky https://stackoverflow.com/a/2574090
            lines_to_sort.sort(key=lambda x: list(map(int, x.value.split('.'))), reverse=reversed)

        for current_line in lines_to_sort:
            sorted_lines.append(current_line.line)

        return sorted_lines

    def __sort_strings(self, mapped_regex_lines, sort, reversed, settings):
        """
        Sort the strings / lines, contained in the region
        :param mapped_regex_lines: The unsorted lines
        :param sort: The selector for the number
        :param reversed: Is the reversed order
        :param settings: The settings for the sort
        """
        sorted_mapped_regex_line = None
        sorted_lines = []

        if sort == 'length':
            subsort_length_of_line = settings.subsort_length_of_line

            if subsort_length_of_line is None:
                sorted_mapped_regex_line = \
                    sorted(mapped_regex_lines, key=lambda current_str: len(current_str.value), reverse=reversed)
            elif SubSorts.is_alphabetically_sort(subsort_length_of_line):
                sorted_mapped_regex_line = defaultdict(list)

                # Put all values in a defaultdict (Grouped by length)
                for value in sorted(mapped_regex_lines, key=lambda current_str: len(current_str.value)):
                    sorted_mapped_regex_line[len(value.value)].append(value)

                is_descending = SubSorts.is_alphabetically_descending(subsort_length_of_line)

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
            if settings.alphabetically_case_sensitive:
                sorted_mapped_regex_line = \
                    sorted(mapped_regex_lines, key=lambda current_str: current_str.value, reverse=reversed)
            else:
                sorted_mapped_regex_line = \
                    sorted(mapped_regex_lines, key=lambda current_string: current_string.value.lower(),
                           reverse=reversed)
        elif sort == 'natural_order':
            sorted_mapped_regex_line = self.__natural_sort(mapped_regex_lines, reversed)

        if sorted_mapped_regex_line is not None:
            for current_line in sorted_mapped_regex_line:
                sorted_lines.append(current_line.line)

        return sorted_lines

    def sort_lines(self, raw_lines, sort, regex, reversed, sort_settings):
        """
        :param raw_lines: The raw lines
        :param sort: The selector for the number
        :param regex: The regex for the slection
        :param reversed: Is the reversed order
        :param sort_settings: The settings
        """

        mapped_regex_lines = self.__map_regex_matches_with_lines(raw_lines, regex)

        if sort == 'decimal' or sort == 'octal' or sort == 'hexadecimal' or sort == 'binary':
            return self.__sort_numbers(mapped_regex_lines, sort, reversed, regex)
        elif sort == 'length' or sort == 'alphabetically' or sort == 'natural_order':
            return self.__sort_strings(mapped_regex_lines, sort, reversed, sort_settings)
        elif sort == 'semver':
            return self.__sort_structures(mapped_regex_lines, sort, reversed)
        else:
            return []

    def __map_regex_matches_with_lines(self, raw_lines, regex):
        """
        Map the raw line with the regex group, if present, or the raw line if not.
        :param raw_lines: The unsorted lines
        :param regex: The regex
        :return:
        """

        values = []

        for line in raw_lines:
            if regex is None:  # No regex
                values.append(_ContainerHelper(line, line))
                continue

            match = re.search(regex, line)

            if match is None:
                values.append(_ContainerHelper(line, line))
            else:
                values.append(_ContainerHelper(line, match.group()))

        return values
