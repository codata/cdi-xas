# X‑ray Fluorescence Spectra – Fe c3d (K‑edge)  
*Metadata description (JSON‑LD → RDF → Markdown)*  

---

## 1. Overview  

| Field | Value |
|-------|-------|
| **Dataset ID** | `nx:fe_c3d.001` |
| **Name** | *X‑ray fluorescence spectra for K edge, Iron c3d* |
| **Description** | Metadata example based on a NEXUS NXxas file. |
| **Publisher** | APS (Advanced Photon Source) – `https://ror.org/aps` |
| **License** | Placeholder – “To be FAIR must include license/usage constraint information.” |
| **Distribution** | One HDF5 file (`FeXAS.nxs`, 2.6 MB) containing 26 spectra. |
| **Measurement Technique** | X‑Ray Absorption Spectroscopy (XAS) – K‑edge at 7112 eV. |
| **Keywords** | *K‑edge*, *Iron* (SKOS terms). |
| **Provenance** | Generated on 12 Aug 2020 by beamline 13‑ID‑E (Si 311 monochromator). |
| **Last Modified** | 20 Aug 2025 (metadata only). |

---

## 2. JSON‑LD Context & Vocabulary

| Prefix | Namespace |
|--------|-----------|
| `schema:` | `https://schema.org/` |
| `dcterms:` | `http://purl.org/dc/terms/` |
| `geosparql:` | `http://www.opengis.net/ont/geosparql#` |
| `spdx:` | `http://spdx.org/rdf/terms#` |
| `cdi:` | `http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/` |
| `time:` | `http://www.w3.org/2006/time#` |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` |
| `nx:` | `https://xas.org/dictionary/` |

These namespaces map the JSON‑LD to a **RDF graph** that can be queried with SPARQL or visualised with any RDF tool.

---

## 3. Dataset Structure

### 3.1 Top‑Level Dataset (`nx:fe_c3d.001`)

- **Type**: `schema:Dataset`, `schema:Product`  
- **Identifier**: DOI placeholder  
- **Contributors**: Facility (APS)  
- **License**: TBD (must comply with FAIR)  
- **Distribution**: One `DataDownload` + `PhysicalDataSet`

### 3.2 Distribution – HDF5 File

| Attribute | Value |
|-----------|-------|
| `contentUrl` | `https://millenia.cars.aps.anl.gov/nxxas/MultiSpectrumFiles/FeXAS.nxs` |
| `description` | “HDF5 file … 26 spectra, each a separate NEXUS entry.” |
| `checksum` | MD5 (`0BA77A348`) |
| `size` | 2.6 MB |
| `encodingFormat` | `application/x-hdf5` |
| `conformsTo` | `nexus v2024.02`, `NXxas` |
| **PhysicalRecordSegment** | Encodes a *wide* data structure (35 columns × 443 rows). |
| **LogicalRecord** | `nx:nxxasfec3d001structure` – a `DimensionalDataSet` describing the scan table. |

### 3.3 Data Structure (Simplified)

```
[Scan Table]
   ├─ energy (Monochromator energy)  – column 0 (443 values)
   ├─ fluorescence intensity (ifluor)
   ├─ incident intensity (i0)
   ├─ μ(E) fluorescence (mufluor)
   └─ … 30 other measurement columns
```

The HDF5 paths for each column are given by `cdifq:hdf5path` (e.g. `Fe_c3d.001/instrument/monochromator/energy`).

---

## 4. Measurement Variables (InstanceVariables)

| Variable | Type | Unit | Range | Notes |
|----------|------|------|-------|-------|
| `nx:monochromatorEnergy` | energy | eV | 7052 – 7380.83 | Independent variable |
| `nx:incidentIntensity` | counts | counts | >0 | Monitor intensity (`i0`) |
| `nx:fluorescenceIntensity` | counts | counts | >0 | Fluorescence signal (`ifluor`) |
| `nx:mufluorescence` | μ(E) | unitless | >0 | Fluorescence‑derived absorption coefficient |

Each variable is linked to a **SKOS concept** (`…Concept`) that provides a controlled definition and URI.

---

## 5. Provenance (`prov:wasGeneratedBy`)

- **Event**: `nx:analysisEvent` (schema:Event)  
- **Date**: 12 Aug 2020 04:34:49  
- **Instrument**:  
  - **Beamline**: 13‑ID‑E (Si 311, 2 Si mirrors, 3 mrad harmonic rejection).  
  - **Monochromator**: Si 311 crystal, d‑spacing 1.6375 Å.  
- **Location**: APS (GeV energy 7.00, undulator 36 mm, 66 poles).  
- **Main Entity**: material sample (no further detail).  
- **Additional Properties**: Edge energy 7112 eV.

This chain records *how* the data were produced, which instruments were used, and the *context* of the measurement.

---

## 6. SKOS Vocabulary (`#xasDict`)

A **concept scheme** for X‑ray Absorption Spectroscopy metadata.

| Concept | PrefLabel | Definition |
|---------|-----------|------------|
| `nx:monochromatorEnergyConcept` | Monochromator Energy | Incident photon energy; independent variable. |
| `nx:incidentIntensityConcept` | Incidnent X‑ray intensity | Flux hitting the sample, measured before the sample. |
| `nx:transmittedIntensityConcept` | Transmitted X‑ray intensity | Flux after the sample. |
| `nx:fluorescenceAbsorptionCoefficientConcept` | Fluorescence Absorption Coefficient | μ(E) derived from fluorescence yield. |
| `nx:absorptionCoefficientConcept` | Absorption Coefficient | μ(E) derived from transmission. |

These concepts standardise terminology, enable semantic querying, and facilitate data integration.

---

## 7. Methodology of the Data

1. **Experimental Setup**  
   - Beamline 13‑ID‑E (APS) with a Si 311 monochromator.  
   - 2 Si mirrors for harmonic rejection; 3 mrad acceptance.  
   - X‑ray energy tuned across the Fe K‑edge (≈ 7112 eV).  

2. **Data Acquisition**  
   - 443 energy steps per scan.  
   - Simultaneous recording of:  
     - Monochromator energy (`energy`)  
     - Incident intensity (`i0`) via an ionisation chamber.  
     - Fluorescence intensity (`ifluor`) via a detector positioned around the sample.  
     - Derived μ(E) fluorescence (`mufluor`).  
   - 26 spectra stored as separate NEXUS entries.

3. **Data Storage**  
   - Encapsulated in a single HDF5 file (`FeXAS.nxs`).  
   - Conforms to `NXxas` application definition (NEXUS 2024.02).  
   - HDF5 paths are documented for each column, ensuring reproducibility.

4. **Metadata Generation**  
   - Using JSON‑LD to capture both **structural** (dataset, distribution) and **semantic** (variables, concepts) information.  
   - Provenance recorded with `prov:wasGeneratedBy`.  
   - Variables linked to controlled SKOS concepts to guarantee consistent interpretation.

5. **FAIR Considerations**  
   - **Findable**: Unique DOI placeholder, rich metadata, controlled vocabularies.  
   - **Accessible**: Direct URL to the HDF5 file.  
   - **Interoperable**: RDF/JSON‑LD format, SKOS vocabularies, NEXUS standard.  
   - **Reusable**: Provenance and variable definitions allow re‑analysis and integration with other XAS datasets.

---

## 8. Usage Notes

- **Download**: `curl -O https://millenia.cars.aps.anl.gov/nxxas/MultiSpectrumFiles/FeXAS.nxs`  
- **Inspection**:  
  ```bash
  h5dump -d Fe_c3d.001/scan/data FeXAS.nxs
  ```
- **Variable Names** (CSV header):  
  `energy,tscaler,i0,i1,i2,sum_outputcounts,sum_fe_ka,outputcounts_mca1,…,dtfactor_mca7`  
- **License**: Replace the placeholder with an appropriate SPDX license (e.g., `CC-BY-4.0`) once finalized.

---

## 9. Summary

The JSON‑LD snippet describes a **single XAS experiment** (Fe K‑edge) stored in an HDF5 file, with a fully‑annotated **semantic layer**.  
It links **data elements** (variables, values) to **controlled concepts**, records the **experimental provenance**, and ensures the dataset is **FAIR** by following NEXUS, RDF, and SKOS best practices.  

Feel free to adapt the schema or enrich the metadata (e.g., add sample description, full instrument parameters) to meet your specific data‑sharing or integration needs.
# X‑ray Fluorescence Spectra – Fe c3d (K‑edge)  
*Metadata description (JSON‑LD → RDF → Markdown)*  

---

## 1. Overview  

| Field | Value |
|-------|-------|
| **Dataset ID** | `nx:fe_c3d.001` |
| **Name** | *X‑ray fluorescence spectra for K edge, Iron c3d* |
| **Description** | Metadata example based on a NEXUS NXxas file. |
| **Publisher** | APS (Advanced Photon Source) – `https://ror.org/aps` |
| **License** | Placeholder – “To be FAIR must include license/usage constraint information.” |
| **Distribution** | One HDF5 file (`FeXAS.nxs`, 2.6 MB) containing 26 spectra. |
| **Measurement Technique** | X‑Ray Absorption Spectroscopy (XAS) – K‑edge at 7112 eV. |
| **Keywords** | *K‑edge*, *Iron* (SKOS terms). |
| **Provenance** | Generated on 12 Aug 2020 by beamline 13‑ID‑E (Si 311 monochromator). |
| **Last Modified** | 20 Aug 2025 (metadata only). |

---

## 2. JSON‑LD Context & Vocabulary

| Prefix | Namespace |
|--------|-----------|
| `schema:` | `https://schema.org/` |
| `dcterms:` | `http://purl.org/dc/terms/` |
| `geosparql:` | `http://www.opengis.net/ont/geosparql#` |
| `spdx:` | `http://spdx.org/rdf/terms#` |
| `cdi:` | `http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/` |
| `time:` | `http://www.w3.org/2006/time#` |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` |
| `nx:` | `https://xas.org/dictionary/` |

These namespaces map the JSON‑LD to a **RDF graph** that can be queried with SPARQL or visualised with any RDF tool.

---

## 3. Dataset Structure

### 3.1 Top‑Level Dataset (`nx:fe_c3d.001`)

- **Type**: `schema:Dataset`, `schema:Product`  
- **Identifier**: DOI placeholder  
- **Contributors**: Facility (APS)  
- **License**: TBD (must comply with FAIR)  
- **Distribution**: One `DataDownload` + `PhysicalDataSet`

### 3.2 Distribution – HDF5 File

| Attribute | Value |
|-----------|-------|
| `contentUrl` | `https://millenia.cars.aps.anl.gov/nxxas/MultiSpectrumFiles/FeXAS.nxs` |
| `description` | “HDF5 file … 26 spectra, each a separate NEXUS entry.” |
| `checksum` | MD5 (`0BA77A348`) |
| `size` | 2.6 MB |
| `encodingFormat` | `application/x-hdf5` |
| `conformsTo` | `nexus v2024.02`, `NXxas` |
| **PhysicalRecordSegment** | Encodes a *wide* data structure (35 columns × 443 rows). |
| **LogicalRecord** | `nx:nxxasfec3d001structure` – a `DimensionalDataSet` describing the scan table. |

### 3.3 Data Structure (Simplified)

```
[Scan Table]
   ├─ energy (Monochromator energy)  – column 0 (443 values)
   ├─ fluorescence intensity (ifluor)
   ├─ incident intensity (i0)
   ├─ μ(E) fluorescence (mufluor)
   └─ … 30 other measurement columns
```

The HDF5 paths for each column are given by `cdifq:hdf5path` (e.g. `Fe_c3d.001/instrument/monochromator/energy`).

---

## 4. Measurement Variables (InstanceVariables)

| Variable | Type | Unit | Range | Notes |
|----------|------|------|-------|-------|
| `nx:monochromatorEnergy` | energy | eV | 7052 – 7380.83 | Independent variable |
| `nx:incidentIntensity` | counts | counts | >0 | Monitor intensity (`i0`) |
| `nx:fluorescenceIntensity` | counts | counts | >0 | Fluorescence signal (`ifluor`) |
| `nx:mufluorescence` | μ(E) | unitless | >0 | Fluorescence‑derived absorption coefficient |

Each variable is linked to a **SKOS concept** (`…Concept`) that provides a controlled definition and URI.

---

## 5. Provenance (`prov:wasGeneratedBy`)

- **Event**: `nx:analysisEvent` (schema:Event)  
- **Date**: 12 Aug 2020 04:34:49  
- **Instrument**:  
  - **Beamline**: 13‑ID‑E (Si 311, 2 Si mirrors, 3 mrad harmonic rejection).  
  - **Monochromator**: Si 311 crystal, d‑spacing 1.6375 Å.  
- **Location**: APS (GeV energy 7.00, undulator 36 mm, 66 poles).  
- **Main Entity**: material sample (no further detail).  
- **Additional Properties**: Edge energy 7112 eV.

This chain records *how* the data were produced, which instruments were used, and the *context* of the measurement.

---

## 6. SKOS Vocabulary (`#xasDict`)

A **concept scheme** for X‑ray Absorption Spectroscopy metadata.

| Concept | PrefLabel | Definition |
|---------|-----------|------------|
| `nx:monochromatorEnergyConcept` | Monochromator Energy | Incident photon energy; independent variable. |
| `nx:incidentIntensityConcept` | Incidnent X‑ray intensity | Flux hitting the sample, measured before the sample. |
| `nx:transmittedIntensityConcept` | Transmitted X‑ray intensity | Flux after the sample. |
| `nx:fluorescenceAbsorptionCoefficientConcept` | Fluorescence Absorption Coefficient | μ(E) derived from fluorescence yield. |
| `nx:absorptionCoefficientConcept` | Absorption Coefficient | μ(E) derived from transmission. |

These concepts standardise terminology, enable semantic querying, and facilitate data integration.

---

## 7. Methodology of the Data

1. **Experimental Setup**  
   - Beamline 13‑ID‑E (APS) with a Si 311 monochromator.  
   - 2 Si mirrors for harmonic rejection; 3 mrad acceptance.  
   - X‑ray energy tuned across the Fe K‑edge (≈ 7112 eV).  

2. **Data Acquisition**  
   - 443 energy steps per scan.  
   - Simultaneous recording of:  
     - Monochromator energy (`energy`)  
     - Incident intensity (`i0`) via an ionisation chamber.  
     - Fluorescence intensity (`ifluor`) via a detector positioned around the sample.  
     - Derived μ(E) fluorescence (`mufluor`).  
   - 26 spectra stored as separate NEXUS entries.

3. **Data Storage**  
   - Encapsulated in a single HDF5 file (`FeXAS.nxs`).  
   - Conforms to `NXxas` application definition (NEXUS 2024.02).  
   - HDF5 paths are documented for each column, ensuring reproducibility.

4. **Metadata Generation**  
   - Using JSON‑LD to capture both **structural** (dataset, distribution) and **semantic** (variables, concepts) information.  
   - Provenance recorded with `prov:wasGeneratedBy`.  
   - Variables linked to controlled SKOS concepts to guarantee consistent interpretation.

5. **FAIR Considerations**  
   - **Findable**: Unique DOI placeholder, rich metadata, controlled vocabularies.  
   - **Accessible**: Direct URL to the HDF5 file.  
   - **Interoperable**: RDF/JSON‑LD format, SKOS vocabularies, NEXUS standard.  
   - **Reusable**: Provenance and variable definitions allow re‑analysis and integration with other XAS datasets.

---

## 8. Usage Notes

- **Download**: `curl -O https://millenia.cars.aps.anl.gov/nxxas/MultiSpectrumFiles/FeXAS.nxs`  
- **Inspection**:  
  ```bash
  h5dump -d Fe_c3d.001/scan/data FeXAS.nxs
  ```
- **Variable Names** (CSV header):  
  `energy,tscaler,i0,i1,i2,sum_outputcounts,sum_fe_ka,outputcounts_mca1,…,dtfactor_mca7`  
- **License**: Replace the placeholder with an appropriate SPDX license (e.g., `CC-BY-4.0`) once finalized.

---

## 9. Summary

The JSON‑LD snippet describes a **single XAS experiment** (Fe K‑edge) stored in an HDF5 file, with a fully‑annotated **semantic layer**.  
It links **data elements** (variables, values) to **controlled concepts**, records the **experimental provenance**, and ensures the dataset is **FAIR** by following NEXUS, RDF, and SKOS best practices.  

Feel free to adapt the schema or enrich the metadata (e.g., add sample description, full instrument parameters) to meet your specific data‑sharing or integration needs.
