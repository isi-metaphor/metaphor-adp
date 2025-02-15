#!/usr/bin/env python2.7

import os
import sys

if len(sys.argv) != 2:
    print("Usage:" + sys.argv[0] + " install_dir")
    sys.exit()

install_dir = sys.argv[1]

setvars = raw_input("This script modifies your .bash_profile file, and sets "
                    "environment variables\n"
                    "relevant for this application. Continue? [yes/no] ")

if setvars != "yes":
    sys.exit()

bashrc_file = os.environ['HOME'] + "/.bash_profile"

with open(bashrc_file, 'a+') as f:
    f.write("\n# Metaphor ADP\n")
    f.write("export ADP_HOME=" + install_dir + "\n")
    f.write("export BOXER_DIR=" + install_dir + "/external-tools/boxer\n")
    f.write("export HENRY_DIR=" + install_dir + "/external-tools/henry\n")
    f.write("export GUROBI_HOME=/Library/gurobi563/mac64\n")
    f.write("export GRB_LICENSE_FILE=$ADP_HOME/gurobi.lic\n")

    if os.environ.get('PATH') is None:
        f.write("export PATH=/usr/local/bin:$GUROBI_HOME/bin\n")
    else:
        f.write("export PATH=$PATH:/usr/local/bin:$GUROBI_HOME/bin\n")

    if os.environ.get('LD_LIBRARY_PATH') is None:
        f.write("export LD_LIBRARY_PATH=$GUROBI_HOME/lib\n")
    else:
        f.write("export LD_LIBRARY_PATH=$GUROBI_HOME/lib:$LD_LIBRARY_PATH\n")

    if os.environ.get('LIBRARY_PATH') is None:
        f.write("export LIBRARY_PATH=$GUROBI_HOME/lib\n")
    else:
        f.write("export LIBRARY_PATH=$GUROBI_HOME/lib:$LIBRARY_PATH\n")

    if os.environ.get('CPLUS_INCLUDE_PATH') is None:
        f.write("export CPLUS_INCLUDE_PATH="
                "$GUROBI_HOME/include:/usr/include/python2.7\n")
    else:
        f.write("export CPLUS_INCLUDE_PATH="
                "$GUROBI_HOME/include:/usr/include/python2.7:"
                "$CPLUS_INCLUDE_PATH\n")
