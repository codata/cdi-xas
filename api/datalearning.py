import re
import pandas as pd
import rdflib
from rdflib import Literal

class DataLearning:
    def __init__(self, config_path, data_path, format="turtle"):
        self.data_path = data_path
        self.g = rdflib.Graph()
        self.nodes = []
        self.path = "file://" + config_path
        self.set_local_path(config_path)
        if not '/' in data_path:
            self.permauri = self.path + data_path
        else:
            self.permauri = self.get_local_path(data_path.replace(self.localpath, ""))
        self.cdiuri = "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/"
        self.localpath = self.path + data_path
        self.full_graph_path = config_path + "/ddi-cdi-full-graph.ttl"
        self.g.bind("DDICDIMODELS", self.path + "xdi_example_ss.jsonld")
        self.cdigraph = rdflib.Graph()
        self.fullgraph = rdflib.Graph()
        self.load_full_graph()
        self.cdigraph.bind("DDICDIMODELS", self.path + "xdi_example_ss.jsonld")
        self.cdigraph.context = {
            "DDICDIMODELS": {
                "@context": {
                    "@vocab": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
                    "DDICDIMODELS": self.path + "xdi_example_wds.jsonld"
                }
            }
        }

    def checkURI(self, uri):
        if uri.startswith("http://") or uri.startswith("https://"):
            return uri
        else:
            return self.cdiuri + uri
    
    def load_full_graph(self, format="turtle"):
        self.fullgraph.parse(self.full_graph_path, format=format)

    def load_data(self, format="json-ld"):
        self.g.parse(self.data_path, format=format)

    def get_data(self):
        return self.g

    def get_type(self, subject, graph=None):
        subject = f"<{self.checkURI(subject)}>"
        query = f"""
            PREFIX xdi: <http://www.w3.org/ns/xdi/core#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?object WHERE {{
                {subject} rdf:type ?object .
            }}
        """
        result = []
        #print(query)
        for s in graph.query(query):
            result.append(str(s[0]))
        if not result:
            return None
        return result[0]

    def set_local_path(self, path):
        self.path = "file://" + path
        self.localpath = self.path 

    def get_local_path(self, path):
        return "file://" + path

    def get_data_as_pandas(self):
        return pd.DataFrame(self.g)
        self.data = self.data.reset_index(drop=True)

    def serialize_data(self, format="turtle"):
        return self.g.serialize(format=format)

    def lookup_subject(self, subject):
        subject = f"<{subject}>"
        query = f"""
            PREFIX xdi: <http://www.w3.org/ns/xdi/core#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?subject ?predicate ?object WHERE {{
                {subject} ?predicate ?object .
            }}
        """ 
        print(query)
        for s in self.g.query(query):
            print(s)

    def get_related_triples(self, graph, subject, predicate="skos:narrower"):
        subject = f"<{self.checkURI(subject)}>"
        self.nodes = []
        query = f"""
            PREFIX xdi: <http://www.w3.org/ns/xdi/core#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT ?object ?predicate WHERE {{
                {subject} {predicate} ?object .
            }}
        """
        #print(query)
        result = []
        for s in graph.query(query):
            result.append(str(s[0]))
            self.nodes.append(str(s[0]))
            print("[DEBUG] ", s[0])
        return result

    def configurate_triples(self, value, graph=None):
        self.DEBUG = True
        if self.DEBUG:
            print("Configurate triples for: ", value)
        for triple in graph.triples((None, None, None)):
            s, p, o = triple
            if value.lower() == str(s).lower():
                if self.DEBUG:
                    print("\nS: ", triple)
                self.cdigraph.add(triple)
            if value.lower() == str(p).lower():
                if self.DEBUG:
                    print("\tP: ", triple)
                self.cdigraph.add(triple)
            if value.lower() == str(o).lower():
                if self.DEBUG:
                    print("\tO: ", triple)
                self.cdigraph.add(triple)

    
    def lookup_predicate(self, predicate):
        return self.g.predicates(predicate)
    
    def lookup_object(self, object):
        return self.g.objects(object)
    
    def add_permanent_schema(self, schema):
        if schema == 'dataset':
            field = "InstanceVariable"
            field = "LogicalRecord_has_InstanceVariable"
            #field = "logical_record"
            x = self.configurate_triples(self.cdiuri + field, self.g)
            field = "LogicalRecord_organizes_DataSet"
            x = self.configurate_triples(self.cdiuri + field, self.g)
            field = "has_DataStructureComponent"
            x = self.configurate_triples(self.cdiuri + field, self.g)
            field = "DataStructureComponent_isDefinedBy_RepresentedVariable"
            x = self.configurate_triples(self.cdiuri + field, self.g)
            field = "logicalRecord-wds"
            x = self.configurate_triples(self.cdiuri + field, self.g)
            field = "SegmentByText"
            x = self.configurate_triples(self.cdiuri + field, self.g)
            compoundfields = self.get_related_triples(self.fullgraph, self.cdiuri + field)
            for field in compoundfields:
                x = self.get_related_triples(self.fullgraph, field)
                print("[COMPOUND DEBUG 2] x: y:", x, field)
                for field in x:
                    #x = self.configurate_triples(field, self.g)
                    y = self.get_related_triples(self.fullgraph, field)
            print("[COMPOUND DEBUG] fields: ", compoundfields)

            # Local path
            #localpath = "file:///home/tikhonov/projects/computer-eyes/resources/xdi_example_ss.jsonld" #xdi_example_wds.jsonld#"
            field = "physicalSegmentLayout"
            x = self.configurate_triples(self.permauri + '#' + field, self.g)
            field = "ValueMapping"
            x = self.configurate_triples(self.permauri + '#' + field, self.g)
            field = "DataStore"
            x = self.configurate_triples(self.permauri + '#' + field, self.g)
            field = "wideDataSet"
            x = self.configurate_triples(self.permauri + '#' + field, self.g)
            field = "wideDataStructure"
            x = self.configurate_triples(self.permauri + '#' + field, self.g)
            field = "physicalSegmentLayout-wds"
            x = self.configurate_triples(self.localpath + '#' + field, self.g)
            #print(data.cdigraph.serialize(format="turtle"))
        return self.cdigraph

    def export(self, format="turtle"):
        data = self.cdigraph.serialize(format=format)
        dataexport = []
        for line in data.split("\n"):
            line = line.replace(self.permauri, "")
            line = line.replace(self.cdiuri, "cdi:")
            dataexport.append(line)
        return "\n".join(dataexport)

    def triple_by_triple(self, graph=None, search=None):
        triples = []
        for s, p, o in graph.triples((None, None, None)):
            if not search:
                triples.append(f"{s} {p} {o}")
                continue
            else:
                searchquery = self.checkURI(search)
                if searchquery.lower() in str(s).lower():
                    triples.append(f"{s} {p} {o}")
                if searchquery.lower() in str(p).lower():
                    triples.append(f"{s} {p} {o}")
                if searchquery.lower() in str(o).lower():
                    triples.append(f"{s} {p} {o}")
        return triples
    