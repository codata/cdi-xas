# mypy: disable-error-code="misc"
from abc import ABCMeta
from typing import List, Union

from pydantic import ConfigDict, Field
from rdflib import URIRef
from cdi.pyro.constants import CDI
from sempyro.rdf_model import LiteralField, RDFModel  # type: ignore


class InternationalRegistrationDataIdentifier(RDFModel, metaclass=ABCMeta):
    """Persistent, globally unique object identifier aligned with ISO/IEC 11179-6:2015"""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.InternationalRegistrationDataIdentifier,
            "$prefix": "cdi",
        },
    )

    dataIdentifier: Union[str, LiteralField] = Field(
        description="Identifier assigned to an Administered Item within a Registration Authority, hereafter called Data Identifier (DI).",
        json_schema_extra={
            "rdf_term": URIRef(
                CDI + "InternationalRegistrationDataIdentifier-dataIdentifier"
            ),
            "rdf_type": "xsd:string",
        },
    )

    registrationAuthorityIdentifier: Union[str, LiteralField] = Field(
        description="Identifier assigned to a Registration Authority, hereafter called Registration Authority Identifier (RAI).",
        json_schema_extra={
            "rdf_term": URIRef(
                CDI
                + "InternationalRegistrationDataIdentifier-registrationAuthorityIdentifier"
            ),
            "rdf_type": "xsd:string",
        },
    )

    versionIdentifier: Union[str, LiteralField] = Field(
        description="Identifier assigned to a version under which an Administered Item registration is submitted or updated hereafter called Version Identifier (VI).",
        json_schema_extra={
            "rdf_term": URIRef(
                CDI + "InternationalRegistrationDataIdentifier-versionIdentifier"
            ),
            "rdf_type": "xsd:string",
        },
    )


class Identifier(RDFModel, metaclass=ABCMeta):
    """Identifier for objects requiring short- or long-lasting referencing and management."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.Identifier,
            "$prefix": "cdi",
        },
    )

    ddiIdentifier: InternationalRegistrationDataIdentifier | None = Field(
        default=None,
        description="Persistent, globally unique object identifier aligned with ISO/IEC 11179-6:2015.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "Identifier-ddiIdentifier"),
            "rdf_type": CDI.InternationalRegistrationDataIdentifier,
        },
    )


class ObjectName(RDFModel, metaclass=ABCMeta):
    """A standard means of expressing a name for a class object."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.ObjectName,
            "$prefix": "cdi",
        },
    )

    name: Union[str, LiteralField] | None = Field(
        default=None,
        description="A name may be specific to a particular context, i.e., a type of software, or a section of a registry. Identify the context related to the specified name.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "ObjectName-name"),
            "rdf_type": "xsd:string",
        },
    )


class LanguageString(RDFModel, metaclass=ABCMeta):
    """A data type which describes a string specific to a language/scope combination."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.LanguageString,
            "$prefix": "cdi",
        },
    )

    content: Union[str, LiteralField] | None = Field(
        default=None,
        description="An identifier as it should be listed for identification purposes.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "LanguageString-content"),
            "rdf_type": "xsd:string",
        },
    )


class InternationalString(RDFModel, metaclass=ABCMeta):
    """Packaging structure for multilingual versions of the same string content, represented by a set of LanguageString."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.InternationalString,
            "$prefix": "cdi",
        },
    )

    languageSpecificString: LanguageString | None = Field(
        default=None,
        description="A non-formatted string of text with an attribute that designates the language of the text. Repeat this object to express the same content in another language.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "InternationalString-languageSpecificString"),
            "rdf_type": CDI.LanguageString,
        },
    )


class LabelForDisplay(InternationalString):
    """A structured display label. Label provides display content of a fully human readable display for the identification of the object."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.LabelForDisplay,
            "$prefix": "cdi",
        },
    )


class TypedString(RDFModel, metaclass=ABCMeta):
    """TypedString combines a type with content defined as a simple string. May be used wherever a simple string needs to support a type definition to clarify its content."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.TypedString,
            "$prefix": "cdi",
        },
    )

    content: Union[str, LiteralField] = Field(
        description="A name may be specific to a particular context, i.e., a type of software, or a section of a registry. Identify the context related to the specified name.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "TypedString-content"),
            "rdf_type": "xsd:string",
        },
    )


# class InternationalIdentifier(RDFModel, metaclass=ABCMeta):
#     """An identifier whose scope of uniqueness is broader than the local archive. Common forms of an international identifier are ISBN, ISSN, DOI or similar designator.
#     Provides both the value of the identifier and the agency who manages it."""

#     model_config = ConfigDict(
#         arbitrary_types_allowed=True,
#         use_enum_values=True,
#         json_schema_extra={
#             "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
#             "$namespace": str(CDI),
#             "$IRI": CDI.InternationalIdentifier,
#             "$prefix": "cdi",
#         },
#     )

#     identifierContent: Union[str, LiteralField] | None = Field(
#         default=None,
#         description="An identifier as it should be listed for identification purposes.",
#         json_schema_extra={
#             "rdf_term": URIRef(CDI + "InternationalIdentifier-identifierContent"),
#             "rdf_type": "xsd:string",
#         },
#     )


class BibliographicName(InternationalString):
    """Full name of the contributor. Language equivalents should be expressed within the international string structure."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.BibliographicName,
            "$prefix": "cdi",
        },
    )


class AgentInRole(RDFModel, metaclass=ABCMeta):
    """A reference to an agent (organization, individual, or machine) including a role for that agent in the context of this specific reference."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.AgentInRole,
            "$prefix": "cdi",
        },
    )

    agentName: BibliographicName | None = Field(
        default=None,
        description="Full name of the contributor. Language equivalents should be expressed within the international string structure.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "AgentInRole-agentName"),
            "rdf_type": CDI.BibliographicName,
        },
    )


class ControlledVocabularyEntry(RDFModel, metaclass=ABCMeta):
    """Allows for unstructured content which may be an entry from an externally maintained controlled vocabulary."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.ControlledVocabularyEntry,
            "$prefix": "cdi",
        },
    )

    entryValue: Union[str, LiteralField] | None = Field(
        default=None,
        description="The value of the entry of the controlled vocabulary.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "ControlledVocabularyEntry-entryValue"),
            "rdf_type": "xsd:string",
        },
    )

    name: Union[str, LiteralField] | None = Field(
        default=None,
        description="The name of the code list (controlled vocabulary).",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "ControlledVocabularyEntry-name"),
            "rdf_type": "xsd:string",
        },
    )


class NonDdiIdentifier(RDFModel, metaclass=ABCMeta):
    """A unique set of attributes, not conforming to the DDI identifier structure nor structured as a URI, used to identify some entity."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.NonDdiIdentifier,
            "$prefix": "cdi",
        },
    )

    managingAgency: Union[str, LiteralField] | None = Field(
        default=None,
        description="The authority which maintains the identification scheme.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "NonDdiIdentifier-managingAgency"),
            "rdf_type": "xsd:string",
        },
    )

    type: Union[str, LiteralField] | None = Field(
        default=None,
        description="The scheme of identifier, as distinct from a URI or a DDI-conforming identifier.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "NonDdiIdentifier-type"),
            "rdf_type": "xsd:string",
        },
    )

    value: Union[str, LiteralField] | None = Field(
        default=None,
        description="The identifier, structured according to the specified type.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "NonDdiIdentifier-value"),
            "rdf_type": "xsd:string",
        },
    )

    version: Union[str, LiteralField] | None = Field(
        default=None,
        description="The version of the object being identified, according to the versioning system provided by the identified scheme.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "NonDdiIdentifier-version"),
            "rdf_type": "xsd:string",
        },
    )


class Reference(RDFModel, metaclass=ABCMeta):
    """
    Provides a way of pointing to resources outside of the information described in the set of DDI-CDI metadata.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.Reference,
            "$prefix": "cdi",
        },
    )

    ddiReference: InternationalRegistrationDataIdentifier | None = Field(
        default=None,
        description="A DDI type reference to a DDI object.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "Reference-ddiReference"),
            "rdf_type": CDI.InternationalRegistrationDataIdentifier,
        },
    )

    nonDdiReference: NonDdiIdentifier | None = Field(
        default=None,
        description="A non-DDI reference to any object using a system of identification which is not supported by a URI.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "Reference-nonDdiReference"),
            "rdf_type": CDI.NonDdiIdentifier,
        },
    )


class CatalogDetails(RDFModel, metaclass=ABCMeta):
    """A set of information useful for attribution, data discovery, and access."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.CatalogDetails,
            "$prefix": "cdi",
        },
    )

    creator: List[AgentInRole] | None = Field(
        default=None,
        description="A reference to an agent (organization, individual, or machine) including a role for that agent in the context of this specific reference.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "CatalogDetails-creator"),
            "rdf_type": CDI.AgentInRole,
        },
    )

    title: InternationalString | None = Field(
        default=None,
        description="Full authoritative title. List any additional titles for this item as alternativeTitle.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "CatalogDetails-title"),
            "rdf_type": CDI.InternationalString,
        },
    )

    typeOfResource: List[ControlledVocabularyEntry] | None = Field(
        default=None,
        description="Provide the type of the resource. This supports the use of a controlled vocabulary. It should be appropriate to the level of the annotation.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "CatalogDetails-typeOfResource"),
            "rdf_type": CDI.ControlledVocabularyEntry,
        },
    )

    relatedResource: List[Reference] | None = Field(
        default=None,
        description="Provide the identifier, managing agency, and type of resource related to this object.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "CatalogDetails-relatedResource"),
            "rdf_type": CDI.Reference,
        },
    )


class Statistic(RDFModel, metaclass=ABCMeta):
    """The value of the statistic expressed as a decimal, float and/or double. Indicates whether it is weighted value and the computation base."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.Statistic,
            "$prefix": "cdi",
        },
    )

    content: float | None = Field(
        default=None,
        description="The value of the statistic expressed as a real number.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "Statistic-content"),
            "rdf_type": "xsd:decimal",
        },
    )
