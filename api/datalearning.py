import re
import pandas as pd
import rdflib
from rdflib import Literal, URIRef, SKOS

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
        #self.full_graph_path = config_path + "/ddi-cdi-full-graph.ttl"
        self.g.bind("DDICDIMODELS", self.path + "prov_generated_by.jsonld")
        self.cdigraph = rdflib.Graph()
        #self.fullgraph = rdflib.Graph()
        #self.load_full_graph()
        self.cdi_path = config_path + "test_cdi.jsonld"
        self.cdigraph.bind("DDICDIMODELS", self.path + "test_cdi.jsonld")
        self.cdigraph.context = {
            "@vocab": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/"
        }
        # self.cdigraph.context = {
        #     "DDICDIMODELS": {
        #         "@context": {
        #             "@vocab": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
        #             "DDICDIMODELS": self.path + "xdi_example_wds.jsonld"
        #         }
        #     }
        # }
        self.schemagraph = rdflib.Graph()
        self.schemagraph.context = [
            "https://docs.ddialliance.org/DDI-CDI/1.0/model/encoding/json-ld/ddi-cdi.jsonld",
            {
                "schema": "http://schema.org/",
                "dcterms": "http://purl.org/dc/terms/",
                "cdi": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
                "skos": "http://www.w3.org/2004/02/skos/core#",
                "xas": "http://cdi4exas.org/",
                "prov": "http://www.w3.org/ns/prov#"
            }
        ]

    def checkURI(self, uri):
        if uri.startswith("http://") or uri.startswith("https://"):
            return uri
        else:
            return self.cdiuri + uri
    
    def load_full_graph(self, format="turtle"):
        self.fullgraph.parse(self.full_graph_path, format=format)

    def load_data(self, format="json-ld"):
        self.g.parse(self.data_path, format=format)

    def load_cdi(self, format="json-ld"):
        self.cdigraph.parse(self.cdi_path, format=format)

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

    def merged(self, field: str) -> str:
        """
        Where field is of format [[<value>]] then this function
         finds the related value from the intermediate CDI SKOS graph created 
         from parsed XDI file
        
        :param self: DataLearning class
        :param field: the triple object to check 
        :type field: str
        :return: field input or related value
        :rtype: str
        """
        match = re.search(r"\[\[(.*?)::(value|units)\]\]", field)
        if (match is not None):
            xas_concept = match.group(1)
            value_units = match.group(2)

            # first determine format of this XAS concept
            # for this, necessary to replace with generic N if xas_concept ends in digit e.g., I0,I1, 
            generic_xas_concept = re.sub(r'\d$', 'N', xas_concept)
            concept_format:str = [triple[2] for triple in self.cdigraph.triples((URIRef(f"http://ddialliance.org/Specification/XAS/{generic_xas_concept}"),URIRef("http://ddialliance.org/Specification/XAS/format"),None))][0]
            plus_units = True if concept_format.endswith("+ units") else False

            concepts = xas_concept.split('.')
            xas_triples = [triple for triple in self.cdigraph.triples((URIRef(f"https://ddi-cdi.org/label/{concepts[0]}"),URIRef(f"https://ddi-cdi.org/label/{concepts[1]}"),None))]
            if len(xas_triples) == 0:
                xas_triples = [triple for triple in self.cdigraph.triples((URIRef(f"https://ddi-cdi.org/label/{concepts[0]}"),URIRef(f"https://ddi-cdi.org/label/{concepts[1].capitalize()}"),None))]

            for triple in xas_triples:
                for i_triple in self.cdigraph.triples((triple[2],SKOS.definition,None)):
                    # confirm plus_units
                    plus_units = True if (plus_units and len(i_triple[2].split(' ')) > 1) else False
                    if value_units == "value":
                        return i_triple[2].rsplit(' ', 1)[1] if plus_units else i_triple[2]
                    elif value_units == "units" and plus_units:
                        return i_triple[2].rsplit(' ', 1)[0]
                    elif value_units == "units":
                        # necessary to find units via XAS/units
                        xas_units:str = [triple[2] for triple in self.cdigraph.triples((URIRef(f"http://ddialliance.org/Specification/XAS/{generic_xas_concept}"),URIRef("http://ddialliance.org/Specification/XAS/units"),None))][0]
                        if xas_units is not None:
                            return xas_units
        return field

    def get_related_triples(self, graph, _subject)-> tuple[str,str,str]:
        if self.DEBUG:
            print("Get related triples for: ", _subject)
        subject = f"<{self.checkURI(_subject)}>"
        #self.nodes = []
        query = f"""
            PREFIX xdi: <http://www.w3.org/ns/xdi/core#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX schema: <http://schema.org/>
            SELECT ?predicate ?object WHERE {{
                {subject} ?predicate ?object .
            }}
        """
        result = []
        for s in graph.query(query):
            result.append((_subject, s[0], s[1]))
            self.schemagraph.add((_subject, s[0], Literal(self.merged(s[1]))))
        self.nodes.append(_subject)
        return result

    def configurate_triples(self, value, graph=None)-> tuple[str,str,str]:
        self.DEBUG = False
        if self.DEBUG:
            print("Configurate triples for: ", value)
        triples = []
        for triple in graph.triples((None, None, None)):
            s, p, o = triple
            if value.lower() == str(s).lower():
                if self.DEBUG:
                    print("\nS: ", triple)
                self.schemagraph.add((s,p,Literal(self.merged(o))))
                triples.append((s,p,o))
            if value.lower() == str(p).lower():
                if self.DEBUG:
                    print("\tP: ", triple)
                self.schemagraph.add((s,p,Literal(self.merged(o))))
                triples.append((s,p,o))
            if value.lower() == str(o).lower():
                if self.DEBUG:
                    print("\tO: ", triple)
                self.schemagraph.add((s,p,Literal(self.merged(o))))
                triples.append((s,p,o))
        return triples

    
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
    