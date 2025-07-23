from io import TextIOWrapper
from cdi.pyro.format_description import LogicalRecord, PhysicalSegmentLayout, ValueMapping, ValueMappingPosition
from skos.model import Concept, ConceptScheme
from cdi.pyro.representations import SubstantiveValueDomain
from cdi.pyro.conceptual import InstanceVariable

from rdflib import Graph, URIRef, SKOS

from cdi.pyro.data_description import Descriptor, DescriptorVariable, IdentifierComponent, KeyValueDataStore, KeyValueStructure, MeasureComponent, ReferenceValue, VariableDescriptorComponent, VariableValueComponent, WideDataSet, WideDataStructure
from cdi.pyro.datatypes import (
    ControlledVocabularyEntry,
    LabelForDisplay,
    LanguageString,
    ObjectName,
    TypedString,
)

# from api.cdi.pyro.format_description import DataStore, LogicalRecord, PhysicalSegmentLayout

CONCEPT = "-concept-"
CONCEPTSCHEME = "#conceptScheme-"
DATASTORE = "#dataStore"
DESCRIPTOR = "#descriptor-"
DESCRIPTORVARIABLE = "#descriptorVariable"
IDENTIFIERCOMPONENT = "#identifierComponent-"
INSTANCEVARIABLE = "#instanceVariable-"
KEYVALUEDATASTORE = "#keyValueDataStore"
KEYVALUESTRUCTURE = "#keyValueStructure"
LOGICALRECORD = "#logicalRecord"
MEASURECOMPONENT = "#measureComponent-"
PHYSICALSEGMENTLAYOUT = "#physicalSegmentLayout"
REFERENCEVALUE = "#referenceValue-"
#REPRESENTEDVARIABLE = "#representedVariable-"
SUBSTANTIVEVALUEDOMAIN = "#substantiveValueDomain-"
VALUEMAPPING = "#valueMapping-"
VALUEMAPPINGPOSITION = "#valueMappingPosition-"
VARIABLEDESCRIPTORCOMPONENT = "#variableDescriptorComponent"
VARIABLEVALUECOMPONENT = "#variableValueComponent"
WIDEDATASET = "#wideDataSet"
WIDEDATASTRUCTURE = "#wideDataStructure"

# def add_data_store_to_graph() -> Graph:
#     data_store_id = DATASTORE

#     data_store = DataStore(
#         DataStore_has_LogicalRecord=[URIRef(LOGICALRECORD + "kv"), URIRef(LOGICALRECORD + "wds")]
#     )

#     g = data_store.to_graph(URIRef(data_store_id))  # type: ignore
#     return g

# def add_key_value_logical_record(key_value_instance_variables: list[str]) -> Graph:
#     key_value_logical_record_id = LOGICALRECORD + "kv"

#     instance_variable_list = [URIRef(INSTANCEVARIABLE + instance_variable) for instance_variable in key_value_instance_variables]

#     key_value_logical_record = LogicalRecord(
#         LogicalRecord_organizes_DataSet=[URIRef(KEYVALUEDATASTORE)],
#         LogicalRecord_has_InstanceVariable = instance_variable_list
#     )

#     g = key_value_logical_record.to_graph(URIRef(key_value_logical_record_id))  # type: ignore
#     return g


# def add_key_value_physical_segment_layout(key_value_instance_variables: list[str]) -> Graph:
#     key_value_physical_segment_layout_id = PHYSICALSEGMENTLAYOUT + "kv"

#     value_mapping_list = [URIRef(VALUEMAPPING + instance_variable) for instance_variable in key_value_instance_variables]

#     key_value_physical_segment_layout = PhysicalSegmentLayout(
#         isDelimited=True,
#         delimiter=":",
#         isFixedWidth=False,
#         PhysicalSegmentLayout_formats_LogicalRecord=[URIRef(LOGICALRECORD + "kv")],
#         PhysicalSegmentLayout_has_ValueMapping=value_mapping_list
#     )

#     g =key_value_physical_segment_layout.to_graph(URIRef(key_value_physical_segment_layout_id))  # type: ignore
#     return g


def add_key_value_data_store_to_graph() -> Graph:
    key_value_data_store_id = KEYVALUEDATASTORE

    key_value_data_store = KeyValueDataStore(DataSet_isStructuredBy_DataStructure=[URIRef(KEYVALUESTRUCTURE)])

    g = key_value_data_store.to_graph(URIRef(key_value_data_store_id))  # type: ignore
    return g


def add_key_value_structure_to_graph() -> Graph:
    key_value_structure_id = KEYVALUESTRUCTURE

    key_value_structure = KeyValueStructure(
        DataStructure_has_DataStructureComponent=[
            URIRef(VARIABLEDESCRIPTORCOMPONENT),
            URIRef(VARIABLEVALUECOMPONENT),
        ]
    )

    g = key_value_structure.to_graph(URIRef(key_value_structure_id))  # type: ignore
    return g


def add_variable_descriptor_component_to_graph() -> Graph:
    variable_descriptor_component_id = VARIABLEDESCRIPTORCOMPONENT

    variable_descriptor_component = VariableDescriptorComponent(
        VariableDescriptorComponent_isDefinedBy_DescriptorVariable=URIRef(DESCRIPTORVARIABLE),
        VariableDescriptorComponent_refersTo_VariableValueComponent=URIRef(VARIABLEVALUECOMPONENT)
    )

    g = variable_descriptor_component.to_graph(URIRef(variable_descriptor_component_id))  # type: ignore
    return g

def add_descriptor_variable_to_graph() -> Graph:
    descriptor_variable_id = DESCRIPTORVARIABLE

    descriptor_variable = DescriptorVariable(
        RepresentedVariable_takesSubstantiveValuesFrom_SubstantiveValueDomain=URIRef(SUBSTANTIVEVALUEDOMAIN + "descriptorVariable")
    )

    g = descriptor_variable.to_graph(URIRef(descriptor_variable_id))  # type: ignore
    return g


def add_substantive_value_domain_to_graph(clss: str, entry_value_str: str) -> Graph:
    substantive_value_domain_id = SUBSTANTIVEVALUEDOMAIN + clss

    entry_value = str(CONCEPTSCHEME + clss) if entry_value_str == "concept_scheme" else "https://www.w3.org/TR/xmlschema-2/#string"

    substantive_value_domain = SubstantiveValueDomain(
        recommendedDataType=ControlledVocabularyEntry(entryValue=entry_value)
    )

    g = substantive_value_domain.to_graph(URIRef(substantive_value_domain_id))  # type: ignore
    return g


def add_concept_scheme_to_graph(clss: str, key_values: list[(str,str)]) -> Graph:
    concept_scheme_id = CONCEPTSCHEME + clss

    #top_concept_list = [URIRef(clss + CONCEPT + key.replace(".","_").replace(" ","_")) for key, _ in key_values]
    top_concept_list = [URIRef(clss + CONCEPT + key.replace(" ","_")) for key, _ in key_values]

    concept_scheme = ConceptScheme(
        hasTopConcept=top_concept_list
    )

    g = concept_scheme.to_graph(URIRef(concept_scheme_id))  # type: ignore
    return g


def add_concept_to_graph(clss: str, key: str) -> Graph:
    #key_str = key.replace(".","_").replace(" ","_")
    key_str = key.replace(" ","_")
    concept_id = clss + CONCEPT + key_str
    print(concept_id)
    concept_id = clss + CONCEPT + key_str
    print(concept_id)

    concept = Concept(
        notation=key,
        prefLabel=key
    )

    g = concept.to_graph(URIRef(concept_id))  # type: ignore
    return g


def add_variable_value_component_to_graph() -> Graph:
    variable_value_component_id = VARIABLEVALUECOMPONENT

    variable_value_component = VariableValueComponent(
        DataStructureComponent_isDefinedBy_RepresentedVariable=URIRef(INSTANCEVARIABLE + "variableValueComponent")
    )

    g = variable_value_component.to_graph(URIRef(variable_value_component_id))  # type: ignore
    return g


# def add_represented_variable_to_graph(clss: str) -> Graph:
#     represented_variable_id = REPRESENTEDVARIABLE + clss

#     represented_variable = InstanceVariable(
#         RepresentedVariable_takesSubstantiveValuesFrom_SubstantiveValueDomain=URIRef(SUBSTANTIVEVALUEDOMAIN + clss)
#     )

#     g = represented_variable.to_graph(URIRef(represented_variable_id))  # type: ignore
#     return g


def add_instance_variable_to_graph(clss: str) -> Graph:
    instance_variable_id = INSTANCEVARIABLE + clss

    instance_variable = InstanceVariable(
        RepresentedVariable_takesSubstantiveValuesFrom_SubstantiveValueDomain=URIRef(SUBSTANTIVEVALUEDOMAIN + clss)
    )

    g = instance_variable.to_graph(URIRef(instance_variable_id))  # type: ignore
    return g


def add_descriptor_to_graph(clss: str) -> Graph:
    descriptor_id = DESCRIPTOR + clss

    content=TypedString(content=clss)

    descriptor = Descriptor(
        content=content,
        #Descriptor_hasValueFrom_DescriptorValueDomain="",
        InstanceValue_hasValueFrom_ValueDomain=URIRef(SUBSTANTIVEVALUEDOMAIN + "descriptorVariable"),
        Descriptor_identifies_RepresentedVariable=URIRef(INSTANCEVARIABLE + clss),
        Descriptor_refersTo_ReferenceValue=[URIRef(REFERENCEVALUE + clss)]
    )

    g = descriptor.to_graph(URIRef(descriptor_id))  # type: ignore
    return g


def add_reference_value_to_graph(clss, value) -> Graph:
    reference_value_id = REFERENCEVALUE + clss

    content=TypedString(content=value)

    reference_value = ReferenceValue(
        content=content,
        InstanceValue_hasValueFrom_ValueDomain=URIRef(SUBSTANTIVEVALUEDOMAIN + clss),
        #ReferenceValue_hasValueFrom_ReferenceValueDomain=
        ReferenceValue_correspondsTo_VariableValueComponent=URIRef(VARIABLEVALUECOMPONENT)
    )

    g = reference_value.to_graph(URIRef(reference_value_id))  # type: ignore
    return g


# def add_instance_variable_to_graph(
#     name: str,
#     display_label: str,
#     physical_data_type: str,
#     described_unit_of_measure: str,
#     concept: str | None,
#     key_value: bool,
#     physical_segment_layout: bool,
#     # file: TextIOWrapper,
#     # output_format: str,
# ) -> Graph:
#     instance_variable_id = INSTANCEVARIABLE + name

#     concept_list: list[URIRef] = []
#     if concept is not None:
#         concept_list.append(URIRef("#" + name + CONCEPT + concept))

#     data_structure = "kv" if key_value else "wds"

#     physical_segment_layout_list: list[URIRef] = []
#     if physical_segment_layout:
#         physical_segment_layout_list.append(
#             URIRef(PHYSICALSEGMENTLAYOUT + data_structure)
#         )

#     instance_variable = InstanceVariable(
#         name=ObjectName(name=name),
#         displayLabel=LabelForDisplay(
#             languageSpecificString=LanguageString(content=display_label)
#         ),
#         physicalDataType=ControlledVocabularyEntry(entryValue=str(physical_data_type)),
#         describedUnitOfMeasure=ControlledVocabularyEntry(
#             entryValue=str(described_unit_of_measure)
#         ),
#         Concept_uses_Concept=concept_list,
#         InstanceVariable_has_ValueMapping=URIRef(VALUEMAPPING + data_structure),
#         InstanceVariable_has_PhysicalSegmentLayout=physical_segment_layout_list,
#         RepresentedVariable_takesSubstantiveValuesFrom_SubstantiveValueDomain=URIRef(
#             SUBSTANTIVEVALUEDOMAIN + data_structure
#         ),
#     )

#     g = instance_variable.to_graph(URIRef(instance_variable_id))  # type: ignore
#     # write_to_graph(graph=g, file=file, output_format=output_format)
#     return g

def add_wide_data_set_to_graph() -> Graph:
    wide_data_set_id = WIDEDATASET
           
    wide_data_set = WideDataSet(
        DataSet_isStructuredBy_DataStructure=[URIRef(WIDEDATASTRUCTURE)],
    )
    g = wide_data_set.to_graph(URIRef(wide_data_set_id))  # type: ignore
    return g


def add_wide_data_structure_to_graph() -> Graph:
    wide_data_structure_id = WIDEDATASTRUCTURE
           
    wide_data_structure = WideDataStructure(
        DataSet_isStructuredBy_DataStructure=[URIRef(WIDEDATASTRUCTURE)],
    )
    g = wide_data_structure.to_graph(URIRef(wide_data_structure_id))  # type: ignore
    return g


def add_logical_record_to_graph(variables: list[str]) -> Graph:
    logical_record_id = LOGICALRECORD

    instance_variable_list = [URIRef(INSTANCEVARIABLE + variable) for variable in variables]
           
    logical_record = LogicalRecord(
        LogicalRecord_organizes_DataSet=[URIRef(WIDEDATASET)],
        LogicalRecord_has_InstanceVariable=instance_variable_list
    )
    g = logical_record.to_graph(URIRef(logical_record_id))  # type: ignore
    return g


def add_identifier_component_to_graph(variable: str) -> Graph:
    identifier_component_id = IDENTIFIERCOMPONENT
           
    identifier_component = IdentifierComponent(
        DataStructureComponent_isDefinedBy_RepresentedVariable=URIRef(INSTANCEVARIABLE + variable)
    )
    g = identifier_component.to_graph(URIRef(identifier_component_id))  # type: ignore
    return g

def add_measure_component_to_graph(variable: str) -> Graph:
    measure_component_id = MEASURECOMPONENT
           
    measure_component = MeasureComponent(
        DataStructureComponent_isDefinedBy_RepresentedVariable=URIRef(INSTANCEVARIABLE + variable)
    )
    g = measure_component.to_graph(URIRef(measure_component_id))  # type: ignore
    return g


def add_physical_segment_layout_to_graph(variables: list[str]) -> Graph:
    physical_segment_layout_id = PHYSICALSEGMENTLAYOUT

    value_mapping_list = [URIRef(VALUEMAPPING + variable) for variable in variables]
    value_mapping_position_list = [URIRef(VALUEMAPPINGPOSITION + variable) for variable in variables]
           
    physical_segment_layout = PhysicalSegmentLayout(
        isFixedWidth=True,
        PhysicalSegmentLayout_formats_LogicalRecord=URIRef(LOGICALRECORD),
        PhysicalSegmentLayout_has_ValueMapping=value_mapping_list,
        PhysicalSegmentLayout_has_ValueMappingPosition=value_mapping_position_list

    )
    g = physical_segment_layout.to_graph(URIRef(physical_segment_layout_id))  # type: ignore
    return g

def add_value_mapping_to_graph(variable: str) -> Graph:
    value_mapping_id = VALUEMAPPING + variable
           
    value_mapping = ValueMapping(
        defaultValue=""
    )
    g = value_mapping.to_graph(URIRef(value_mapping_id))  # type: ignore
    return g


def add_value_mapping_position_to_graph(variable: str, index: int) -> Graph:
    value_mapping_position_id = VALUEMAPPING + variable
           
    value_mapping_position = ValueMappingPosition(
        value=index,
        ValueMappingPosition_indexes_ValueMapping=URIRef(VALUEMAPPING + variable)
    )
    g = value_mapping_position.to_graph(URIRef(value_mapping_position_id))  # type: ignore
    return g


def write_to_graph(graph: Graph, file: TextIOWrapper, output_format: str) -> None:
    # file.write(graph.serialize(format="json-ld", auto_compact=True, context_data=None))
    file.write(graph.serialize(format="json-ld"))
    file.flush()
