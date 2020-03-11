# Test Scripts
Jonathan Gordon, 2014-10-29

## Data

Unfortunately, our test data files can't be publicly released at this
time, so the testing infrastructure will require adaptation for use
outside of ISI.

## Use

Run `run-local` to run the test set on the Metaphor ADP Server, running
locally.

To see only the regressions between two runs, use the `logdiff` script.

## Modification

The wrapper scripts run all four languages simultaneously. If you want
to cause less server load -- at the expense of time -- comment out the `&`
at the end of each `test` invocation and they'll run sequentially.
