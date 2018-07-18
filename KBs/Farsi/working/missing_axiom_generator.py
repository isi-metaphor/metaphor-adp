#!/usr/bin/env python2.7

import codecs
import sys
import os

input_dir = sys.argv[1]
source_axiom_file = codecs.open(sys.argv[2], encoding='utf-8')
target_axiom_file = codecs.open(sys.argv[3], encoding='utf-8')
output_file = sys.stdout

var_name_values = {
    "source": "",
    "target": "",
    "sourceConceptSubDomain": "",
    "sourceFrame": "",
    "targetConceptDomain": "",
    "targetConceptSubDomain": "",
    "targetFrame": ""
}

for json_file_name in os.listdir(input_dir):
    abs_file_path = "%s/%s"%(input_dir, json_file_name)
    with codecs.open(abs_file_path, encoding='utf-8') as json_file:
        lines = json_file.readlines()
        is_first_source_node = True
        for var_name in var_name_values:
            for line in lines:
                if var_name in line:
                    if var_name == "source" and not is_first_source_node:
                        continue
                    var_name_values[var_name] = get_value(line)
                    if var_name == "source":
                        is_first_source_node = False

# Now we have read all the name_values.
# Read the axiom files and compare against the name_values.

source_ax_lines = source_axiom_file.readlines()
target_ax_lines = target_axiom_file.readlines()

source_axiom_file.close()
target_axiom_file.close()
