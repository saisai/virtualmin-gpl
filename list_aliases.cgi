#!/usr/local/bin/perl
# list_aliases.cgi
# Display users and aliases in a domain

require './virtual-server-lib.pl';
&ReadParse();
$d = &get_domain($in{'dom'});
&can_edit_domain($d) && &can_edit_aliases() || &error($text{'aliases_ecannot'});
@aliases = &list_domain_aliases($d, 1);
&ui_print_header(&domain_in($d), $text{'aliases_title'}, "");

# Create add links
($mleft, $mreason, $mmax, $mhide) = &count_feature("aliases");
if ($mleft != 0) {
	push(@links, [ "edit_alias.cgi?new=1&dom=$in{'dom'}",
		       $text{'aliases_add'} ]);
	}
push(@links, [ "mass_aedit_form.cgi?dom=$in{'dom'}",
	       $text{'aliases_emass'}, 'right' ]);

# Show reason why aliases cannot be added
if ($mleft != 0 && $mleft != -1 && !$mhide) {
	print "<b>",&text('aliases_canadd'.$mreason,$mleft),"</b><p>\n";
	}
elsif ($mleft == 0) {
	print "<b>",&text('aliases_noadd'.$mreason, $mmax),"</b><p>\n";
	}

# Make the table data
@table = ( );
if ($can_alias_comments) {
	($anycmt) = grep { $_->{'cmt'} } @aliases;
	}
foreach $a (sort { $a->{'from'} cmp $b->{'from'} } @aliases) {
	$name = $a->{'from'};
	$name =~ s/\@\S+$//;
	$name = "<i>$text{'alias_catchall'}</i>" if ($name eq "");
	$alines = "";
	$simple = &get_simple_alias($d, $a);
	foreach $v (@{$a->{'to'}}) {
		($anum, $astr) = &alias_type($v);
		if ($anum == 5 && $simple) {
			$msg = $simple->{'autotext'};
			$msg = substr($msg, 0, 100)." ..."
				if (length($msg) > 100);
			$alines .= &text('aliases_reply',
				"<i>".&html_escape($msg)."</i>");
			}
		else {
			$alines .= &text("aliases_type$anum",
			   "<tt>".&html_escape($astr)."</tt>");
			}
		}
	if (!@{$a->{'to'}}) {
		$alines = "<i>$text{'aliases_dnone'}</i>\n";
		}
	push(@table, [
		{ 'type' => 'checkbox', 'name' => 'd',
		  'value' => $a->{'from'} },
		"<a href='edit_alias.cgi?dom=$in{'dom'}&".
		"alias=$a->{'from'}'>$name</a>",
		$d->{'dom'},
		$alines,
		$anycmt ? ( $a->{'cmt'} ) : ( ),
		]);
	}

# Generate the table
print &ui_form_columns_table(
	"delete_aliases.cgi",
	[ [ "delete", $text{'aliases_delete'} ] ],
	1,
	\@links,
	[ [ "dom", $in{'dom'} ] ],
	[ "", $text{'aliases_name'},
	  $text{'aliases_domain'}, $text{'aliases_dests'},
          $anycmt ? ( $text{'aliases_cmt'} ) : ( ) ],
	100,
	\@table,
	undef, 0, undef,
	$text{'aliases_none'});

if ($single_domain_mode) {
	&ui_print_footer(&domain_footer_link($d),
			 "", $text{'index_return2'});
	}
else {
	&ui_print_footer(&domain_footer_link($d),
		"", $text{'index_return'});
	}

