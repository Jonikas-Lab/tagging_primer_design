### Files:

* `output_Max2600_Min1700.txt` is the final file containing the amplification primers and amplicon number/length information for all genes, in tab-separated plain text.

* `design_gene_amplification_primers.py` was used to generate output.txt from Creinhardtii_236_gene.txt and Creinhardtii_236_softmasked.fa*, using the following command: `design_gene_amplification_primers.py -m 1700 -a 2600 -F output_Max2600_Min1700.txt` (default values were used for the input files and additional options, which can be seen by running `design_gene_amplification_primers.py --help`)

* `convert_gff_gene_data.py` was used to generate Creinhardtii_236_gene.txt from Creinhardtii_236_gene.gff3*, using the following command: `convert_gff_gene_data.py Creinhardtii_236_gene.gff3 Creinhardtii_236_gene.txt`

*The Creinhardtii_236_gene.gff3 and Creinhardtii_236_softmasked.fa files are too large to be included here, and can be downloaded from Phytozome 9 (Chlamydomonas v5.3 genome bulk download): ftp://ftp.jgi-psf.org/pub/compgen/phytozome/v9.0/Creinhardtii/.

### Details:

The command-line output from running `design_gene_amplification_primers.py -m 1700 -a 2600 -F output_Max2600_Min1700.txt` providing a summary of the results and problems was as follows:

    Warning: gene g4491 doesn't start with ATG!
    Warning: gene g5570 doesn't start with ATG!
    Warning: gene Cre06.g264150 doesn't start with ATG!
    Warning: gene g7573 doesn't start with ATG!
    Warning: gene g13826 doesn't start with ATG!
    Warning: gene g18408 doesn't start with ATG!
    Warning: gene g18269 doesn't start with ATG!
    Warning: gene g11595 doesn't start with ATG!
    Warning: gene g18363 doesn't start with ATG!
    Warning: gene g18368 doesn't start with ATG!
    DONE! Designed primers for 17737 genes, with a total of 38796 amplicons; 1-32 amplicons per gene; amplicon sizes are 162-2601bp.
    Details on iffy cases: 4346 genes were smaller than the min amplicon size, and there were 4410 cases where it was impossible to put a junction in an exon while staying within the amplicon size ranges, so it was placed in an intron.
