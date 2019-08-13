reads a comma separated csv and replaces certain values according to another csv that contains replacements

e.g.

source file:
```
head1,head2
hello,world
```

rule file:
```
0,hello,bye
```

cmd:
```
python csvmapper.py source.csv rule.csv
```

output:
```
head1,head2
bye,world
```