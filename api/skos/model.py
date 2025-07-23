# mypy: disable-error-code="misc"
from abc import ABCMeta
from typing import List, Union

from pydantic import ConfigDict, Field
from sempyro.rdf_model import LiteralField, RDFModel  # type: ignore
from rdflib import SKOS, URIRef


class ConceptScheme(RDFModel, metaclass=ABCMeta):
    """A SKOS concept scheme can be viewed as an aggregation of one or more SKOS concepts."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://www.w3.org/2004/02/skos/core#",
            "$namespace": str(SKOS),
            "$IRI": SKOS.ConceptScheme,
            "$prefix": "skos",
        },
    )

    prefLabel: Union[str, LiteralField] | None = Field(
        default=None,
        description="Preferred label.",
        json_schema_extra={
            "rdf_term": SKOS.prefLabel,
            "rdf_type": "rdfs_literal",
        },
    )

    altLabel: Union[str, LiteralField] | None = Field(
        default=None,
        description="Alternative label.",
        json_schema_extra={
            "rdf_term": SKOS.altLabel,
            "rdf_type": "rdfs_literal",
        },
    )

    hasTopConcept: List[URIRef] | None = Field(
        default=None,
        description="The property skos:hasTopConcept is, by convention, used to link a concept scheme to the SKOS concept(s) which are topmost in the hierarchical relations for that scheme.",
        json_schema_extra={
            "rdf_term": SKOS.hasTopConcept,
            "rdf_type": "uri",
        },
    )


class Concept(RDFModel, metaclass=ABCMeta):
    """A SKOS concept can be viewed as an idea or notion; a unit of thought."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://www.w3.org/2004/02/skos/core#",
            "$namespace": str(SKOS),
            "$IRI": SKOS.Concept,
            "$prefix": "skos",
        },
    )

    notation: Union[str, LiteralField] | None = Field(
        default=None,
        description="notation.",
        json_schema_extra={
            "rdf_term": SKOS.notation,
            "rdf_type": "rdfs_literal",
        },
    )

    prefLabel: Union[str, LiteralField] | None = Field(
        default=None,
        description="Preferred label.",
        json_schema_extra={
            "rdf_term": SKOS.prefLabel,
            "rdf_type": "rdfs_literal",
        },
    )

    altLabel: Union[str, LiteralField] | None = Field(
        default=None,
        description="Alternative label.",
        json_schema_extra={
            "rdf_term": SKOS.altLabel,
            "rdf_type": "rdfs_literal",
        },
    )

    narrower: List[URIRef] | None = Field(
        default=None,
        description="A hierarchical link between two concepts indicating that one is in some way less general than the other (narrower).",
        json_schema_extra={
            "rdf_term": SKOS.narrower,
            "rdf_type": "uri",
        },
    )

    broader: List[URIRef] | None = Field(
        default=None,
        description="A hierarchical link between two concepts indicating that one is in some way more general than the other (broader).",
        json_schema_extra={
            "rdf_term": SKOS.broader,
            "rdf_type": "uri",
        },
    )

    topConceptOf: URIRef | None = Field(
        default=None,
        description="SKOS concepts which are topmost in the hierarchical relations for that scheme.",
        json_schema_extra={
            "rdf_term": SKOS.topConceptOf,
            "rdf_type": "uri",
        },
    )
