reads a comma separated csv and replaces certain values according to another csv that contains replacements rules

Please try to use ```UTF-8``` file format for the source.csv and rule.csv file
Please make sure your CSV files have CRLF or LF file endings to seperate the rows
and use ```,``` as delimiter to seperate the columns

example::


	head1,head2,head3\r\n
	data1,data2,data3\r\n

OR

	head1,head2,head3\n
	data1,data2,data3\n
	

To exectute this programm you have to specify a source csv file and a rule csv file:
```
python app.py source.csv rule.csv
```

Rule File Format:
```
<ROW>,wordToReplace,word,<MODE>
```

Available Modes:

**replace_word** replaces all words, which are equal to the **wordToReplace** with the specified **word**
**replace_column** replaces the whole column with **word** if the column contains **wordToReplace**


example::

source file:
```
h1,h2
hello,hello world
```

rule file:

```
0,hello,helloooo,replace_column
1,world,max,replace_word
```

output:
```
h1,h2
helloooo,hello max
```

To test this application execute this command in the root directory of the project:
```
python csv_mapper/app.py test/fixture.csv test/rules.csv
```