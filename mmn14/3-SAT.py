from lab import *

formula = [["x", "y", "z"], ["x", "y", "z'"], ["x'", "y'", "w"], ["x", "z'", "w'"]]


variables = ["x", "y", "z", "w"]

con_vertices = [f"a{i}" for i in range(1, len(variables)+2)]

first_vertex = con_vertices[0]

comp_variables = [f"{var}'" for var in variables]

all_vertices = variables + comp_variables + con_vertices

sequences: Dict[str, str] = create_random_sequences(all_vertices)

edges = [(first_vertex, variables[0]), (first_vertex, comp_variables[0])]

edges += [(con_vertex, var) for con_vertex, var in zip(con_vertices[1:], variables[1:])]
edges += [(con_vertex, comp_var) for con_vertex, comp_var in zip(con_vertices[1:], comp_variables[1:])]
edges += [(var, con_vertex) for con_vertex, var in zip(con_vertices[1:], variables)]
edges += [(comp_var, con_vertex) for con_vertex, comp_var in zip(con_vertices[1:], comp_variables)]

edges_molecules: List[str] = create_edges(con_vertices[0], con_vertices[-1], edges, sequences)

vertices_molecules = [create_complementary(sequence) for sequence in sequences.values()]

AMOUNT = 400
DNA_strands = [DNAStrand(vertex, start_seq=False) for vertex in vertices_molecules for i in range(AMOUNT)]
DNA_strands += [DNAStrand(vertex, start_seq=False) for vertex in vertices_molecules[-5:] for i in range(AMOUNT)]
DNA_strands += [DNAStrand(edge, start_seq=False) for edge in edges_molecules[2:] for i in range(AMOUNT)]
DNA_strands += [DNAStrand(edge, start_seq=True) for edge in edges_molecules[:2] for i in range(AMOUNT)]

PRIMER1 = sequences["a1"]
PRIMER2 = create_complementary(sequences["a5"])
test_tube = TestTube(DNA_strands)
for key, seq in sequences.items():
    print(key, seq)
print()    
for edge1, edge2 in zip(edges_molecules, edges):
    print(edge1, edge2)
print()

formula_in_dna = [[sequences[symbol] for symbol in clause] for clause in formula]
test_tube.solve(PRIMER1, PRIMER2, formula_in_dna, num_of_muls=9)

results = test_tube.translate(sequences)

#check results
for result in results:
    result = result[1::2]
    for var in result:
        if var[-1] == "'":
            print(var[:-1], "false", end=" ")
        else:
            print(var, "true", end=" ")       
    print()    

