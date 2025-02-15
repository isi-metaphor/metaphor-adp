#!/bin/bash

export GUROBI_HOME=$ADP_HOME/external-tools/gurobi/linux32
export GRB_LICENSE_FILE=$ADP_HOME/external-tools/gurobi/license/gurobi.lic

if [ X"$PATH" == X ]; then
    export PATH=$GUROBI_HOME/bin
else
    export PATH=$PATH:$GUROBI_HOME/bin
fi

if [ X"$LD_LIBRARY_PATH" == X ]; then
    export LD_LIBRARY_PATH=$GUROBI_HOME/lib
else
    export LD_LIBRARY_PATH=$GUROBI_HOME/lib:$LD_LIBRARY_PATH
fi

if [ X"$LIBRARY_PATH" == X ]; then
    export LIBRARY_PATH=$GUROBI_HOME/lib
else
    export LIBRARY_PATH=$GUROBI_HOME/lib:$LIBRARY_PATH
fi

if [ X"$CPLUS_INCLUDE_PATH" == X ]; then
    export CPLUS_INCLUDE_PATH=$GUROBI_HOME/include:/usr/include/python2.7
else
    export CPLUS_INCLUDE_PATH=$GUROBI_HOME/include:/usr/include/python2.7:$CPLUS_INCLUDE_PATH
fi
