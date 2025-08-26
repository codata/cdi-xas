# X‑ray Fluorescence Spectra – Fe K‑edge (c3d) – Metadata Summary  

| Property | Value |
|----------|-------|
| **Name** | X‑ray fluorescence spectra for K edge, Iron c3d |
| **Description** | Metadata example based on NEXUS NXxas file. |
| **Identifier** | <https://doi.org/10.xxxxx/fe_c3d001> |
| **Contributor** | APS (Facility) – ROR: <https://ror.org/aps> |
| **License** | *Placeholder* – “To be FAIR must include license/usage constraint information” |
| **Distribution** | One HDF5 file (`application/x‑hdf5`) at <https://millenia.cars.aps.anl.gov/nxxas/MultiSpectrumFiles/FeXAS.nxs> |
| **Measurement Technique** | X‑ray Absorption Spectroscopy (XAS) – `https://w3id.org/geochem/1.0/analyticalmethod/xrayabsorptionspectrometry` |
| **Keywords** | • K‑edge (ID: `https://xas.org/vocab/absorptionedge/k`)  <br>• Iron (URI placeholder) |
| **Variables Measured** | 1. `nx:monochromatorEnergy` (energy, eV, 7052–7380.83 eV) <br>2. `nx:incidentIntensity` (i0, counts) <br>3. `nx:fluorescenceIntensity` (ifluor, counts) <br>4. `nx:mufluorescence` (mufluor, unitless) |
| **Provenance – Event** | • **Event ID**: *not defined* <br>• **Start**: 2020‑08‑12T04:34:49 <br>• **Instrument**: <br>  - Beamline “13‑ID‑E” (identifier placeholder) <br>  - Monochromator “Si 311” (d-spacing 1.6375 Å) <br>• **Edge Energy**: 7112 eV (unit placeholder) <br>• **Location**: APS, GeV: 7.00 (GeV) <br>• **Main Entity**: MaterialSample (no description) |
| **Dataset Relationships** | • `schema:subjectOf` – Metadata for the dataset (creator: Stephen M. Richard, ORCID <https://orcid.org/0000-0002-7933-2154>) <br>• Conforms to: `CDIF_basic_1.0`, `nx:nxxasCDIF` |
| **Vocabulary** | Skos concept scheme “X‑Ray Absorption Spectroscopy Dictionary” (ID: `#xasDict`) containing concepts for energy, intensity, absorption coefficient, etc. |

---

## Missing / Placeholder Information

| Category | Missing / Placeholder | Notes |
|----------|-----------------------|-------|
| **License** | Actual license URI & usage constraints | “To be FAIR must include license/usage constraint information” – needs a concrete SPDX or CC license URL. |
| **Dataset Identifiers** | `schema:creator`, `schema:publisher`, `schema:dateCreated`, `schema:datePublished`, `schema:version` | Only `schema:subjectOf` has a creator; the main dataset lacks these metadata. |
| **Dataset Conformance** | `dcterms:conformsTo` on the main dataset | Only the subjectOf has conformance metadata. |
| **Distribution Details** | `schema:contentSize` units (bytes vs. MB), `schema:downloadUrl` or `schema:accessURL`, `schema:availability`, `schema:encodingFormat` (full MIME string) | Current `schema:contentSize` is “2.6 Mb” (should be a number with unit); no explicit download URL. |
| **Checksum** | `spdx:checksumValue` length / algorithm | Provided MD5 value seems truncated (`0BA77A348`); full 32‑hex MD5 needed. |
| **Variable Definitions** | Full list of 35 columns in raw data | Only one identifierComponent is described; all other columns (`tscaler`, `i1`–`i7`, `sum_outputcounts`, etc.) are missing definitions. |
| **Variable Identifiers** | `@id`/`identifier` for each variable | Each variable has “should be URI from nexusFormat organization” placeholder. |
| **Variable Units** | `nx:edge_energy` property unit | UnitText is “???” – should be “eV”. |
| **Variable Naming** | Misspelled property `schame:alternateName` for `nx:monochromatorEnergy` | Correct to `schema:alternateName`. |
| **Instrument Registry** | `schema:identifier` for beamline, monochromator | Placeholders “should have a registry with URIs”. |
| **Sample Information** | `schema:mainEntity` description | “no information” – need sample type, composition, thickness, etc. |
| **Sample Location** | Spatial coverage of sample (laboratory, beamline) | Not provided. |
| **Temporal Coverage** | Start/stop times of the scan | Missing. |
| **Access Rights** | `schema:accessMode`, `schema:availability` | No information about open, restricted, embargoed. |
| **Contact / Publisher** | `schema:contactPoint`, `schema:publisher` | Not specified. |
| **Data Provenance** | `schema:creator` for distribution (the person who created the file) | Only event has `schema:identifier`. |
| **Keyword Vocabularies** | URI placeholders for Iron keyword | “URI for iron (CCPAC?)” and “URI for element vocabulary” need to be resolved. |
| **Measurement Range** | Full min/max for each variable (e.g., energy, intensity) | Only energy min/max provided. |
| **Metadata Date** | `schema:dateModified` on main dataset | Only present in subjectOf. |
| **Concept IDs** | `nx:fluorescenceAbsorptionCoefficientConcept` URI mismatch (ID in JSON is `nx:fluorescenceAbsorptionCoefficientConcept`, but variable references `nx:fluorescenceAbsorptionCoefficientConcept`?) | Ensure consistent concept IDs in the Skos list. |

---

## Recommendations

1. **Add a concrete license URI** (e.g., CC‑BY‑4.0 `<https://creativecommons.org/licenses/by/4.0/>` or SPDX `<https://spdx.org/licenses/MIT.html>`).
2. **Populate the main dataset** with `schema:creator`, `schema:publisher`, creation & publication dates, version number, and language.
3. **Describe the full set of raw‑data columns** in the HDF5 file using `identifierComponent`, units, and `skos:definition`.
4. **Resolve URI placeholders** for all variables, keywords, and instrument identifiers using a proper registry (e.g., ROR, IETF, OPC or other relevant ontologies).
5. **Provide full checksum** (algorithm and full 32‑hex MD5 value) and **complete distribution metadata** (`schema:contentSize` in bytes, `schema:downloadUrl`, `schema:availability`).
6. **Define the sample** (`schema:mainEntity`) with material, thickness, environment, and spatial/temporal coverage.
7. **Correct minor syntax errors** (`schame:alternateName` → `schema:alternateName`).
8. **Standardise units** for all numeric fields (e.g., `schema:contentSize` → `2600000` bytes, `schema:unitText` → “eV”, “counts”).
9. **Populate the Skos concept scheme** with the correct IDs (e.g., `nx:fluorescenceAbsorptionCoefficientConcept` vs. `nx:fluorescenceAbsorptionCoefficientConcept`) and ensure all concepts are linked via `schema:propertyID` and `schema:uses`.

Once these gaps are filled, the dataset will comply with CDIF, FAIR, and ISO/OGC data‑management best practices, making it machine‑readable, discoverable, and reusable by the community.
# X‑ray Fluorescence Spectra – Fe K‑edge (c3d) – Metadata Summary  

| Property | Value |
|----------|-------|
| **Name** | X‑ray fluorescence spectra for K edge, Iron c3d |
| **Description** | Metadata example based on NEXUS NXxas file. |
| **Identifier** | <https://doi.org/10.xxxxx/fe_c3d001> |
| **Contributor** | APS (Facility) – ROR: <https://ror.org/aps> |
| **License** | *Placeholder* – “To be FAIR must include license/usage constraint information” |
| **Distribution** | One HDF5 file (`application/x‑hdf5`) at <https://millenia.cars.aps.anl.gov/nxxas/MultiSpectrumFiles/FeXAS.nxs> |
| **Measurement Technique** | X‑ray Absorption Spectroscopy (XAS) – `https://w3id.org/geochem/1.0/analyticalmethod/xrayabsorptionspectrometry` |
| **Keywords** | • K‑edge (ID: `https://xas.org/vocab/absorptionedge/k`)  <br>• Iron (URI placeholder) |
| **Variables Measured** | 1. `nx:monochromatorEnergy` (energy, eV, 7052–7380.83 eV) <br>2. `nx:incidentIntensity` (i0, counts) <br>3. `nx:fluorescenceIntensity` (ifluor, counts) <br>4. `nx:mufluorescence` (mufluor, unitless) |
| **Provenance – Event** | • **Event ID**: *not defined* <br>• **Start**: 2020‑08‑12T04:34:49 <br>• **Instrument**: <br>  - Beamline “13‑ID‑E” (identifier placeholder) <br>  - Monochromator “Si 311” (d-spacing 1.6375 Å) <br>• **Edge Energy**: 7112 eV (unit placeholder) <br>• **Location**: APS, GeV: 7.00 (GeV) <br>• **Main Entity**: MaterialSample (no description) |
| **Dataset Relationships** | • `schema:subjectOf` – Metadata for the dataset (creator: Stephen M. Richard, ORCID <https://orcid.org/0000-0002-7933-2154>) <br>• Conforms to: `CDIF_basic_1.0`, `nx:nxxasCDIF` |
| **Vocabulary** | Skos concept scheme “X‑Ray Absorption Spectroscopy Dictionary” (ID: `#xasDict`) containing concepts for energy, intensity, absorption coefficient, etc. |

---

## Missing / Placeholder Information

| Category | Missing / Placeholder | Notes |
|----------|-----------------------|-------|
| **License** | Actual license URI & usage constraints | “To be FAIR must include license/usage constraint information” – needs a concrete SPDX or CC license URL. |
| **Dataset Identifiers** | `schema:creator`, `schema:publisher`, `schema:dateCreated`, `schema:datePublished`, `schema:version` | Only `schema:subjectOf` has a creator; the main dataset lacks these metadata. |
| **Dataset Conformance** | `dcterms:conformsTo` on the main dataset | Only the subjectOf has conformance metadata. |
| **Distribution Details** | `schema:contentSize` units (bytes vs. MB), `schema:downloadUrl` or `schema:accessURL`, `schema:availability`, `schema:encodingFormat` (full MIME string) | Current `schema:contentSize` is “2.6 Mb” (should be a number with unit); no explicit download URL. |
| **Checksum** | `spdx:checksumValue` length / algorithm | Provided MD5 value seems truncated (`0BA77A348`); full 32‑hex MD5 needed. |
| **Variable Definitions** | Full list of 35 columns in raw data | Only one identifierComponent is described; all other columns (`tscaler`, `i1`–`i7`, `sum_outputcounts`, etc.) are missing definitions. |
| **Variable Identifiers** | `@id`/`identifier` for each variable | Each variable has “should be URI from nexusFormat organization” placeholder. |
| **Variable Units** | `nx:edge_energy` property unit | UnitText is “???” – should be “eV”. |
| **Variable Naming** | Misspelled property `schame:alternateName` for `nx:monochromatorEnergy` | Correct to `schema:alternateName`. |
| **Instrument Registry** | `schema:identifier` for beamline, monochromator | Placeholders “should have a registry with URIs”. |
| **Sample Information** | `schema:mainEntity` description | “no information” – need sample type, composition, thickness, etc. |
| **Sample Location** | Spatial coverage of sample (laboratory, beamline) | Not provided. |
| **Temporal Coverage** | Start/stop times of the scan | Missing. |
| **Access Rights** | `schema:accessMode`, `schema:availability` | No information about open, restricted, embargoed. |
| **Contact / Publisher** | `schema:contactPoint`, `schema:publisher` | Not specified. |
| **Data Provenance** | `schema:creator` for distribution (the person who created the file) | Only event has `schema:identifier`. |
| **Keyword Vocabularies** | URI placeholders for Iron keyword | “URI for iron (CCPAC?)” and “URI for element vocabulary” need to be resolved. |
| **Measurement Range** | Full min/max for each variable (e.g., energy, intensity) | Only energy min/max provided. |
| **Metadata Date** | `schema:dateModified` on main dataset | Only present in subjectOf. |
| **Concept IDs** | `nx:fluorescenceAbsorptionCoefficientConcept` URI mismatch (ID in JSON is `nx:fluorescenceAbsorptionCoefficientConcept`, but variable references `nx:fluorescenceAbsorptionCoefficientConcept`?) | Ensure consistent concept IDs in the Skos list. |

---

## Recommendations

1. **Add a concrete license URI** (e.g., CC‑BY‑4.0 `<https://creativecommons.org/licenses/by/4.0/>` or SPDX `<https://spdx.org/licenses/MIT.html>`).
2. **Populate the main dataset** with `schema:creator`, `schema:publisher`, creation & publication dates, version number, and language.
3. **Describe the full set of raw‑data columns** in the HDF5 file using `identifierComponent`, units, and `skos:definition`.
4. **Resolve URI placeholders** for all variables, keywords, and instrument identifiers using a proper registry (e.g., ROR, IETF, OPC or other relevant ontologies).
5. **Provide full checksum** (algorithm and full 32‑hex MD5 value) and **complete distribution metadata** (`schema:contentSize` in bytes, `schema:downloadUrl`, `schema:availability`).
6. **Define the sample** (`schema:mainEntity`) with material, thickness, environment, and spatial/temporal coverage.
7. **Correct minor syntax errors** (`schame:alternateName` → `schema:alternateName`).
8. **Standardise units** for all numeric fields (e.g., `schema:contentSize` → `2600000` bytes, `schema:unitText` → “eV”, “counts”).
9. **Populate the Skos concept scheme** with the correct IDs (e.g., `nx:fluorescenceAbsorptionCoefficientConcept` vs. `nx:fluorescenceAbsorptionCoefficientConcept`) and ensure all concepts are linked via `schema:propertyID` and `schema:uses`.

Once these gaps are filled, the dataset will comply with CDIF, FAIR, and ISO/OGC data‑management best practices, making it machine‑readable, discoverable, and reusable by the community.
