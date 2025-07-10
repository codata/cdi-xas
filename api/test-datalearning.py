from datalearning import DataLearning
datafile = "resources/xdi_example_wds.jsonld"
datafile = "/home/tikhonov/projects/computer-eyes/resources/xdi_example_ss.jsonld"
configpath = "/home/tikhonov/projects/computer-eyes/resources/"
data = DataLearning(configpath, datafile, format="json-ld")
data.load_data()
data.get_data()

#print(data.get_data_as_pandas())
#print(data.serialize_data(format="json-ld"))
#x = data.lookup_subject("http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/InstanceVariable")
#print(x)

#data.add_permanent_schema('dataset')
#print(data.export(format="json-ld"))
condition = "http://www.w3.org/2004/02/skos/core#narrower"
condition = "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/stateProvince" #DateRange-startDate" #startDate" #startLine"
condition = "InstanceVariable"
#condition = None
triples = data.triple_by_triple(data.fullgraph, search=condition)
for triple in triples:
    print(triple)

print(data.get_type(condition, data.fullgraph))
data.get_related_triples(data.fullgraph, condition)
print(data.nodes)
