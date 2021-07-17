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

from . import SubSorts
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

    def test_sort_lines_alphabetically_case_sensitive(self):
        # given
        sort_api = SortApi()
        given_lines = ["Ethical", "eternal", "filling", "Figures", "EStonia", "habitat", "guitars"]
        given_sort_settings = SortSettings(True, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.ALPHABETICALLY, None, False, given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["EStonia", "Ethical", "Figures", "eternal", "filling", "guitars", "habitat"])

    def test_sort_lines_alphabetically_case_sensitive_reversed(self):
        # given
        sort_api = SortApi()
        given_lines = ["Ethical", "eternal", "filling", "Figures", "EStonia", "habitat", "guitars"]
        given_sort_settings = SortSettings(True, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.ALPHABETICALLY, None, True, given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["habitat", "guitars", "filling", "eternal", "Figures", "Ethical", "EStonia"])

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

    def test_sort_lines_length(self):
        # given
        sort_api = SortApi()
        given_lines = ["1", "11111111111", "aaa", "111111111", "1", "111111", "11"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.LENGTH, None, False, given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["1", "1", "11", "aaa", "111111", "111111111", "11111111111"])

    def test_sort_lines_length_reversed(self):
        # given
        sort_api = SortApi()
        given_lines = ["1", "11111111111", "aaa", "111111111", "1", "111111", "11"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.LENGTH, None, True, given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["11111111111", "111111111", "111111", "aaa", "11", "1", "1"])

    def test_sort_lines_length_subsort_alphabetically(self):
        # given
        sort_api = SortApi()
        given_lines = ["a", "bb", "ccc", "aa", "ccc", "ddd", "ccc", "b", "a"]
        given_sort_settings = SortSettings(False, False, SubSorts.ALPHABETICALLY)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.LENGTH, None, False,
                                              given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["a", "a", "b", "aa", "bb", "ccc", "ccc", "ccc", "ddd"])

    def test_sort_lines_length_subsort_alphabetically_reversed(self):
        # given
        sort_api = SortApi()
        given_lines = ["a", "bb", "ccc", "aa", "ccc", "ddd", "ccc", "b", "a"]
        given_sort_settings = SortSettings(False, False, SubSorts.ALPHABETICALLY)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.LENGTH, None, True,
                                              given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["ccc", "ccc", "ccc", "ddd", "aa", "bb", "a", "a", "b"])

    def test_sort_lines_decimal(self):
        # given
        sort_api = SortApi()

        given_lines = ["1", "11111111111", "111", "111111111", "1", "111111", "11"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.DECIMAL, None, False,
                                              given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["1", "1", "11", "111", "111111", "111111111", "11111111111"])

    def test_sort_lines_decimal_reversed(self):
        # given
        sort_api = SortApi()

        given_lines = ["1", "11111111111", "111", "111111111", "1", "111111", "11"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.DECIMAL, None, True,
                                              given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["11111111111", "111111111", "111111", "111", "11", "1", "1"])

    def test_sort_lines_hexadecimal(self):
        # given
        sort_api = SortApi()

        given_lines = ["00", "0xFF", "0x00", "0x0C", "0x0A", "55"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.HEXADECIMAL, None, False,
                                              given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["00", "0x00", "0x0A", "0x0C", "55", "0xFF"])

    def test_sort_lines_hexadecimal_reversed(self):
        # given
        sort_api = SortApi()

        given_lines = ["00", "0xFF", "0x00", "0x0C", "0x0A", "55"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.HEXADECIMAL, None, True,
                                              given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["0xFF", "55", "0x0C", "0x0A", "00", "0x00"])

    def test_sort_lines_octal(self):
        # given
        sort_api = SortApi()

        given_lines = ["0000101", "7", "27", "007", "1234567"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.OCTAL, None, False,
                                              given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["7", "007", "27", "0000101", "1234567"])

    def test_sort_lines_octal_reversed(self):
        # given
        sort_api = SortApi()

        given_lines = ["0000101", "7", "27", "007", "1234567"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.OCTAL, None, True,
                                              given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["1234567", "0000101", "27", "7", "007"])

    def test_sort_lines_binary(self):
        # given
        sort_api = SortApi()

        given_lines = ["10100", "0", "111111", "101010", "1", "1110000"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.BINARY, None, False,
                                              given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["0", "1", "10100", "101010", "111111", "1110000"])

    def test_sort_lines_binary_reversed(self):
        # given
        sort_api = SortApi()

        given_lines = ["10100", "0", "111111", "101010", "1", "1110000"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.BINARY, None, True,
                                              given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["1110000", "111111", "101010", "10100", "1", "0"])

    def test_sort_lines_semver(self):
        # given
        sort_api = SortApi()

        given_lines = ["2.2.1", "0.12.1", "2.0.9", "1.1.1", "1.2.2", "2.0.1"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.SEMVER, None, False,
                                              given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["0.12.1", "1.1.1", "1.2.2", "2.0.1", "2.0.9", "2.2.1"])

    def test_sort_lines_semver_reversed(self):
        # given
        sort_api = SortApi()

        given_lines = ["2.2.1", "0.12.1", "2.0.9", "1.1.1", "1.2.2", "2.0.1"]
        given_sort_settings = SortSettings(False, False, None)

        # when
        array_to_assert = sort_api.sort_lines(given_lines, Sort.SEMVER, None, True,
                                              given_sort_settings)

        # then
        self.assertEqual(array_to_assert, ["2.2.1", "2.0.9", "2.0.1", "1.2.2", "1.1.1", "0.12.1"])
