
from collections import defaultdict

class RtsTable(object):

    def __init__(self, primary_ids, sequences, genes=None, secondary_ids=None, control_prefix=None):
        assert len(primary_ids) == len(sequences)
        self.primary = {seq:id for seq, id in zip(sequences, primary_ids)}
        self.secondary = None
        self.genes_from_primary = None
        self.genes_from_secondary = None
        self.control_prefix = control_prefix

        if genes is not None and len(genes) > 0:
            assert len(genes) == len(primary_ids)
            self.genes_from_primary = {id:gene for id,gene in zip(primary_ids, genes)}

            if secondary_ids is not None and len(secondary_ids) > 0:
                assert len(secondary_ids) == len(primary_ids)
                self.secondary = {seq:id for seq, id in zip(sequences, secondary_ids)}
                self.genes_from_primary = {id:gene for id,gene in zip(primary_ids, genes)}
                self.genes_from_secondary = {id:gene for id,gene in zip(secondary_ids, genes)}

    @classmethod
    def from_file(cls, fn, control_prefix=None):
        primary, sequences, genes, secondary = list(), list(), list(), list()
        with open(fn) as handle:
            for line in handle:
                parts = line.strip().split("\t")
                if parts[0].startswith("RTSID"):
                    continue
                if len(parts) == 2:
                    rts_id, rts_seq = parts
                    primary.append( rts_id )
                    sequences.append( rts_seq )
                elif len(parts) == 5:
                    rts_id, rts_seq, gene, _, second_id = parts
                    primary.append( rts_id )
                    sequences.append( rts_seq )
                    genes.append( gene )
                    secondary.append( second_id )
                else:
                    raise Exception("ERROR: Invalid RTS file format - line has {} columns, but should have 2 or 5".format(len(parts)))
        return RtsTable(primary, sequences, genes, secondary, control_prefix)

    def has_genes(self):
        return (self.genes_from_primary is not None)

    def has_controls(self):
        return (self.control_prefix is not None)

    def get_gene(self, id):
        if not self.has_genes():
            raise Exception("ERROR: Can't get Gene name from RTS Table lacking gene information")

        try:
            gene = self.genes_from_primary[id]
            return gene
        except KeyError:
            pass
        
        if self.genes_from_secondary is not None:
            try:
                gene = self.genes_from_secondary[id]
                return gene
            except KeyError:
                pass
        
        return None

    def is_control(self, id):
        if not self.has_genes():
            raise Exception("ERROR: Can't get control status from RTS Table lacking gene information")
        if not self.has_controls():
            raise Exception("ERROR: Can't get control status from RTS Table lacking control information")

        gene = self.get_gene(id)
        if gene is None:
            return False
        return (gene.startswith(self.control_prefix))

    def probes_by_gene(self):
        if not self.has_genes():
            raise Exception("ERROR: Can't get control status from RTS Table lacking gene information")

        by_gene = defaultdict(list)
        for id, gene in self.genes_from_primary.items():
            by_gene[gene].append( id )

        return by_gene

    def translate(self, data, use_secondary=False):
        retval = defaultdict(int)

        if use_secondary:
            for seq, count in data.items():
                try:
                    id = self.secondary[seq]
                except:
                    raise Exception("ERROR: Invalid RTS sequence found '{}'".format(seq))
                retval[id] = count
        else:
            for seq, count in data.items():
                try:
                    id = self.primary[seq]
                except:
                    #raise Exception("ERROR: Invalid RTS sequence found '{}'".format(seq))
                    continue
                retval[id] = count

        return retval
