#!/usr/bin/perl
# Serge Sharoff, April 2011
# The script converts the output of Treetagger to the CoNLL format expected
# by Malt
# It splits very long sentences (usually they are remainders of lists after
# cleaning)
# STDERR collects the sentence offsets for the text ids

$lineNumber=0;
$i=0;
$sl=0;
$start=0;
$metaFlag=1;

while (<>) {
    if (/^</) {
        if (/<text id="(.+?)"(.*)>/) {
            print STDERR "$i\t$1\t$2\n";
            print "\n";
        }
    } else {
        chomp;
        ($w,$p,$l)=split /\t/,$_;
        if (defined $l) {
            $t=substr($p,0,1);
            $sl++;
            if (($p eq 'SENT')) {
                $i++;
                $start=0;
                if ($metaFlag==0) {
                    $lineNumber++;
                    $out="$lineNumber\t$w\t$l\t$t\t$t\t$p\n";
                }
                else {
                    $out="1\t$w\t$l\t$t\t$t\t$p\n";
                }
                print $out;
                print "\n";
            } else {
                $metaFlag=0;
                $lineNumber++;
                $out="$lineNumber\t$w\t$l\t$t\t$t\t$p\n";
                print $out;
            }
        }
        $out="";
    }
}

if (!($p eq 'SENT')){
	print "\n";
}
print "END\n";
