# mypy: disable-error-code="misc"
from abc import ABCMeta
from typing import List, Union

from pydantic import AnyHttpUrl, ConfigDict, Field
from rdflib import URIRef
from sempyro.rdf_model import LiteralField, RDFModel  # type: ignore

from cdi.pyro.constants import CDI
from cdi.pyro.datatypes import Identifier, ObjectName


class PhysicalDataSet(RDFModel, metaclass=ABCMeta):
    """Information needed for understanding the physical structure of data coming from a file or other source."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.PhysicalDataSet,
            "$prefix": "cdi",
        },
    )

    allowsDuplicates: bool = Field(
        default=False,
        description="If value is False, the members are unique within the collection - if True, there may be duplicates.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "PhysicalDataSet-allowsDuplicates"),
            "rdf_type": "xsd:boolean",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "PhysicalDataSet-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    name: ObjectName | None = Field(
        default=None,
        description="A standard means of expressing a name for a class object.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "PhysicalDataSet-name"),
            "rdf_type": CDI.ObjectName,
        },
    )

    PhysicalDataSet_has_PhysicalRecordSegment: List[AnyHttpUrl] | None = Field(
        default=None,
        description="Description of each physical storage segment required to completely cover a physical record representing the logical record.",
        json_schema_extra={
            "rdf_term": CDI.PhysicalDataSet_has_PhysicalRecordSegment,
            "rdf_type": "uri",
        },
    )


class PhysicalRecordSegment(RDFModel, metaclass=ABCMeta):
    """Description of each physical storage segment required to completely cover a physical record representing the logical record."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.PhysicalRecordSegment,
            "$prefix": "cdi",
        },
    )

    allowsDuplicates: bool = Field(
        default=False,
        description="If value is False, the members are unique within the collection - if True, there may be duplicates.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "PhysicalRecordSegment-allowsDuplicates"),
            "rdf_type": "xsd:boolean",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "PhysicalRecordSegment-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    PhysicalRecordSegment_has_DataPoint: List[AnyHttpUrl] | None = Field(
        default=None,
        description="Container for an instance value.",
        json_schema_extra={
            "rdf_term": CDI.PhysicalRecordSegment_has_DataPoint,
            "rdf_type": "uri",
        },
    )


class PhysicalSegmentLayout(RDFModel, metaclass=ABCMeta):
    """Used as an extension point in the description of the different layout styles of data structure descriptions."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.PhysicalSegmentLayout,
            "$prefix": "cdi",
        },
    )

    isDelimited: bool = Field(
        default=False,
        description="Indicates whether the data are in a delimited format. If “true,” the format is delimited, and the isFixedWidth property must be set to “false.” \
                        If not set to “true,” the property isFixedWitdh must be set to “true.”.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "PhysicalSegmentLayout-isDelimited"),
            "rdf_type": "xsd:boolean",
        },
    )

    isFixedWidth: bool = Field(
        default=False,
        description="Set to true if the file is fixed-width. If true, isDelimited must be set to false.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "PhysicalSegmentLayout-isFixedWidth"),
            "rdf_type": "xsd:boolean",
        },
    )

    delimiter: Union[str, LiteralField] | None = Field(
        default=None,
        description="The Delimiting character in the data. Must be used if isDelimited is True.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "PhysicalSegmentLayout-delimiter"),
            "rdf_type": "xsd:string",
        },
    )

    PhysicalSegmentLayout_formats_LogicalRecord: List[URIRef] | None = Field(
        default=None,
        description="Logical record physically represented by the physical layout.",
        json_schema_extra={
            "rdf_term": CDI.PhysicalSegmentLayout_formats_LogicalRecord,
            "rdf_type": "uri",
        },
    )

    PhysicalSegmentLayout_has_ValueMapping: List[URIRef] | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.PhysicalSegmentLayout_has_ValueMapping,
            "rdf_type": "uri",
        },
    )


class ValueMapping(RDFModel, metaclass=ABCMeta):
    """Physical characteristics for the value of an instance variable stored in a data point as part of a physical segment layout."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.ValueMapping,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "ValueMapping-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    defaultValue: Union[str, LiteralField] | None = Field(
        default=None,
        description="A default string indicating the value to substitute for an empty string.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "ValueMapping-defaultValue"),
            "rdf_type": "xsd:string",
        },
    )

    ValueMapping_formats_DataPoint: List[AnyHttpUrl] | None = Field(
        default=None,
        description="Container for an instance value.",
        json_schema_extra={
            "rdf_term": CDI.ValueMapping_formats_DataPoint,
            "rdf_type": "uri",
        },
    )


class ValueMappingPosition(RDFModel, metaclass=ABCMeta):
    """Denotes the position of a value mapping in a sequence."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.ValueMappingPosition,
            "$prefix": "cdi",
        },
    )

    value: int | None = Field(
        default=None,
        description="Index value of the member in an ordered array.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "ValueMapping-value"),
            "rdf_type": "xsd:nonNegativeInteger",
        },
    )

    ValueMappingPosition_indexes_ValueMapping: List[URIRef] | None = Field(
        default=None,
        description="Assigns a position to a value mapping within a physical segment.",
        json_schema_extra={
            "rdf_term": CDI.ValueMappingPosition_indexes_ValueMapping,
            "rdf_type": "uri",
        },
    )


class LogicalRecord(RDFModel, metaclass=ABCMeta):
    """Collection of instance variables."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.LogicalRecord,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "LogicalRecord-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    LogicalRecord_organizes_DataSet: List[URIRef] | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.LogicalRecord_organizes_DataSet,
            "rdf_type": "uri",
        },
    )

    LogicalRecord_has_InstanceVariable: List[URIRef] | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.LogicalRecord_has_InstanceVariable,
            "rdf_type": "uri",
        },
    )


class DataStore(RDFModel, metaclass=ABCMeta):
    """Collection of logical records."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.DataStore,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "DataStore-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    DataStore_has_LogicalRecord: List[URIRef] | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.DataStore_has_LogicalRecord,
            "rdf_type": "uri",
        },
    )
