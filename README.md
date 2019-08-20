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
	

To exectute this program you have to specify a source csv file and a rule csv file:
```
python app.py source.csv rule.csv
```

You can also specify a output.csv,
the result is going to be written into this file instead of the stdout stream

```
python app.py source.csv rule.csv destination.csv
```

Available Modes for the rulefile:

**replace_word** replaces all words, which are equal to the **wordToReplace** with the specified **word**

**replace_column[single wordToReplace]** replaces the whole column with **word** if the column contains **wordToReplace**

**replace_column[multipe wordsToReplace]** replaces the whoel column with the specified **word** if the column contains all 
words that are in **wordsToReplace**

example rulefile::

```
1,hello,helloooo,replace_word
```

~ this rule would replace all **hello** words in **each row** of column **2**

```
3,hello, max mustermann, replace_column
```

~ this rule would replace the whole field with **max mustermann** if it contains **hello** in each row  of column **4**

```
0,hey world max,hallo max mustermann!,replace_column  
```

~ this rule would replace the whole field with **hallo max mustermann!** in each row of column **1**
if it contains the words **hey**, **world** and **max**

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
2,mustermann hello max,hello World!,replace_column
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