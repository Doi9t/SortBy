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

from unittest import TestCase

from .sort import Sort
from .sortapi import SortApi, SortSettings


class TestSortApi(TestCase):

    def test_sort_lines_alphabetically(self):
        # given
        sort_api = SortApi()
        given_lines = ["yorkshire", "10", "abstract", "manual", "additions", "shadow", "0"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.ALPHABETICALLY, None, False, given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["0", "10", "abstract", "additions", "manual", "shadow", "yorkshire"])

    def test_sort_lines_alphabetically_reversed(self):
        # given
        sort_api = SortApi()
        given_lines = ["yorkshire", "10", "abstract", "manual", "additions", "shadow", "0"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.ALPHABETICALLY, None, True, given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["yorkshire", "shadow", "manual", "additions", "abstract", "10", "0"])

    def test_sort_lines_alphabetically_regex(self):
        # given
        sort_api = SortApi()

        # language=PythonRegExp
        given_regex = "^|[a-zA-Z0-9]*$"

        given_lines = ["yorkshire|0", "shadow|10", "manual|abstract", "additions|additions", "abstract|manual",
                       "10|shadow", "0|yorkshire"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.ALPHABETICALLY, given_regex, False, given_sort_settings)

        # then
        self.assertEqual(array_to_assert,  # Sorted after the pipe
                         ["yorkshire|0", "shadow|10", "manual|abstract", "additions|additions", "abstract|manual",
                          "10|shadow", "0|yorkshire"])

    def test_sort_lines_natural_order(self):
        # given
        sort_api = SortApi()
        given_lines = ["z18", "z17", "z13", "z5", "z16", "z12", "z11", "z3", "z15", "z9", "z6", "z20",
                       "z101", "z10", "z14", "z7", "z1", "z100", "z19", "z8", "z102", "z4", "z2"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.NATURAL_ORDER, None, False, given_sort_settings)

        # then
        self.assertEqual(array_to_assert,
                         ["z1", "z2", "z3", "z4", "z5", "z6", "z7", "z8", "z9", "z10", "z11", "z12", "z13", "z14",
                          "z15", "z16", "z17", "z18", "z19", "z20", "z100", "z101", "z102"])

    def test_sort_lines_natural_order_reversed(self):
        # given
        sort_api = SortApi()
        given_lines = ["z18", "z17", "z13", "z5", "z16", "z12", "z11", "z3", "z15", "z9", "z6", "z20",
                       "z101", "z10", "z14", "z7", "z1", "z100", "z19", "z8", "z102", "z4", "z2"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.NATURAL_ORDER, None, True, given_sort_settings)

        # then
        self.assertEqual(array_to_assert,
                         ["z102", "z101", "z100", "z20", "z19", "z18", "z17", "z16", "z15", "z14", "z13", "z12", "z11",
                          "z10", "z9", "z8", "z7", "z6", "z5", "z4", "z3", "z2", "z1"])