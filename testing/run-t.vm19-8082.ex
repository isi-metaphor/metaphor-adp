#!/bin/bash

# Rebuild automatic KBs and run the test set for each language
# Jonathan Gordon, 2014-10-17

henry -m compile_kb -o \
    ../KBs/English/English_compiled_KB.da \
    ../KBs/English/en-examples.txt

henry -m compile_kb -o \
    ../KBs/Spanish/Spanish_compiled_KB.da \
    ../KBs/Spanish/es-examples.txt

henry -m compile_kb -o \
    ../KBs/Farsi/Farsi_compiled_KB.da \
    ../KBs/Farsi/fa-examples.txt

henry -m compile_kb -o \
    ../KBs/Russian/Russian_compiled_KB.da \
    ../KBs/Russian/ru-examples.txt

export IDENTIFIER=$RANDOM

scp ../KBs/English/English_compiled_KB.da \
    colo-vm19.isi.edu:kbs/en-$IDENTIFIER.da
scp ../KBs/Spanish/Spanish_compiled_KB.da \
    colo-vm19.isi.edu:kbs/es-$IDENTIFIER.da
scp ../KBs/Farsi/Farsi_compiled_KB.da \
    colo-vm19.isi.edu:kbs/fa-$IDENTIFIER.da
scp ../KBs/Russian/Russian_compiled_KB.da \
    colo-vm19.isi.edu:kbs/ru-$IDENTIFIER.da

./test -l en -i $IDENTIFIER \
    -u http://colo-vm19.isi.edu:8082 \
    data/en.test.tsv > en-t.vm19-8082.ex.txt &
./test -l es -i $IDENTIFIER \
    -u http://colo-vm19.isi.edu:8082 \
    data/es.test.tsv > es-t.vm19-8082.ex.txt &
./test -l fa -i $IDENTIFIER \
    -u http://colo-vm19.isi.edu:8082 \
    data/fa.test.tsv > fa-t.vm19-8082.ex.txt &
./test -l ru -i $IDENTIFIER \
    -u http://colo-vm19.isi.edu:8082 \
    data/ru.test.tsv > ru-t.vm19-8082.ex.txt &

for job in `jobs -p`; do
    echo $job
    wait $job || echo "Failed: $job."
done

ssh colo-vm19.isi.edu "rm kbs/en-$IDENTIFIER.da"
ssh colo-vm19.isi.edu "rm kbs/es-$IDENTIFIER.da"
ssh colo-vm19.isi.edu "rm kbs/fa-$IDENTIFIER.da"
ssh colo-vm19.isi.edu "rm kbs/ru-$IDENTIFIER.da"

echo "Done."
