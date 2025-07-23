# mypy: disable-error-code="misc"
from abc import ABCMeta
from typing import List, Union
from pydantic import ConfigDict, Field, field_validator
from rdflib import OWL, URIRef
from sempyro.rdf_model import LiteralField, RDFModel  # type: ignore

from cdi.pyro.constants import CDI
from cdi.pyro.datatypes import (
    ControlledVocabularyEntry,
    Identifier,
    LabelForDisplay,
    ObjectName,
    Reference,
)
from sempyro.utils.validator_functions import force_literal_field  # type: ignore


class Concept(RDFModel, metaclass=ABCMeta):
    """Unit of thought differentiated by characteristics (from the Generic Statistical Information Model version 1.2"""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.Concept,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "Concept-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    name: ObjectName | None = Field(
        default=None,
        description="A standard means of expressing a name for a class object.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "Concept-name"),
            "rdf_type": CDI.ObjectName,
        },
    )

    displayLabel: LabelForDisplay | None = Field(
        default=None,
        description="A human-readable display label for the object.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "Concept-displayLabel"),
            "rdf_type": CDI.LabelForDisplay,
        },
    )

    sameAs: URIRef | None = Field(
        default=None,
        description="The built-in OWL property owl:sameAs links an individual to an individual. ",
        json_schema_extra={
            "rdf_term": OWL.sameAs,
            "rdf_type": "uri",
        },
    )

    externalDefinition: Reference | None = Field(
        default=None,
        description="A reference to an external definition of a concept (that is, a concept which is described outside the content"
        " of the DDI-CDI metadata description). An example is a SKOS concept. ",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "Concept-externalDefinition"),
            "rdf_type": CDI.Reference,
        },
    )

    Concept_uses_Concept: List[URIRef] | None = Field(
        default=None,
        description="The uses association is intended to describe specific relationships between Concepts and several of its sub-classes.",
        json_schema_extra={
            "rdf_term": CDI.Concept_uses_Concept,
            "rdf_type": "uri",
        },
    )


class ConceptualVariable(Concept):
    """A variable at the highest level of abstraction."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.ConceptualVariable,
            "$prefix": "cdi",
        },
    )


class RepresentedVariable(ConceptualVariable):
    """Conceptual variable with a substantive value domain specified."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.RepresentedVariable,
            "$prefix": "cdi",
        },
    )

    describedUnitOfMeasure: ControlledVocabularyEntry | None = Field(
        default=None,
        description="The unit in which the data values are measured (kg, pound, euro), expressed as a value from a controlled system of entries (i.e., QDT).",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "RepresentedVariable-describedUnitOfMeasure"),
            "rdf_type": CDI.ControlledVocabularyEntry,
        },
    )

    RepresentedVariable_takesSubstantiveValuesFrom_SubstantiveValueDomain: (
        URIRef | None
    ) = Field(
        default=None,
        description="The substantive representation (substantive value domain) of the variable. This is equivalent to the "
        "relationship “Measures” in the Generic Statistical Information Model (GSIM) although GSIM makes "
        "no distinction between substantive and sentinel values.",
        json_schema_extra={
            "rdf_term": CDI.RepresentedVariable_takesSubstantiveValuesFrom_SubstantiveValueDomain,
            "rdf_type": "uri",
        },
    )


class InstanceVariable(RepresentedVariable):
    """Use of a represented variable within a data set."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.InstanceVariable,
            "$prefix": "cdi",
        },
    )

    variableFunction: list[ControlledVocabularyEntry] | None = Field(
        default=None,
        description="Immutable characteristic of the variable such as geographic designator, weight, temporal designation, etc.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "InstanceVariable-variableFunction"),
            "rdf_type": CDI.ControlledVocabularyEntry,
        },
    )

    physicalDataType: ControlledVocabularyEntry | None = Field(
        default=None,
        description="The data type of this variable. Supports the optional use of an external controlled vocabulary.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "InstanceVariable-physicalDataType"),
            "rdf_type": CDI.ControlledVocabularyEntry,
        },
    )

    InstanceVariable_has_ValueMapping: URIRef | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.InstanceVariable_has_ValueMapping,
            "rdf_type": "uri",
        },
    )

    InstanceVariable_has_PhysicalSegmentLayout: list[URIRef] | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.InstanceVariable_has_PhysicalSegmentLayout,
            "rdf_type": "uri",
        },
    )


class VariableCollection(RDFModel, metaclass=ABCMeta):
    """Group of any type of variable within the variable cascade (conceptual, represented, instance)."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.VariableCollection,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "VariableCollection-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    allowsDuplicates: bool = Field(
        default=False,
        description="If value is False, the members are unique within the collection - if True, there may be duplicates.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "VariableCollection-allowsDuplicates"),
            "rdf_type": "xsd:boolean",
        },
    )

    VariableCollection_isDefinedBy_Concept: List[URIRef] | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.VariableCollection_isDefinedBy_Concept,
            "rdf_type": "uri",
        },
    )

    VariableCollection_has_ConceptualVariable: List[URIRef] | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.VariableCollection_has_ConceptualVariable,
            "rdf_type": "uri",
        },
    )

    @field_validator("allowsDuplicates", mode="before")
    @classmethod
    def convert_to_literal(cls, value: Union[bool, LiteralField]) -> List[LiteralField]:
        return force_literal_field(value)  # type: ignore


class Category(Concept):
    """Concept whose role is to define and measure a characteristic."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.Category,
            "$prefix": "cdi",
        },
    )
