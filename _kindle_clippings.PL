package Nagler::Kindle;
use strict;
use Encode ();
use POSIX ();
use Text::Wrap ();
my($books) = {};
my($in_text) = 0;
my($book);
my($rec);
my($punct) = qr{[.\?\!\'\"]};
my($now) = POSIX::strftime('%Y-%m-%dT%H:00:00Z', gmtime());
foreach my $line (<>) {
    chomp($line);
    # first char on line by kindle
    $line =~ s{^\357\273\277}{};
    $line = Encode::decode('UTF-8', $line);
    $line =~ s/[\x{2010}-\x{2015}]/--/g;
    $line =~ s/[\x{2018}-\x{201B}]/'/g;
    $line =~ s/[\x{201C}-\x{201F}]/"/g;
    $line =~ s/[\x{2026}]/.../g;
    $line =~ s/[\x{2020}]/+/g;
    $line =~ s/\x{8094}/--/g;
    $line =~ s/[\x{0aa3}]/GBP /g;
    $line =~ s/\p{IsSpacePerl}+/ /g;
    $line =~ s/([^[:ascii:]]+)/'<FIXME ' . sprintf('%x', ord($1)) . '>'/eg;
    $line =~ s/\r//g;
    # Trim footnotes
    $line =~ s/(?<=[^\d]$punct)\d+//sg;
    $line =~ s/^\s+|\s+$//g;
    if ($line =~ m{^-(?:\s+Your)?\s+(\w+)\s+(?:on\s+)?(Loc|Page)\S*\s+(\w+)(?:-(\w+))?(?:\s+\|\s+Location\s+(\d+)(?:-(\d+))?)?}i) {
        my($type, $unit, $start, $end, $ls, $le) = ($1, $2, $3, $4, $5, $6);
        $unit = $unit =~ /^p/i ? 'p' : 'k';
        $rec = {type => $type};
        $in_text = 1;
        if ($type =~ /note/i) {
            $rec->{is_highlight} = 0;
            $rec->{start} = $rec->{end} = $ls || $start;
            $rec->{label} = "NOTE: ";
        }
        elsif ($type =~ /highlight/i) {
            $rec->{is_highlight} = 1;
            # overridden by kindle location below
            $rec->{label} = "[$unit$start] ";
            if ($ls) {
                $start = $ls;
                $end = $le || $ls;
            }
            # Override: Use kindle locations, because pages are not
            # standardized on kindle so hard to find.
            $rec->{label} = "[k$start] ";
            $rec->{start} = $start;
            $end ||= $start;
            foreach my $x (1 .. length($end)) {
                chop($start);
            }
            $start .= $end;
            $rec->{end} = $start;
        }
        elsif ($type =~ /bookmark/i) {
            # don't save, just parse and toss
            next;
        }
        else {
            die(qq{type "$type" unknown: $line});
        }
        push(@{$book->{records} ||= []}, $rec);
    }
    elsif ($in_text) {
        if ($line =~ /^=======/) {
            $rec = \('invalid');
            $in_text = 0;
            next;
        }
        if ($line) {
            my($p) = '';
            if ($rec->{is_highlight}) {
                $p .= '> ';
            }
            if (!$rec->{text}) {
                $p .= $rec->{label};
            }
            $rec->{text} .= $p . $line . "\n";
        }
        elsif ($rec->{text}) {
            $rec->{text} .= "\n";
        }
    }
    # Second form was for The Shadow of the Sun, which isn't in usual form
    elsif ($line =~ /^_?(.+)\((.+)\)$/ || $line =~ /^([A-Z][a-z]+(?:[A-Za-z\s]+)[A-Z][a-z]+)$/) {
        my($title, $author) = ($1, $2);
        $author ||= 'No Author';
        $title =~ s/^\s+|\s+$//g;
        $author =~ s/^\s+|\s+$//g;
        $author = join(' ', reverse(split(/\s*,\s*/, $author)));
        next
            if $book = $books->{$title . $author};
        ($book = ($books->{$title . $author} ||= {}))->{prefix}
            = <<"EOF";
---
layout: post
title: "BookNotes: $title"
date: $now
---
By $author, Some Publisher, Month 1, 201x, ISBN

EOF
        $book->{title} = $title;
    }
}

my($data) = '';
foreach $book (values(%$books)) {
    next
	unless $book->{records};
    my($records) = [];
    my($prev);
    foreach my $curr (sort({
	$a->{end} <=> $b->{end}
	    || $a->{type} cmp $b->{type}
	} @{$book->{records}})
    ) {
	if (!$curr->{text}) {
	    $curr = undef;
	}
	next
	    unless $prev && $prev->{is_highlight} eq $curr->{is_highlight};
	if ($prev->{start} eq $curr->{start}) {
            unless ($prev->{text} eq $curr->{text}) {
                print(STDERR "TITLE: $book->{title}\nREPLACED: $prev->{text}WITH: $curr->{text}\n\n");
            }
	    %$prev = %$curr;
	}
 	elsif ($prev->{is_highlight}
 	    and $prev->{end} == $curr->{start}
 	    || $prev->{end} + 1 == $curr->{start}
 	) {
 	    $prev->{text} .= "\nFIXME\n" . $curr->{text};
 	}
	else {
	    next;
	}
	$curr = undef;
    }
    continue {
	if ($curr) {
	    $prev = $curr;
	    push(@$records, $curr);
	}
    }
    $data .= $book->{prefix}
	. join("\n\n", map(
	    {
		my($t) = $_->{text};
		$t =~ s/^[\s\n]+|[\n\s]+$//sg;
		if ($_->{is_highlight}) {
		    foreach my $qr (
                        # something like: "white middle-class neighborhoods"
                        # should not be trimmed.
			qr{(?<!$punct)([A-Z0-9][a-z0-9\s]*)$}is,
			qr{^([a-z].*?$punct\)?\s+)}s,
		    ) {
                        my($x) = $t;
                        # Single character is "don't" or something.
                        # Check length of trimmed text, because sometimes
                        # clippings miss period, and the data strips too much.
                        if ($x =~ s/$qr//) {
                            if (length($1) > 1 && length($1) < 15) {
                                print(STDERR "TITLE: $book->{title}\nTRIMMED: $_->{label} $1\nFROM: $t\n\n");
                                $t = $x;
                            }
                            elsif ($t !~ m{$punct\s*$}s) {
                                $t .= "\nFIXME";
                            }
                        }
		    }
                    $t = Text::Wrap::wrap('', '> ', $t);
		}
		$t;
	    } @$records,
	))
	. "\n\n";
}
$data =~ s/\n\n+/\n\n/sg;
print($data);
