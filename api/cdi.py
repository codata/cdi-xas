import json
import requests
import pandas as pd
import rdflib
import re
import os
import argparse

class CDI_DDI:
    def __init__(self, url=None, export_file=None, export_format=None, resources_dir="../resources", type=None):
        self.url = url
        self.g = rdflib.Graph()
        self.resources = {}
        self.resources_dir = resources_dir
        self.resources = self.load_resources(type)
        self.skos = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
        self.rdf = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        self.dcat = rdflib.Namespace("http://www.w3.org/ns/dcat#")
        self.name = rdflib.Namespace("https://ddi-cdi.org/label/")
        self.label = rdflib.Namespace("https://ddi-cdi.org/label/")
        self.bind = rdflib.Namespace("https://ddi-cdi.org/bind/")
        self.g.bind("skos", self.skos)
        self.g.bind("rdf", self.rdf)
        self.g.bind("dcat", self.dcat)
        self.g.bind("name", self.name)
        self.g.bind("label", self.label)
        self.g.bind("bind", self.bind)
        self.export_file = export_file
        self.export_format = export_format
        if url:
            self.response = requests.get(url)
        else:
            self.response = None
        self.lastvariable = ""
        self.data = []
        self.datasets = {}
        self.navigator = None
        self.session_triples = []
        self.triples_memory = []

    def load_resources(self, type):
        self.resources = {}
        for file in os.listdir(self.resources_dir):
            if type in file:
                print(type, file)
                if file.endswith(".jsonld"):
                    self.resources[file.replace(".jsonld", "")] = self.g.parse(os.path.join(self.resources_dir, file), format="json-ld")
                elif file.endswith(".ttl"):
                    self.resources[file.replace(".ttl", "")] = self.g.parse(os.path.join(self.resources_dir, file), format="turtle")
        return self.resources

    def empty_session_triples(self):
        self.session_triples = []
        return self.session_triples

    def find_resource(self, resource_name, search_by="prefLabel"):
        self.DEBUG = False
        self.DEBUG_LEVEL = 0
        self.triples = []
        for resource in self.resources:
            for triple in self.resources[resource]:
                s, p, o = triple
                print(triple)
                if self.DEBUG_LEVEL == 1:
                    print(s, p, o)
                if search_by == "all":
                    if p == rdflib.URIRef(self.skos.prefLabel) and o == rdflib.Literal(resource_name):
                        if self.DEBUG:
                            print("Search by prefLabel: " + s + " " + p + " " + resource_name) # + " " + self.resources[resource])
                        if not triple in self.triples_memory:
                            self.session_triples.append(triple)
                            self.triples_memory.append(triple)
                        self.find_resource(s, search_by="definition")
                elif search_by == "subject":
                    if rdflib.URIRef(s) == rdflib.URIRef(resource_name):
                        if self.DEBUG:
                            print("*** Search by subject: " + s + " " + p + " " + resource_name) # + " " + self.resources[resource])
                        if not triple in self.triples_memory:
                            self.session_triples.append(triple)
                            self.triples_memory.append(triple)
                elif search_by == "prefLabel":
                    if p == rdflib.URIRef(self.skos.prefLabel) and o == rdflib.Literal(resource_name):
                        if self.DEBUG:
                            print("Search by prefLabel: " + s + " " + p + " " + resource_name) # + " " + self.resources[resource])
                        self.find_resource(s, search_by="subject")
                        self.session_triples.append(triple)
                elif search_by == "definition":
                    if p == rdflib.URIRef(self.skos.definition) and o == rdflib.Literal(resource_name):
                        if self.DEBUG:
                            print("Search by definition: " + s + " " + p + " " + resource_name) # + " " + self.resources[resource])
                        self.session_triples.append(triple)
                elif search_by == "altLabel":
                    if p == rdflib.URIRef(self.skos.altLabel) and o == rdflib.Literal(resource_name):
                        if self.DEBUG:
                            print("Search by altLabel: " + s + " " + p + " " + resource_name) # + " " + self.resources[resource])
                        self.session_triples.append(triple)
        return self.session_triples

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
                                self.g.add((rdflib.URIRef(self.name + variable_name), self.skos.prefLabel, rdflib.Literal(variable_name)))
                                self.g.add((rdflib.URIRef(self.name + variable_name), self.skos.broader, rdflib.URIRef(self.name + variable_next)))
                                variable_last = variable_next
                                #self.g.add((rdflib.URIRef(self.name + variable_name), rdflib.URIRef(self.name + variable_next), rdflib.Literal(variable_value)))
                                blank = rdflib.BNode()
                                self.g.add((rdflib.URIRef(self.name + variable_name), rdflib.URIRef(self.name + variable_next), blank))
                                self.g.add((blank, rdflib.URIRef(self.skos.definition), rdflib.Literal(variable_value)))
                                self.navigator = blank
                        else:
                            variable_name = compound_variable_name.strip('#  ').replace(" ", "_")
                            try:
                                variable_value = variable_value.group(1)
                                self.g.add((rdflib.URIRef(self.name + variable_name), self.skos.prefLabel, rdflib.Literal(variable_value)))
                            except:
                                pass
                        try:
                            lastvariable = variable_name
                            g.add((rdflib.URIRef(name + variable_name), skos.prefLabel, rdflib.Literal(variable_value)))
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

        # Convert the graph to JSON-LD format
        self.g.serialize(destination=self.export_file, format=self.export_format)

        print(f"Graph exported to {self.export_file} in {self.export_format} format")
        print(self.datasets)
        return self.data
