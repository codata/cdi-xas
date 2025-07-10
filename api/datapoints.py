import re
import rdflib
import requests
from rdflib.namespace import SKOS, RDF

class CDI_DDI:
    def __init__(self, url=None, export_file=None, export_format=None, resources_dir="./resources", type=None):
        self.url = url
        self.export_file = export_file
        self.export_format = export_format
        self.resources_dir = resources_dir
        self.type = type
        self.g = rdflib.Graph()
        self.skos = SKOS
        self.rdf = RDF
        self.name = "https://docs.ddialliance.org/DDI-CDI/1.0/model/encoding/json-ld/ddi-cdi.jsonld#"
        self.g.bind("skos", SKOS)
        self.g.bind("rdf", RDF)
        self.g.bind("cdi", self.name)
        self.instance = "instanceVariable"
        self.datasets = {}
        self.navigator = None
        self.lastvariable = None
        self.response = requests.get(url)

    def get_full_variable_name(self, variable_name):
        return self.name +  self.instance + '-' + variable_name
    
    def load_resources(self, type):
        if type == 'cdi':
            self.load_cdi_resources()
        elif type == 'ddi':
            self.load_ddi_resources()

    def load_cdi_resources(self):
        self.g.parse(self.resources_dir + "/cdi.ttl", format="turtle")

    def load_ddi_resources(self):
        self.g.parse(self.resources_dir + "/ddi.ttl", format="turtle")

    def check_compound_variable_name(self, compound_variable_name):
        if '.' in compound_variable_name:
            return True
        else:
            return False

    def check_variable_name(self, variable_name):
        if variable_name.startswith('#'):
            return True
        else:
            return False

    def parse_structure(self, value):
        if ':' in value:
            compound_variable_name = re.search(r'#\s+(.*)\:', value)
            variable_value = re.search(r'\:\s*(.*)', value)
            return compound_variable_name, variable_value
        else:
            return None, value

    def parse_cdi(self):
        for line in self.response.text.split("\n"):
            # Variables path
            #print(line)
            if self.check_variable_name(line):
                compound_variable_name, variable_value = self.parse_structure(line)
                if compound_variable_name and variable_value:
                        compound_variable_name = compound_variable_name.group(1).strip('#  ')
                        variable_value = variable_value.group(1)
                        if '.' in compound_variable_name:
                            #Outer.value:  1.0
                            compound_variable_name_uri = compound_variable_name.replace(" ", "_").replace(":", "_")
                            variables = compound_variable_name_uri.split('.')
                            variable_last = ''
                            for variable_id in range(0,len(variables)-1):
                                variable_name = variables[variable_id]
                                variable_next = variables[variable_id+1]
                                print("Compound: " + variable_name + '.' + variable_next + " = " + variable_value)
                                self.g.add((rdflib.URIRef(self.get_full_variable_name(variable_name)), self.skos.prefLabel, rdflib.Literal(variable_name)))
                                self.g.add((rdflib.URIRef(self.get_full_variable_name(variable_name)), self.skos.broader, rdflib.URIRef(self.get_full_variable_name(variable_next))))
                                variable_last = variable_next
                                #self.g.add((rdflib.URIRef(self.name + variable_name), rdflib.URIRef(self.name + variable_next), rdflib.Literal(variable_value)))
                                blank = rdflib.BNode()
                                self.g.add((rdflib.URIRef(self.get_full_variable_name(variable_name)), rdflib.URIRef(self.get_full_variable_name(variable_next)), blank))
                                self.g.add((blank, rdflib.URIRef(self.skos.definition), rdflib.Literal(variable_value)))
                                self.navigator = blank
                        else:
                            variable_name = compound_variable_name.strip('#  ').replace(" ", "_")
                            try:
                                variable_value = variable_value.group(1)
                                self.g.add((rdflib.URIRef(self.get_full_variable_name(variable_name)), self.skos.prefLabel, rdflib.Literal(variable_value)))
                            except:
                                pass
                        try:
                            lastvariable = variable_name
                            g.add((rdflib.URIRef(self.get_full_variable_name(variable_name)), skos.prefLabel, rdflib.Literal(variable_value)))
                            data.append({
                                variable_name: variable_value
                            })
                        except:
                            #print(line)
                            pass
            # Data path
            else:
                if self.navigator:
                    if not self.lastvariable in self.datasets:
                        self.datasets[self.navigator] = [line.strip()]
                        for row in line.strip().split(' '):
                            self.g.add((self.navigator, rdflib.URIRef(self.rdf.List), rdflib.Literal(row)))
                    else:
                        self.datasets[self.navigator].append(line.strip())
                        for row in line.strip().split(' '):
                            self.g.add((self.navigator, rdflib.URIRef(self.rdf.List), rdflib.Literal(row)))
        return self.g

#url = "https://raw.githubusercontent.com/XraySpectroscopy/XAS-Data-Interchange/refs/heads/master/data/nonxafs_2d.xdi"
#cdi = CDI_DDI(url, "cdi.jsonld", "turtle", type='xas')
#print(cdi.parse_cdi().serialize(format='turtle'))