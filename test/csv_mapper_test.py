from csv_mapper.app import *
import os
import pytest


class TestCsvMapper:

    def test_load_csv(self):
        csv_content = load_csv("hello,world")
        assert csv_content == [["hello", "world"]]

    def test_load_csv_from_file(self):
        csv_content = load_csv_from_file(os.path.dirname(__file__) + "/fixture.csv")
        assert csv_content == [["h1", "h2"], ["hello", "hello world"]]

    def test_write_csv_to_string(self):
        csv_string = write_csv_to_string([["hello", "world"]])
        assert csv_string == "hello,world\r\n"

    def test_write_csv_to_csv(self):
        csv_content = [["h1", "h2"], ["data1", "data2"]]
        write_csv(csv_content, os.path.dirname(__file__) + "/test_result.csv")
        result = load_csv_from_file(os.path.dirname(__file__) + "/test_result.csv")

        assert result == csv_content

    def test_skip_first_line(self):
        csv_content = [["hello", "world"], ["hello", "world"]]
        rules = [[0, "replace_column", "hello", "helloooo"], [1, "replace_word", "world", "max"]]

        result = map_content(csv_content, rules)
        assert result == [["hello", "world"], ["helloooo", "max"]]

    def test_not_replace_content(self):
        csv_content = [["h1", "h2"], ["hello", "hello world"]]
        rules = [[0, "replace_column", "henllo", "helloooo"], [1, "replace_word", "w0rld", "hello"]]

        result = map_content(csv_content, rules)
        assert result == [["h1", "h2"], ["hello", "hello world"]]

    def test_skip_komma_in_content(self):
        csv_content = [["h1", "h2"], ["hell,,,o,,", "he,,,llo ,,wo,rld"]]
        rules = [[0, "replace_column", "hello", "helloooo"], [1, "replace_word", "world", "max"]]

        result = map_content(csv_content, rules)
        assert result == [["h1", "h2"], ["helloooo", "hello max"]]

    def test_replace_multiple_content(self):
        csv_content = [["h1", "h2"], ["hello world", "worldd"], ["hell0", "hello world"], ["hello", "w0rld"]]
        rules = [[0, "replace_column", "hello", "helloooo"], [1, "replace_word", "world", "max"]]

        result = map_content(csv_content, rules)
        assert result == [["h1", "h2"], ["helloooo", "worldd"], ["hell0", "hello max"], ["helloooo", "w0rld"]]

    def test_delete_column(self):
        csv_content = [["h1", "h2"], ["hello world", "worldd"], ["hell0", "hello world"], ["hello", "w0rld"]]
        rules = [[1, "delete_column", "", ""]]

        result = map_content(csv_content, rules)
        assert result == [["h1"], ["hello world"], ["hell0"], ["hello"]]

    def test_replace_content_regardless_of_case(self):
        csv_content = [["h1", "h2"], ["heLlO world", "worldd"], ["hell0", "hello WoRlD"], ["hello", "w0rld"]]
        rules = [[0, "replace_column", "HelLo", "helloooo"], [1, "replace_word", "wOrld", "MAX"]]

        result = map_content(csv_content, rules)
        assert result == [["h1", "h2"], ["helloooo", "worldd"], ["hell0", "hello MAX"], ["helloooo", "w0rld"]]

    def test_not_replace_content_in_different_columns(self):
        csv_content = [["h1", "h2", "h3"], ["hello", "hello", "hello"]]
        rules = [[0, "replace_column", "hello", "helloooo"], [1, "replace_word", "hello", "max"]]

        result = map_content(csv_content, rules)
        assert result == [["h1", "h2", "h3"], ["helloooo", "max", "hello"]]

    def test_replace_content_in_multiple_columns(self):
        csv_content = [["h1", "h2"], ["hello", "world"]]
        rules = [[0, "replace_column", "hello", "helloooo"], [1, "replace_word", "world", "wooorld"]]

        result = map_content(csv_content, rules)
        assert result == [["h1", "h2"], ["helloooo", "wooorld"]]

    def test_multiple_words_in_replace_column(self):
        csv_content = [["h1", "h2"], ["world", "hello world says mister mustermann"]]
        rules = [[1, "replace_column", "world mustermann hello", "wooorld"]]

        result = map_content(csv_content, rules)
        assert result == [["h1", "h2"], ["world", "wooorld"]]

    def test_unknown_mode_exception(self):
        csv_content = [["h1", "h2"], ["hello", "world"]]
        rules = [[0, "replace_row", "hello", "helloooo"]]

        with pytest.raises(NameError):
            assert apply_rule(csv_content, rules[0])

    def test_string_array_argument_exception(self):
        csv_content = [["h1", "h2"], ["hello", "world"]]
        rules = [[1, "replace_word", "world hello no bye", "wooorld"]]

        with pytest.raises(TypeError):
            assert apply_rule(csv_content, rules[0])

    def test_main_invalid_argument_count_exception(self):
        args = ['app.py', 'source.txt', 'rules.txt', 'target', 'random.txt']

        with pytest.raises(Exception):
            assert main(args)
