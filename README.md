### Files:

* `output_Max2600_Min1700.txt` is the final file containing the amplification primers and amplicon number/length information for all genes, in tab-separatd plain text.

* `design_gene_amplification_primers.py` was used to generate output.txt from Creinhardtii_236_gene.txt and Creinhardtii_236_softmasked.fa*, using the following command: `design_gene_amplification_primers.py -m 1700 -a 2600 -F output_Max2600_Min1700.txt`

* `convert_gff_gene_data.py` was used to generate Creinhardtii_236_gene.txt from Creinhardtii_236_gene.gff3*, using the following command: `convert_gff_gene_data.py Creinhardtii_236_gene.gff3 Creinhardtii_236_gene.txt`

*The Creinhardtii_236_gene.gff3 and Creinhardtii_236_softmasked.fa files are too large to be included here, and can be downloaded from Phytozome 9 (Chlamydomonas v5.3 genome bulk download): ftp://ftp.jgi-psf.org/pub/compgen/phytozome/v9.0/Creinhardtii/.
