# mypy: disable-error-code="misc"
from abc import ABCMeta
from typing import List

from pydantic import AnyHttpUrl, ConfigDict, Field
from rdflib import URIRef
from sempyro.rdf_model import RDFModel  # type: ignore

from cdi.pyro.conceptual import RepresentedVariable
from cdi.pyro.representations import SubstantiveValueDomain, ValueDomain
from cdi.pyro.constants import CDI
from cdi.pyro.datatypes import CatalogDetails, Identifier, TypedString


class InstanceValue(RDFModel, metaclass=ABCMeta):
    """Single data instance corresponding to a concept (with a notion of equality defined) being observed, captured, or derived."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.InstanceValue,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "InstanceValue-identifier"),
            "rdf_type": CDI.InternationalRegistrationDataIdentifier,
        },
    )

    content: TypedString | None = Field(
        default=None,
        description="The actual content of this value as a string.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "InstanceValue-content"),
            "rdf_type": CDI.TypedString,
        },
    )

    InstanceValue_isStoredIn_DataPoint: List[AnyHttpUrl] | None = Field(
        default=None,
        description="The instance variable delimits the values which can populate a data point. Data point is described by one instance variable.",
        json_schema_extra={
            "rdf_term": CDI.InstanceValue_isStoredIn_DataPoint,
            "rdf_type": "uri",
        },
    )

    InstanceValue_hasValueFrom_ValueDomain: URIRef | None = Field(
        default=None,
        description="Set of permissible values for a variable (adapted from ISO/IEC 11179).",
        json_schema_extra={
            "rdf_term": CDI.InstanceValue_hasValueFrom_ValueDomain,
            "rdf_type": "uri",
        },
    )


class KeyMember(InstanceValue):
    """Single data instance that is part of a key."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.KeyMember,
            "$prefix": "cdi",
        },
    )


class Key(RDFModel, metaclass=ABCMeta):
    """Collection of data instances that uniquely identify a collection of data points in a dataset."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.Key,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "Key-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    Key_identifies_DataPoint: List[AnyHttpUrl] | None = Field(
        default=None,
        description="The instance variable delimits the values which can populate a data point. Data point is described by one instance variable.",
        json_schema_extra={
            "rdf_term": CDI.Key_identifies_DataPoint,
            "rdf_type": "uri",
        },
    )

    Key_has_KeyMember: List[AnyHttpUrl] | None = Field(
        default=None,
        description="Single data instance that is part of a key.",
        json_schema_extra={
            "rdf_term": CDI.Key_has_KeyMember,
            "rdf_type": "uri",
        },
    )


class DataPoint(RDFModel, metaclass=ABCMeta):
    """Container for an instance value."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.DataPoint,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "DataPoint-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    DataPoint_isDescribedBy_InstanceVariable: List[AnyHttpUrl] | None = Field(
        default=None,
        description="The instance variable delimits the values which can populate a data point. Data point is described by one instance variable.",
        json_schema_extra={
            "rdf_term": CDI.DataPoint_isDescribedBy_InstanceVariable,
            "rdf_type": "uri",
        },
    )


class DataSet(RDFModel, metaclass=ABCMeta):
    """Organized collection of data based on keys."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.DataSet,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "DataSet-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    catalogDetails: CatalogDetails | None = Field(
        default=None,
        description="A set of information useful for attribution, data discovery, and access.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "DataSet-catalogDetails"),
            "rdf_type": CDI.CatalogDetails,
        },
    )

    DataSet_has_DataPoint: List[AnyHttpUrl] | None = Field(
        default=None,
        description="Container for an instance value.",
        json_schema_extra={
            "rdf_term": CDI.DataSet_has_DataPoint,
            "rdf_type": "uri",
        },
    )

    DataSet_has_Key: List[AnyHttpUrl] | None = Field(
        default=None,
        description="Collection of data instances that uniquely identify a collection of data points in a dataset.",
        json_schema_extra={
            "rdf_term": CDI.DataSet_has_Key,
            "rdf_type": "uri",
        },
    )

    DataSet_isStructuredBy_DataStructure: List[URIRef] | None = Field(
        default=None,
        description="Data organization based on reusable data structure components.",
        json_schema_extra={
            "rdf_term": CDI.DataSet_isStructuredBy_DataStructure,
            "rdf_type": "uri",
        },
    )


class KeyValueDataStore(DataSet):
    """Organized collection of key-value data. It is structured by a key value structure.."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.KeyValueDataStore,
            "$prefix": "cdi",
        },
    )


class DataStructureComponent(RDFModel, metaclass=ABCMeta):
    """Role given to a represented variable in the context of a data structure."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.DataStructureComponent,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "DataStructureComponent-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    DataStructureComponent_isDefinedBy_RepresentedVariable: URIRef | None = Field(
        default=None,
        description="Conceptual variable with a substantive value domain specified.",
        json_schema_extra={
            "rdf_term": CDI.DataStructureComponent_isDefinedBy_RepresentedVariable,
            "rdf_type": "uri",
        },
    )


class IdentifierComponent(DataStructureComponent):
    """Role given to a represented variable in the context of a long or wide data structure to identify the units associated to data points,
    and in dimensional and key value data structures to provide identifying fields for the instance values.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.IdentifierComponent,
            "$prefix": "cdi",
        },
    )


class AttributeComponent(DataStructureComponent):
    """Role given to a represented variable in the context of a data structure to qualify observations or provide other types of supplementary information."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.AttributeComponent,
            "$prefix": "cdi",
        },
    )


class MeasureComponent(DataStructureComponent):
    """Role given to a represented variable in the context of a data structure to hold the observed/derived values."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.MeasureComponent,
            "$prefix": "cdi",
        },
    )

class VariableDescriptorComponent(DataStructureComponent):
    """Role given to a represented variable in the context of a data structure to provide codes for variable identification."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.VariableDescriptorComponent,
            "$prefix": "cdi",
        },
    )

    VariableDescriptorComponent_refersTo_VariableValueComponent: URIRef | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.VariableDescriptorComponent_refersTo_VariableValueComponent,
            "rdf_type": "uri",
        },
    )

    VariableDescriptorComponent_isDefinedBy_DescriptorVariable: URIRef | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.VariableDescriptorComponent_isDefinedBy_DescriptorVariable,
            "rdf_type": "uri",
        },
    )

class VariableValueComponent(DataStructureComponent):
    """Role given to a represented variable in the context of a data structure to record values of multiple variables."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.VariableValueComponent,
            "$prefix": "cdi",
        },
    )


class DataStructure(DataStructureComponent):
    """Data organization based on reusable data structure components."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.DataStructure,
            "$prefix": "cdi",
        },
    )

    DataStructure_has_DataStructureComponent: List[URIRef] | None = Field(
        default=None,
        description="Role given to a represented variable in the context of a data structure.",
        json_schema_extra={
            "rdf_term": CDI.DataStructure_has_DataStructureComponent,
            "rdf_type": "uri",
        },
    )


class KeyValueStructure(DataStructure):
    """Structure of a key-value datastore (organized collection of key-value data). It is described by identifier, contextual, synthetic id, dimension, variable descriptor and variable value components."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.KeyValueStructure,
            "$prefix": "cdi",
        },
    )


class Notation(RDFModel, metaclass=ABCMeta):
    """Representation of a category in the context of a code or a classification item, as opposed of the corresponding instance value which would appear when used in a dataset."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.Notation,
            "$prefix": "cdi",
        },
    )

    identifier: Identifier | None = Field(
        default=None,
        description="Identifier for objects requiring short- or long-lasting referencing and management.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "Notation-identifier"),
            "rdf_type": CDI.Identifier,
        },
    )

    content: TypedString | None = Field(
        default=None,
        description="The actual content of this value as a string.",
        json_schema_extra={
            "rdf_term": URIRef(CDI + "Notation-content"),
            "rdf_type": CDI.TypedString,
        },
    )

    Notation_represents_Category: List[URIRef] | None = Field(
        default=None,
        description="Notation represents zero to many categories.",
        json_schema_extra={
            "rdf_term": CDI.Notation_represents_Category,
            "rdf_type": "uri",
        },
    )

class DescriptorVariable(RepresentedVariable):
    """Variable that provides codes for variable identification in the context of a data structure. Variable playing the role of a variable descriptor component."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.DescriptorVariable,
            "$prefix": "cdi",
        },
    )

class DescriptorValueDomain(SubstantiveValueDomain):
    """Set of permissible values for a variable playing the role of a variable descriptor component."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.DescriptorValueDomain,
            "$prefix": "cdi",
        },
    )

class ReferenceVariable(RepresentedVariable):
    """Variable that records values of multiple variables in the context of a data structure. Variable playing the role of a variable value component."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.ReferenceVariable,
            "$prefix": "cdi",
        },
    )

    ReferenceVariable_takesValuesFrom_ReferenceValueDomain: URIRef | None = Field(
        default=None,
        description="Points to a value domain that contains values that may be drawn from the domains of multiple simple variables.",
        json_schema_extra={
            "rdf_term": CDI.ReferenceVariable_takesValuesFrom_ReferenceValueDomain,
            "rdf_type": "uri",
        },
    )

class Descriptor(KeyMember):
    """Use of a code for variable identification in the context of a data structure and a variable descriptor component."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.Descriptor,
            "$prefix": "cdi",
        },
    )

    Descriptor_hasValueFrom_DescriptorValueDomain: URIRef | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.Descriptor_hasValueFrom_DescriptorValueDomain,
            "rdf_type": "uri",
        },
    )

    Descriptor_identifies_RepresentedVariable: URIRef | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.Descriptor_identifies_RepresentedVariable,
            "rdf_type": "uri",
        },
    )

    Descriptor_refersTo_ReferenceValue: List[URIRef] | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.Descriptor_refersTo_ReferenceValue,
            "rdf_type": "uri",
        },
    )

class ReferenceValue(InstanceValue):
    """Recorded value in a variable value component. Value referenced by a descriptor."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.ReferenceValue,
            "$prefix": "cdi",
        },
    )

    ReferenceValue_hasValueFrom_ReferenceValueDomain: URIRef | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.ReferenceValue_hasValueFrom_ReferenceValueDomain,
            "rdf_type": "uri",
        },
    )

    ReferenceValue_correspondsTo_VariableValueComponent: URIRef | None = Field(
        default=None,
        description="",
        json_schema_extra={
            "rdf_term": CDI.ReferenceValue_correspondsTo_VariableValueComponent,
            "rdf_type": "uri",
        },
    )

class ReferenceValueDomain(ValueDomain):
    """Set of permissible values for a variable playing the role of a variable value component."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.ReferenceValueDomain,
            "$prefix": "cdi",
        },
    )

class WideDataSet(DataSet):
    """Organized collection of wide data. It is structured by a wide data structure."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.WideDataSet,
            "$prefix": "cdi",
        },
    )


class WideDataStructure(DataStructure):
    """Structure of a wide dataset (organized collection of wide data). It is described by identifier, measure and attribute components."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={
            "$ontology": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "$namespace": str(CDI),
            "$IRI": CDI.WideDataStructure,
            "$prefix": "cdi",
        },
    )
