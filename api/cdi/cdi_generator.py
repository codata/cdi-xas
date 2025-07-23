from rdflib import Graph

from cdi.cdi_helpers import (
    add_concept_scheme_to_graph,
    add_concept_to_graph,
    add_descriptor_to_graph,
    add_descriptor_variable_to_graph,
    add_identifier_component_to_graph,
    add_instance_variable_to_graph,
    add_key_value_data_store_to_graph,
    add_key_value_structure_to_graph,
    add_logical_record_to_graph,
    add_measure_component_to_graph,
    add_physical_segment_layout_to_graph,
    add_reference_value_to_graph,
    add_substantive_value_domain_to_graph,
    add_value_mapping_position_to_graph,
    add_value_mapping_to_graph,
    add_variable_descriptor_component_to_graph,
    add_variable_value_component_to_graph,
    add_wide_data_set_to_graph,
    add_wide_data_structure_to_graph,
)

def create_key_value_data_store_structures(key_values: list[(str,str)]) -> Graph:

    kvds_g = add_key_value_data_store_to_graph()
    
    kvs_g = add_key_value_structure_to_graph()

    vdc_g = add_variable_descriptor_component_to_graph()

    dv_g = add_descriptor_variable_to_graph() # ????

    svd_dv_g = add_substantive_value_domain_to_graph("descriptorVariable", "concept_scheme")

    cs_dv_g = add_concept_scheme_to_graph("descriptorVariable", key_values)

    vvc_g = add_variable_value_component_to_graph()

    iv_vvc_g = add_instance_variable_to_graph("variableValueComponent")

    svd_vvc_g = add_substantive_value_domain_to_graph("variableValueComponent", "string")

    key_value_g = Graph()

    for key, value in key_values:
        c_dv_g = add_concept_to_graph("descriptorVariable", key)
        d_g = add_descriptor_to_graph(key)
        rv_g = add_reference_value_to_graph(key, value)
        iv_d_g = add_instance_variable_to_graph(key)
        cs_d_g = Graph()
       
        c1_d_g = Graph()
        c2_d_g = Graph()

        if key == "Column.1":
            svd_d_g = add_substantive_value_domain_to_graph(key, "concept_scheme") # TODO from ontology pick up possible values
            cs_d_g = add_concept_scheme_to_graph(key, [("energy",""),("energy eV","")])

            c1_d_g = add_concept_to_graph(key, "energy")
            c2_d_g = add_concept_to_graph(key, "energy eV")

        else:
            svd_d_g = add_substantive_value_domain_to_graph(key, "string") # TODO from ontology pick up possible values

        key_value_g = key_value_g + c_dv_g + d_g + rv_g + iv_d_g + svd_d_g + cs_d_g + c1_d_g + c2_d_g

    combined_graph = kvds_g + kvs_g + vdc_g + dv_g + svd_dv_g + cs_dv_g + vvc_g + iv_vvc_g + svd_vvc_g + key_value_g
    print(combined_graph.serialize())

    return combined_graph


def create_wide_data_set_structures(key_values: list[(str,str)]) -> Graph:
    combined_graph = Graph()

    wds_g = add_wide_data_set_to_graph()

    identifier_variables = ["energy","time"]
    measure_variables = ["itrans","i0"]

    wdst_g = add_wide_data_structure_to_graph(identifier_variables, measure_variables)

    lr_g = add_logical_record_to_graph(identifier_variables + measure_variables)

    psl_g = add_physical_segment_layout_to_graph(identifier_variables + measure_variables)

    for variable in identifier_variables:
        ic_g = add_identifier_component_to_graph(variable)
        combined_graph = combined_graph + ic_g

    for variable in measure_variables:
        mc_g = add_measure_component_to_graph(variable)
        combined_graph = combined_graph + mc_g

    index = 0
    for variable in (identifier_variables + measure_variables):
        iv_g = add_instance_variable_to_graph(variable)
        svd_g = add_substantive_value_domain_to_graph(variable)
        vm_g = add_value_mapping_to_graph(variable)
        vmp_g = add_value_mapping_position_to_graph(variable, index)
        combined_graph = combined_graph + iv_g + svd_g + vm_g + vmp_g
        index+=1
    
    # primary_key?

    combined_graph = combined_graph + wds_g + wdst_g  + lr_g + psl_g

    return combined_graph

