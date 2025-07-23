# mypy: disable-error-code="misc"
from abc import ABCMeta

from pydantic import ConfigDict, Field
from rdflib import URIRef
from sempyro.rdf_model import RDFModel  # type: ignore

from cdi.pyro.constants import CDI
from cdi.pyro.datatypes import ControlledVocabularyEntry, Identifier, Statistic


class ValueDomain(RDFModel, metaclass=ABCMeta):
    """Set of permissible values for a variable (adapted from ISO/IEC 11179)."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.ValueDomain,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "ValueDomain-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    recommendedDataType: ControlledVocabularyEntry | None = Field(
        default=None,
        description="The data types that are recommended for use with this domain.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "ValueDomain-recommendedDataType"),
            "rdf_type": CDI.ControlledVocabularyEntry,
        },
    )


class SubstantiveValueDomain(ValueDomain):
    """Value domain for a substantive conceptual domain. Typically a description and/or enumeration of allowed values of interest."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.SubstantiveValueDomain,
            "$prefix": "cdi",
        },
    )

    SubstantiveValueDomain_takesValuesFrom_EnumerationDomain: URIRef | None = Field(
        default=None,
        description="Any subtype of an enumeration domain enumerating the set of valid values.",
        json_schema_extra={
            "rdf_term": CDI.SubstantiveValueDomain_takesValuesFrom_EnumerationDomain,
            "rdf_type": "uri",
        },
    )


class EnumerationDomain(RDFModel, metaclass=ABCMeta):
    """A base class acting as an extension point to allow all codifications (codelist, statistical classification, etc.) to be understood as enumerated value domains."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.EnumerationDomain,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "EnumerationDomain-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )


class CodeList(EnumerationDomain):
    """List of codes and associated categories."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.CodeList,
            "$prefix": "cdi",
        },
    )

    allowsDuplicates: bool = Field(
        default=False,
        description="If value is False, the members are unique within the collection - if True, there may be duplicates.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "CodeList-allowsDuplicates"),
            "rdf_type": "xsd:boolean",
        },
    )

    CodeList_has_Code: list[URIRef] | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.CodeList_has_Code,
            "rdf_type": "uri",
        },
    )


class Code(RDFModel, metaclass=ABCMeta):
    """The characters used as a symbol to designate a category within a codelist or classification."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.Code,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "Code-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    Code_uses_Notation: URIRef = Field(
        description="",
        json_schema_extra={
            "rdf_term": CDI.Code_uses_Notation,
            "rdf_type": "uri",
        },
    )

    Code_denotes_Category: URIRef = Field(
        description="",
        json_schema_extra={
            "rdf_term": CDI.Code_denotes_Category,
            "rdf_type": "uri",
        },
    )


class CategoryStatistic(RDFModel, metaclass=ABCMeta):
    """Statistics related to a specific category of an instance variable within a data set."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.CategoryStatistic,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "CategoryStatistic-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    statistic: list[Statistic] | None = Field(
        default=None,
        description="The value of the identified type of statistic for the category. May be repeated to provide unweighted or weighted values and different computation bases.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "CategoryStatistic-statistic"),
            "rdf_type": CDI.Statistic,
        },
    )

    typeOfCategoryStatistic: ControlledVocabularyEntry | None = Field(
        default=None,
        description="Indicates the type of information about the appearance of categories within the instance variable.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "CategoryStatistic-typeOfCategoryStatistic"),
            "rdf_type": CDI.ControlledVocabularyEntry,
        },
    )

    CategoryStatistic_appliesTo_InstanceVariable: list[URIRef] = Field(
        description="",
        json_schema_extra={
            "rdf_term": CDI.CategoryStatistic_appliesTo_InstanceVariable,
            "rdf_type": "uri",
        },
    )
