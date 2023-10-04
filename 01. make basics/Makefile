######
# This manual is highly recommended:
# https://www.gnu.org/software/make/manual/html_node/index.html

######
# Section 1 - Variables

# list of files to process, uses makefile function wildcard
# https://www.gnu.org/software/make/manual/html_node/File-Name-Functions.html
TEXT_FILES := $(wildcard *.txt)

# list of files to generate - *.sorted for each *.txt
SORTED_FILES := $(addsuffix .sorted, $(basename $(TEXT_FILES)))

# what to do by default
.DEFAULT_GOAL := all

######
# Section 2 - rules
# General syntax:
# target_name: dependency names
#     shell commands to build target
#
# both targets and dependecies are file names, unless stated otherwise (see .PHONY below)
# you can build any target you want by calling command:
# make target_name

# Example 1 - an explicit target:
# file mydata.sorted DEPENDS on file data1.txt
# - creates mydata.sorted from sorted data1.txt
# - recreates mydata.sorted if data1.txt is newer than mydata.sorted
mydata1.sorted: data1.txt
	sort -o mydata1.sorted data1.txt

# Example 2 - pattern target:
# f- iles *.sorted DEPEND on files *.txt
# - does the same as above for each pair of *.txt/*.sorted files
# - could be called by name of each match instance with command:
# make data1.sorted
%.sorted: %.txt
	sort -o $@ $<

# Example 3 - file depends on several files
data.merged: $(TEXT_FILES)
	cat $(TEXT_FILES) | sort -o data.merged

# Example 4 - "phony" target:
# - sort all data files if needed
# - does not create any file or directory
# - can depend on other targets, which may need to be generated
.PHONY: sort
sort: $(SORTED_FILES)

# Example 5 - "all" target:
# Typically your project may include "all" target - just build or generate everything
# Since no "all" file is actually generated, it is a phony target as well
.PHONY:
all: $(SORTED_FILES) data.merged

# Example 6 - good manners:
# Typically your project may include "clean" target, which deletes all generated files
.PHONY:
clean:
	rm -rf *.sorted *.merged
