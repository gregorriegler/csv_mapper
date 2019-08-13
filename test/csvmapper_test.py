from src.csvmapper import load_csv, load_csv_from_file, map_content, write_csv
import os


class TestCsvMapper:

    def test_load_csv(self):
        csv_content = load_csv("hello,world")
        assert csv_content == [["hello", "world"]]

    def test_load_csv_from_file(self):
        csv_content = load_csv_from_file(os.path.dirname(__file__) + "/fixture.csv")
        assert csv_content == [["hello", "world"]]

    def test_write_csv_to_string(self):
        csv_string = write_csv([["hello", "world"]])
        assert csv_string == "hello,world\r\n"

    def test_skip_first_line(self):
        csv_content = [["hello", "world"], ["hello", "world"]]
        rules = [[0, "hello", "helloooo"]]

        result = map_content(csv_content, rules)
        assert result == [["hello", "world"], ["helloooo", "world"]]

    def test_not_replace_content(self):
        csv_content = [["h1", "h2"], ["hello", "world"]]
        rules = [[0, "Hello", "helloooo"]]

        result = map_content(csv_content, rules)
        assert result == [["h1", "h2"], ["hello", "world"]]

    def test_replace_multiple_content(self):
        csv_content = [["h1", "h2"], ["hello", "world"], ["hell0", "world"], ["hello", "w0rld"]]
        rules = [[0, "hello", "helloooo"]]

        result = map_content(csv_content, rules)
        assert result == [["h1", "h2"], ["helloooo", "world"], ["hell0", "world"], ["helloooo", "w0rld"]]

    def test_replace_content_in_multiple_columns(self):
        csv_content = [["h1", "h2"], ["hello", "world"]]
        rules = [[0, "hello", "helloooo"], [1, "world", "wooorld"]]

        result = map_content(csv_content, rules)
        assert result == [["h1", "h2"], ["helloooo", "wooorld"]]
