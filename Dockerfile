FROM debian:8.10

MAINTAINER Jonathan Gordon <jgordon@isi.edu>

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8


# Install basic system dependencies.

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -q -y --fix-missing && \
    apt-get install -q -y --fix-missing --no-install-recommends \
        bzip2 ca-certificates g++ git-core graphviz libsqlite3-dev make \
        openjdk-7-jre python-dev python-lxml python-nltk swi-prolog wget

RUN apt-get clean -q


# Install Gurobi.

ENV GUROBI_INSTALL /adp/external-tools/gurobi
ENV GUROBI_HOME $GUROBI_INSTALL/linux64
ENV PATH $PATH:$GUROBI_HOME/bin
ENV CPLUS_INCLUDE_PATH $GUROBI_HOME/include:$CPLUS_INCLUDE_PATH
ENV LD_LIBRARY_PATH $GUROBI_HOME/lib:$LD_LIBRARY_PATH
ENV LIBRARY_PATH $GUROBI_HOME/lib:$LIBRARY_PATH
ENV GRB_LICENSE_FILE $GUROBI_INSTALL/license/gurobi.lic

RUN mkdir -p $GUROBI_INSTALL && \
    wget http://packages.gurobi.com/5.6/gurobi5.6.3_linux64.tar.gz && \
    tar xvzf gurobi5.6.3_linux64.tar.gz && \
    mv gurobi563/linux64 $GUROBI_INSTALL && \
    mkdir $GUROBI_HOME/scripts && \
    rm -rf $GUROBI_HOME/docs && \
    rm -rf $GUROBI_HOME/examples && \
    rm -rf $GUROBI_HOME/src && \
    rm -rf gurobi563 && \
    rm -f gurobi5.6.3_linux64.tar.gz


# Install Henry.

WORKDIR /adp/external-tools

RUN git clone https://github.com/isi-metaphor/henry-n700.git henry

WORKDIR /adp/external-tools/henry

RUN make -B


## Install Boxer.

WORKDIR /adp/external-tools

RUN git clone https://github.com/jgordon/boxer

RUN cd boxer && \
    make && \
    make bin/boxer && \
    make bin/tokkie

RUN cd boxer && \
    tar xvjf models-1.02.tar.bz2 && \
    rm models-1.02.tar.bz2


# Add the application code to the Docker image.

COPY KBs /adp/KBs
COPY external-tools /adp/external-tools
COPY installation /adp/installation
COPY pipelines /adp/pipelines
COPY testing /adp/testing


RUN yes yes | /adp/installation/scripts-linux/setenv-linux64.py /adp


# Done

WORKDIR /adp
