# Test Scripts
Jonathan Gordon, 2014-10-29

## Use

The scripts to run are run-*, which are shell scripts that compile the
relevant KBs, scp them to the right machine, then run 'test' with
appropriate arguments, and delete the KBs.

'run-d-*' run the development sets.
'run-t-*' run the test sets.

To see only the regressions between two runs, use the 'logdiff' script.


## Set Up

Make a symbolic link 'data' in this directory to Dropbox/ISI Metaphor
OY2/evalsets/lcc_20140801 or modify the scripts to use the test CSV
files you want.

Other users should modify the path in 'test' for the KBs on colo-vm19,
which defaults to a directory in my home directory. For colo-pm4, the
wrapper scripts specify the 'kbs' dir. in the metaphor user's home,
which should be fine.


## Modification

The wrapper scripts run all four languages simultaneously. If you want
to cause less server load and don't care about time, comment out the '&'
at the end of each 'test' invocation and they'll run sequentially.
