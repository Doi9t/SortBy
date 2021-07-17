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

import sublime
import sublime_plugin

from .api.sortapi import SortSettings, SortApi


class SrtbyliCommand(sublime_plugin.TextCommand):

    def run(self, edit, sort='length', reversed=False, regex=None):
        view = self.view
        selection = view.sel()
        sort_api = SortApi()

        settings = sublime.load_settings("SortBy.sublime-settings")

        sort_settings = SortSettings(settings.get("alphabetically_case_sensitive"),
                                     settings.get("handle_selected_part_of_line_as_full_selected_line"),
                                     settings.get("subsort_length_of_line"))

        if selection is None or len(selection) == 0:  # Just is case
            print("SortBy error: No selection found !")
            return

        if len(selection) == 1 and selection[0].empty():  # No selection
            region = selection[0].end()
            raw_lines = [x for x in view.substr(sublime.Region(0, view.size())).splitlines() if x != '']

            sorted_lines = sort_api.sort_lines(raw_lines, sort, regex, reversed, sort_settings)
            self.write_to_view(sorted_lines, False, region, view, edit)
        else:
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

                    sorted_lines = sort_api.sort_lines(raw_lines, sort, regex, reversed, sort_settings)
                    self.write_to_view(sorted_lines, True, region_to_write, view, edit)

    def write_to_view(self, sorted_lines, have_selected_regions_of_text, region, view, edit):
        """
        Method that write the specified dictionary into the view
        :param sorted_lines: The lines to be written to the region
        :param have_selected_regions_of_text:
        :param region: The selected region
        :param view: The view
        :param edit: The edit
        """

        if len(sorted_lines) != 0:
            if have_selected_regions_of_text:
                view.replace(edit, region, ''.join(self.put_end_lines(sorted_lines)))
            else:
                view.erase(edit, sublime.Region(0, view.size()))
                view.insert(edit, 0, ''.join(self.put_end_lines(sorted_lines)))
        else:
            print("SortBy error: No string found !")

    def put_end_lines(self, lines):
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
