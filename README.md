reads a comma separated csv and replaces certain values according to another csv that contains replacements

e.g.

source file:
```
head1,head2
max mustermann,hello world
```

rule file:

```
<ROW>,wordToReplace,word,<MODE>
```
Available Modes:
	```replace_word``` replaces all words, which are equal to the ```wordToReplace```
	```replace_column``` replaces the whole column with ```word``` if the column contains ```wordToReplace```
example::
	0,max,bye,replace_word
	1,hello,bye,replace_column
cmd:
```
python csvmapper.py source.csv rule.csv
```

output:
```
head1,head2
bye mustermann,bye
```