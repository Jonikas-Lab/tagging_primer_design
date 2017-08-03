#! /usr/bin/env python2.7

"""
Convert gff file to a simpler format giving CDS start-end and all exon start-ends, using just one splice variant per gene (the longest one, or the one with the most exons if lengths are equal).
The positions are 1-based, end-inclusive (so the first two bases of a sequence are 1-2, not 0-1 or 0-2 or 1-3).
NOTE: this requires the BCBio.GFF module (http://github.com/chapmanb/bcbb/tree/master/gff).
 -- Weronika Patena, 2014
USAGE: convert_gff_gene_data.py infile outfile
"""

# standard library
from __future__ import division
import sys
# other packages
from BCBio import GFF

### Constants
GFF_strands = {1:'+', -1:'-'}
N_chromosome_groups = 10

### Help functions

def split_into_N_sets_by_counts(ID_counts, N):
    """ Given an ID:count dictionary, return a list of sets of IDs with total counts balanced between the sets. """
    # make a sorted (high to low) list of (count,ID) tuples
    counts_IDs = sorted([(count,ID) for (ID,count) in ID_counts.iteritems()], reverse=True)
    output_counts_sets = [[0,set()] for i in range(N)]
    # now go over all IDs, adding an ID (and the corresponding count) to the smallest set each time
    for (count,ID) in counts_IDs:
        output_counts_sets[0][1].add(ID)
        output_counts_sets[0][0] += count
        output_counts_sets.sort()
    return [ID_set for [count,ID_set] in output_counts_sets]

def get_feature_start_end(feature_record):
    """ Get the start and end feature positions as numbers, 1-based, end-inclusive (so the first two bases are 1-2).

    BCBio uses 0-based end-exclusive positions, so the first two bases are 0-2.
    """
    return (feature_record.location.start.position+1, feature_record.location.end.position)

def get_gene_start_end_excluding_UTRs(mRNA_record):
    """ Get the start of the first CDS feature and the end of the last one, (as numbers, 1-based, end-inclusive).

    If gene has no mRNAs or more than one, raise exception.

    BCBio uses 0-based end-exclusive positions, so the first two bases are 0-2; this uses 1-based end-inclusive, so they're 1-2.
    """
    features = mRNA_record.sub_features
    CDS_positions = [get_feature_start_end(feature) for feature in features if feature.type=='CDS']
    CDS_starts, CDS_ends = zip(*CDS_positions)
    return min(CDS_starts), max(CDS_ends)

### Main function

try:
    infile, outfile = sys.argv[1:]
except ValueError:
    print __doc__
    sys.exit("Error: Needs exactly one input and one output file!")

examiner = GFF.GFFExaminer()

# parsing the whole GFF file at once takes a ton of memory, so split it into sets
with open(infile) as INFILE:
    GFF_limit_data = examiner.available_limits(INFILE)
    chromosomes_and_counts = dict([(c,n) for ((c,),n) in GFF_limit_data['gff_id'].items()])

chromosome_sets = split_into_N_sets_by_counts(chromosomes_and_counts, N_chromosome_groups)

with open(outfile, 'w') as OUTFILE:
    for chromosome_set in chromosome_sets:
        genefile_parsing_limits = {'gff_id': list(chromosome_set)}
        with open(infile) as INFILE:
            for chromosome_record in GFF.parse(INFILE, limit_info=genefile_parsing_limits):
                for gene in chromosome_record.features:
                    if not len(gene.sub_features):      sys.exit("Error: gene %s has no mRNAs!"%gene.id)
                    # look at all mRNAs if multiple are present; pick longest one and then one with most exons
                    subfeature_lengths_Nexons = []
                    for N, mRNA in enumerate(gene.sub_features):
                        if not mRNA.type=='mRNA':       sys.exit("Error: gene %s has non-mRNA thing!"%gene.id)
                        if len(mRNA.sub_features)==0:   sys.exit("Error: gene %s mRNA has no features!"%gene.id)
                        start, end = get_gene_start_end_excluding_UTRs(mRNA)
                        length = end-start+1
                        N_exons = len([f for f in mRNA.sub_features if f.type=='CDS'])
                        subfeature_lengths_Nexons.append((length, N_exons, N))
                    best_mRNA = gene.sub_features[sorted(subfeature_lengths_Nexons)[-1][-1]]
                    # grab start and end positions - those are the earlier and later positions in the genome, 
                    #  so if the gene is -strand, the end is 5'!
                    start, end = get_gene_start_end_excluding_UTRs(best_mRNA)
                    CDS_positions = [get_feature_start_end(f) for f in mRNA.sub_features if f.type=='CDS']
                    OUTFILE.write('\t'.join([gene.id, chromosome_record.id, GFF_strands[mRNA.strand], str(start), str(end)] + ['%s-%s'%(start,end) for (start,end) in CDS_positions]) + '\n')
