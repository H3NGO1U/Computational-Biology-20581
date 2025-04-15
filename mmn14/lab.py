from typing import List, Tuple, Dict
import random 

complementary_dict = {"A":"T", "T":"A", "G":"C", "C":"G"}
NUCLEOTIDES = ["A", "T", "G", "C"]
BASE = 20
PRINT_LEN = 100
NUM_OF_REPS = 1

class Nucleotide:
    def __init__(self, prev_nucleotide, next_nucleotide, value: str, connected_nucleotide = None):
        self.prev_nucleotide = prev_nucleotide
        self.next_nucleotide = next_nucleotide
        self.value = value
        self.connected_nucleotide = connected_nucleotide

    def connect(self, nuc_to_connect):
        self.connected_nucleotide = nuc_to_connect 
        nuc_to_connect.connected_nucleotide = self   

    def __str__(self):
        return self.value
    
    def print_all(self):
        temp = self
        while temp:
            print(temp.value, end=" ")
            temp = temp.next_nucleotide
        print()    


class Primer:
    def __init__(self, start_nuc: Nucleotide, backwards: bool = False):
        self.start_nuc = start_nuc
        self.backwards = backwards


class DNAStrand:
    def __init__(self, sequence: str = None, start_seq: bool = None, start_nuc: Nucleotide = None):
        if start_nuc:
            self.start_nucleotide = start_nuc
            return
        sequence = sequence.strip().upper()
        if len(sequence) == 0:
            raise Exception(f"DNA sequence should not be empty")
        self.start_nucleotide = Nucleotide(prev_nucleotide = None, next_nucleotide = None, value = sequence[0])
        self.free_nucs = [self.start_nucleotide]
        temp = self.start_nucleotide
        for i, nucleotide in enumerate(sequence):
            if i == 0:
                continue
            if nucleotide not in NUCLEOTIDES:
                raise Exception("DNA sequence should contain only A, T, G, C")    
            temp.next_nucleotide = Nucleotide(temp, None, nucleotide)
            temp = temp.next_nucleotide
            if start_seq and i == BASE:
                self.free_nucs.append(temp)
            elif not start_seq and i == BASE // 2:
                self.free_nucs.append(temp)    

        self.end_nucleotide = temp    
                

    def get_free_nucs(self) -> List[Nucleotide]:
        return self.free_nucs
    
    def denaturation(self):
        """
        The DNA is heated to 95 degrees, 
        and it causes the strands to seperate from each other.
        """  
        temp = self.start_nucleotide
        while temp:
            temp.connected_nucleotide = None
            temp = temp.next_nucleotide

    def annealing(self, primer1: str, primer2: str):
        """
        cool to 55 degrees, do stuff with primers, return 2 DNA molecules if success
        """
        primers = []
        if not primer1 or not primer2 or len(primer1) != len(primer2) != BASE:
            raise Exception(f"Primers should be of len {BASE}")
        temp = self.start_nucleotide
        while temp:
            sequence = ""
            length = BASE
            cur_start = temp
            prev = None
            while temp and length > 0:
                sequence += temp.value
                prev = temp
                temp = temp.next_nucleotide 
                length -= 1
            if sequence == primer1:
                primers.append(Primer(cur_start, backwards=False)) 
            elif sequence == primer2:
                primers.append(Primer(prev, backwards=True))        
        return primers
    
    def __str__(self):
        first_strand = ""
        temp: Nucleotide = self.start_nucleotide
        second_strand = ""
        while temp:
            first_strand += temp.value
            if temp.next_nucleotide:
                first_strand += "-"
            else:
                first_strand += " "   
            con_to_nuc = temp.connected_nucleotide  
            if con_to_nuc:
                second_strand += temp.connected_nucleotide.value
                if con_to_nuc.next_nucleotide:
                    second_strand += "-"
                else:
                    second_strand += " "
            else:
                second_strand += "  "        
            temp = temp.next_nucleotide
        middle = ""    
        for base in second_strand:
            if base in NUCLEOTIDES:
                middle += "|"
            else:
                middle += " " 
        n = len(first_strand)
        result = first_strand[:PRINT_LEN] + "\n" + middle[:PRINT_LEN] + "\n" + second_strand[:PRINT_LEN]
        while n > PRINT_LEN:
            result += "\n"
            first_strand = first_strand[PRINT_LEN:]
            middle = middle[PRINT_LEN:]
            second_strand = second_strand[PRINT_LEN:]
            result += first_strand[:PRINT_LEN] + "\n" + middle[:PRINT_LEN] + "\n" + second_strand[:PRINT_LEN]
            n -= PRINT_LEN
        result += "\n\n\n\n"
        return result    

    def get_sequence(self) -> str:
        sequence = ""
        temp = self.start_nucleotide
        while temp:
            sequence += temp.value
            temp = temp.next_nucleotide
        return sequence    

class TestTube:
    def __init__(self, DNA_strands: List[DNAStrand]):
        self.pool = []
        self.strands = DNA_strands
        for DNA_strand in DNA_strands:
            self.pool += DNA_strand.get_free_nucs()

    def denaturation(self):
        for strand in self.strands:
            strand.denaturation()

    def annealing(self, start_primer, end_primer) -> List[Nucleotide]:
        primers = []
        for strand in self.strands:
            primers += strand.annealing(start_primer, end_primer)
        return primers
    
    def polymerase(self, primers: List[Primer]):
        for primer in primers:
            cur_nuc = primer.start_nuc
            if primer.backwards:
                next_nuc = None
                while cur_nuc and not cur_nuc.connected_nucleotide:
                    cur_nuc.connected_nucleotide = Nucleotide(None, next_nuc, complementary_dict[cur_nuc.value], cur_nuc)
                    if cur_nuc == primer.start_nuc:
                        strand = DNAStrand(start_nuc=cur_nuc)
                    if next_nuc:
                        next_nuc.prev_nucleotide = cur_nuc.connected_nucleotide
                        cur_nuc.connected_nucleotide.next_nucleotide = next_nuc
                    next_nuc = cur_nuc.connected_nucleotide
                    cur_nuc = cur_nuc.prev_nucleotide
                strand.end_nucleotide = strand.start_nucleotide
                strand.start_nucleotide = next_nuc 

            else:
                prev_nuc = None    
                while cur_nuc and not cur_nuc.connected_nucleotide:
                    cur_nuc.connected_nucleotide = Nucleotide(prev_nuc, None, complementary_dict[cur_nuc.value], cur_nuc)
                    if cur_nuc == primer.start_nuc:
                        strand = DNAStrand(start_nuc=cur_nuc)
                    if prev_nuc:
                        prev_nuc.next_nucleotide = cur_nuc.connected_nucleotide
                        cur_nuc.connected_nucleotide.prev_nucleotide = prev_nuc
                    prev_nuc = cur_nuc.connected_nucleotide
                    cur_nuc = cur_nuc.next_nucleotide
                strand.end_nucleotide = prev_nuc    
            self.strands.append(strand)

    def ligation(self):
        """
        Combines and repairs DNA strands, create potential paths
        """
        random.shuffle(self.pool)
        n = len(self.pool)
        i = 0
        while i < n:
            j = i + 1
            while j < n: 
                length = check_if_complementary(self.pool[i], self.pool[j])
                if length > 0:
                    nuc1, nuc2 = self.pool[i], self.pool[j]
                    self.pool.remove(nuc1)
                    self.pool.remove(nuc2)
                    for x in range(length):
                        nuc1.connect(nuc2)
                        nuc2.connect(nuc1)
                        nuc1, nuc2 = nuc1.next_nucleotide, nuc2.next_nucleotide
                    n -= 2
                    break
                j += 1
            i += 1        
        for strand in self.strands:
            end_nuc = strand.end_nucleotide
            if end_nuc.connected_nucleotide and end_nuc.connected_nucleotide.next_nucleotide and end_nuc.connected_nucleotide.next_nucleotide.connected_nucleotide and not end_nuc.next_nucleotide:
                end_nuc.next_nucleotide = end_nuc.connected_nucleotide.next_nucleotide.connected_nucleotide
                end_nuc.next_nucleotide.prev_nucleotide = end_nuc

    def gel_elecro(self, num_of_muls):
        new_strands = []        
        for strand in self.strands:
            if len(strand.get_sequence())==BASE*num_of_muls:
                new_strands.append(strand)
        self.strands = new_strands

    def pcr(self, primer1: str, primer2: str):
        for i in range(NUM_OF_REPS):
            self.denaturation()
            primers = self.annealing(primer1, primer2)
            self.polymerase(primers)

    def perform_magnetic_in_row(self, formulas: List[str]) -> List[str]:
        #cache for efficiency
        ok = []
        not_ok = []
        for strand in self.strands:
            if strand not in ok and strand not in not_ok:
                for clause in formulas:
                    clause_sat = False
                    sequence = strand.get_sequence()
                    for symbol in clause:
                        if symbol in sequence:
                            clause_sat = True
                            break
                    if not clause_sat:    
                        not_ok.append(sequence)
                        #clause not satisfied - strand is not ok
                        break
                if clause_sat:    
                    ok.append(strand)                      
        self.strands = ok
    
    def solve(self, primer1: str, primer2: str, formulas: List[str], num_of_muls: int):
        self.ligation()
        self.pcr(primer1, primer2)
        self.gel_elecro(num_of_muls)
        self.perform_magnetic_in_row(formulas)
        print(self)

    def translate(self, sequences):
        done = []
        result = []
        for strand in self.strands:
            cur_res = []
            sequence = strand.get_sequence()
            if sequence not in done:
                for index in range(len(sequences)):
                    found = False
                    for key, value in sequences.items():
                        if value == sequence[index*BASE:(index+1)*BASE]:
                            cur_res.append(key)
                            found = True
                    if not found:
                        break 
                done.append(sequence)                  
            if cur_res:
                result.append(cur_res)
        return result        

    def __str__(self):
        result = ""
        for strand in self.strands:
            result += str(strand)
        return result

    def print_all_sequences(self):
        for strand in self.strands:
            print(strand.get_sequence())


def create_complementary(sequence: str) -> str:
    complementary = ""
    for nuc in sequence:
        complementary += complementary_dict[nuc]
    return complementary

def create_random_sequences(vertices: List[str]) -> Dict[str, str]:   
    sequences = {}
    for vertex in vertices:
        next_seq = ""
        for j in range(BASE):
            next_seq += NUCLEOTIDES[random.randint(0, 3)]
        sequences[vertex] = next_seq 
    return sequences

def create_edges(start_vertex: str, end_vertex: str, edges: List[Tuple[str, str]], vertices_molecules: Dict[str, str]) -> List[str]:
    edges_molecules = []
    for v1, v2 in edges:
        cur_edge = ""
        if v1 not in vertices_molecules or v2 not in vertices_molecules:
            raise Exception("Illegal vertex in edge")
        if v1 == start_vertex:
            #start vertex should be added as whole
            cur_edge += vertices_molecules[start_vertex]
        else:
            #for any other vertex, add 10 last bases of v1
            cur_edge += vertices_molecules[v1][BASE//2:]
        if v2 == end_vertex:
            #end vertex should be added as whole
            cur_edge += vertices_molecules[end_vertex]
        else:
            #for any other vertex, add 10 first bases of v2
            cur_edge += vertices_molecules[v2][:BASE//2]
        edges_molecules.append(cur_edge)
    return edges_molecules            

def check_if_complementary(start_seq1: Nucleotide, start_seq2: Nucleotide):   
    index = 0
    while index < BASE and start_seq1 and start_seq2:
        base1, base2 = start_seq1.value, start_seq2.value
        if complementary_dict[base1] != base2:
            if index >= BASE // 2:
                return BASE // 2
            return 0
        index += 1
        start_seq1, start_seq2 = start_seq1.next_nucleotide, start_seq2.next_nucleotide
    if index > BASE // 2:    
        return BASE
    return BASE // 2


    
        
    


