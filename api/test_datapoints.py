import json
from rdflib import Graph
from datapoints import CDI_DDI
from config_local import datadir
from cdi.cdi_generator import create_key_value_data_store_structures
from pyld import jsonld

cdi = CDI_DDI()
cdi.load_xdi_resource()
cdi.parse_xdi()
#print(cdi.g.serialize(format="turtle"))

# ************************************************************************************************
# Key Value Generation
# ************************************************************************************************
# retrieve list of key value instance variables
key_values: list[tuple[str,str]] = []
for triple in cdi.get_related_triples():

    # exclude tabular triples - type RDF.list
    #if not cdi.is_tabular_variable(triple[0], triple[1]):

    label = ".".join(
        [
            str(triple[0]).replace(cdi.name, "").replace("instanceVariable-", ""),
            str(triple[1]).replace(cdi.name, "").replace("instanceVariable-", ""),
        ]
    )
    value = cdi.lookup_definition(triple[0],triple[1])[0]

    print("label: ", label, "value: ", value)
    key_values.append((label,value))

# First create structures for KeyValueDataStore
destination_path = datadir + "/test_cdi_output.ttl"

combined_graph = Graph()

combined_graph = combined_graph + create_key_value_data_store_structures(key_values)

with open(destination_path, "w") as file:
    file.write(combined_graph.serialize(format="json-ld"))


with open(destination_path) as f:
    doc = json.load(f)

    with open(datadir + "/cdi_frame.json") as f:
        frame = json.load(f)

        framed = jsonld.frame(doc, frame=frame, options={"omitDefault":True})

        destination_path = destination_path.replace("ttl", "jsonld")

        with open(destination_path, "w") as file:
            file.write(json.dumps(framed))
# ************************************************************************************************