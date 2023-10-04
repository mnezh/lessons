# make basics

[make](https://www.gnu.org/software/make/manual/html_node/index.html) - the utility, which determines automatically which pieces of a large program need to be recompiled, and issues the commands to recompile them.

Could be used for general task or data processing automation.

## What's there

- [Makefile](Makefile) - commented example script for make utility
- [data1.txt](data1.txt) and [data2.txt](data2.txt) - unsorted text files with the list of names

## Making Makefile

Read the manual [3.1 What Makefiles Contain](https://www.gnu.org/software/make/manual/html_node/Makefile-Contents.html)

We're going to use just the very basic things.

### Section 1 - variables

We're going to define variable `TEXT_FILES` using the builtin `wildcard` make function (see [8.3 Functions for File Names](https://www.gnu.org/software/make/manual/html_node/File-Name-Functions.html)):
```make
TEXT_FILES := $(wildcard *.txt)
```
Based on list of text files, we're defining the list of desired sorted files, replacing `.txt` file name extension with `.sorted` using builtin functions `addsuffix` and `basename` (see [8.3 Functions for File Names](https://www.gnu.org/software/make/manual/html_node/File-Name-Functions.html)):
```make
SORTED_FILES := $(addsuffix .sorted, $(basename $(TEXT_FILES)))
```

### Section 2 - rules
#### Example 1 - generate one file from another

Let's make a rule to automatically create file `mydata1.sorted` by sorting the data in `data1.txt`:
```make
mydata1.sorted: data1.txt
    sort -o mydata1.sorted data1.txt
```

We can run the task from command line with:
```shell
$ make mydata1.sorted
sort -o mydata1.sorted data1.txt
```

* file `mydata1.sorted` *depends* on `data1.txt`
* we have defined a *rule* of how to create `mydata1.sorted` from `data1.txt`
* the command *will not* be executed if `mydata1.sorted` already exists and is newer than `data1.txt`
  
#### Example 2 - using patterns

We have may have several data files, so we can duplicate the rules:
```make
data1.sorted: data1.txt
    sort -o data1.sorted data1.txt
data2.sorted: data2.txt
    sort -o data2.sorted data2.txt
```

Our `Makefile` could become quite long, so instead we can use *patterns* (see [10.5.1 Introduction to Pattern Rules](https://www.gnu.org/software/make/manual/html_node/Pattern-Intro.html)):
```make
%.sorted: %.txt
	sort -o $@ $<
```

* `$@` is replaced with target name
* `$<` is replaced with dependency name

It could be invoked in the same way as a static rule:
```shell
$ make data1.sorted
sort -o data1.sorted data1.txt
```

#### Example 3 - sort all data files
We already have a list of files we want to generate, it is defined in `SORTED_FILES` variable above. Let's make a target, which will depend on all the desired sorted files:
```make
.PHONY: sort
sort: $(SORTED_FILES)
```
Note `.PHONY: sort` - we're telling `make`, that we're not actually going to generate a file named `sorted`, we just want all our dependencies to be available. All the depencies will be generated with the pattern rule defined above.
```shell
$ make sort
sort -o data1.sorted data1.txt
sort -o data2.sorted data2.txt
```

#### Example 4 - merge all data into one sorted file
We have a list of source files in `TEXT_FILES`. So if any of them is newer than `data.merged`, the targer file be re-generated:
```make
data.merged: $(TEXT_FILES)
	cat $(TEXT_FILES) | sort -o data.merged
```

#### Example 5 - routine automation

Now we know how to sort all files and created a sorted merged data. What if we want to it all at once? We can invoke two targets:

```shell
$ make sort data.merged
```

Or we can create a rule to make it all, many project follow this convention:

```make
.PHONY: all
all: sort data.merged
```

And call it:
```shell
$ make all
```

#### Example 6 - default target

We've defined many rules. We can make on of the default one, it will be executed if no rule is specified, otherwise the first one will be used:

```make
.DEFAULT_GOAL := all
```

So we can run just:
```shell
$ make 
sort -o data1.sorted data1.txt
sort -o data2.sorted data2.txt
cat data1.txt data2.txt | sort -o data.merged
```

#### Example 7 - good manners, cleaning up

Our script generates many files. We may want to reset the directory to its original state and clean up:

```make
.PHONY: clean
clean:
    rm -rf *.sorted *.merged
```

Let's run:
```shell
$make clean
rm -rf *.sorted *.merged
```
