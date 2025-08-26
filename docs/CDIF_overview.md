# X‑ray Fluorescence Spectra for K‑Edge, Iron c3d (Fe c3d.001)

**Dataset**  
| Item | Value |
|------|-------|
| **ID** | `nx:fe_c3d.001` |
| **Name** | *X‑ray fluorescence spectra for K edge, Iron c3d* |
| **Description** | Metadata example based on a NEXUS NXxas file. |
| **DOI** | <https://doi.org/10.xxxxx/fe_c3d001> |
| **Creation / Modif.** | Latest metadata update: 2025‑08‑20 |
| **Creator** | Richard, Stephen M. (<https://orcid.org/0000-0002-7933-2154>) |
| **Contributor** | APS (Facility, ROR: <https://ror.org/aps>) |
| **License** | *To be FAIR must include license/usage constraint information* |
| **Distribution** | 1 HDF5 file (`FeXAS.nxs`), 2.6 MB, 443 rows × 35 cols, 26 spectra |


## Distribution Details

- **File**: `https://millenia.cars.aps.anl.gov/nxxas/MultiSpectrumFiles/FeXAS.nxs`  
- **Format**: `application/x-hdf5`  
- **Checksum**: MD5 – `0BA77A348`  
- **Conforms To**: *nexus v2024.02*, *NXxas*  
- **Physical Segments**  
  - 26 individual spectra, each a separate NX entry inside the file.  
  - Raw data (`nx:fec3d001RawData`) is a 443 × 35 array; column 0 is `energy` (eV).  
  - Value mappings:  
    * `nx:monochromatorEnergy` → `/Fe_c3d.001/instrument/monochromator/energy`  
    * `nx:incidentIntensity` → `/Fe_c3d.001/instrument/i0/data`  
    * `nx:fluorescenceIntensity` → `/Fe_c3d.001/instrument/ifluor/data`  
    * `nx:mufluorescence` → `/Fe_c3d.001/data/mufluor`  

## Measurement Technique

- **Technique**: X‑Ray Absorption Spectroscopy (XAS)  
  - **Term Code**: `XAS`  
  - **URI**: <https://w3id.org/geochem/1.0/analyticalmethod/xrayabsorptionspectrometry>  
  - **Defined Term Set**: <https://w3id.org/geochem/1.0/analyticalmethod/method>

## Key Variables (Instance Variables)

| Variable | ID | Unit | Range | Description |
|----------|----|------|-------|-------------|
| Monochromator energy | `nx:monochromatorEnergy` | eV | 7052 – 7380.83 | Photon energy selected by the monochromator; independent variable of an XAS scan. |
| Incident intensity (monitor) | `nx:incidentIntensity` | counts | ≥ 0 | X‑ray flux hitting the sample (ionization chamber or photodiode). |
| Fluorescence intensity | `nx:fluorescenceIntensity` | counts | ≥ 0 | Fluorescent X‑ray photons emitted by the sample. |
| Fluorescence absorption coefficient | `nx:mufluorescence` | unitless | ≥ 0 | μ(E) inferred from fluorescence yield. |

### Variable Metadata (SKOS Concepts)

| Concept ID | PrefLabel | Definition |
|------------|-----------|------------|
| `nx:monochromatorEnergyConcept` | Monochromator Energy | Photon energy delivered to the sample; independent variable. |
| `nx:incidentIntensityConcept` | Incident X‑ray Intensity | Measured flux before the sample. |
| `nx:transmittedIntensityConcept` | Transmitted X‑ray Intensity | Flux transmitted through the sample. |
| `nx:fluorescenceAbsorptionCoefficientConcept` | Fluorescence Absorption Coefficient | μ(E) derived from fluorescence. |
| `nx:absorptionCoefficientConcept` | Absorption Coefficient | μ(E) from incident / transmitted flux. |

All concepts belong to the **X‑ray Absorption Spectroscopy Dictionary** (`#xasDict`).

## Instrumentation

- **Facility**: APS (Advanced Photon Source) – <https://ror.org/aps>
- **Beamline**: 13‑ID‑E  
  - Harmonic rejection: 2 Si mirrors, 3 mrad.  
- **Monochromator**: Si 311  
  - d‑spacing: 1.637514293 Å  
- **Location**: <https://ror.org/aps> – 7 GeV undulator, 36 mm aperture, 66 poles.

## Provenance

- **Event**: Analysis event (`nx:analysisEvent`)  
  - **Start**: 2020‑08‑12 04:34:49  
  - **Location**: APS facility (same as above)  
  - **Edge energy**: 7112.000 eV (approx.)  
  - **Sample**: unspecified material.

## Metadata Record

The metadata itself is a separate dataset (`nx:metadata.fe_c3d.001`):

| Field | Value |
|-------|-------|
| **Modified** | 2025‑08‑20 |
| **Creator** | Richard, Stephen M. (ORCID) |
| **About** | `nx:fe_c3d.001` |
| **Conforms To** | `CDIF_basic_1.0`, `nx:nxxasCDIF` |

---

> **Note** – The license information is currently a placeholder and should be updated to a FAIR‑compliant license (e.g., CC‑BY‑4.0) before public release.
# X‑ray Fluorescence Spectra for K‑Edge, Iron c3d (Fe c3d.001)

**Dataset**  
| Item | Value |
|------|-------|
| **ID** | `nx:fe_c3d.001` |
| **Name** | *X‑ray fluorescence spectra for K edge, Iron c3d* |
| **Description** | Metadata example based on a NEXUS NXxas file. |
| **DOI** | <https://doi.org/10.xxxxx/fe_c3d001> |
| **Creation / Modif.** | Latest metadata update: 2025‑08‑20 |
| **Creator** | Richard, Stephen M. (<https://orcid.org/0000-0002-7933-2154>) |
| **Contributor** | APS (Facility, ROR: <https://ror.org/aps>) |
| **License** | *To be FAIR must include license/usage constraint information* |
| **Distribution** | 1 HDF5 file (`FeXAS.nxs`), 2.6 MB, 443 rows × 35 cols, 26 spectra |


## Distribution Details

- **File**: `https://millenia.cars.aps.anl.gov/nxxas/MultiSpectrumFiles/FeXAS.nxs`  
- **Format**: `application/x-hdf5`  
- **Checksum**: MD5 – `0BA77A348`  
- **Conforms To**: *nexus v2024.02*, *NXxas*  
- **Physical Segments**  
  - 26 individual spectra, each a separate NX entry inside the file.  
  - Raw data (`nx:fec3d001RawData`) is a 443 × 35 array; column 0 is `energy` (eV).  
  - Value mappings:  
    * `nx:monochromatorEnergy` → `/Fe_c3d.001/instrument/monochromator/energy`  
    * `nx:incidentIntensity` → `/Fe_c3d.001/instrument/i0/data`  
    * `nx:fluorescenceIntensity` → `/Fe_c3d.001/instrument/ifluor/data`  
    * `nx:mufluorescence` → `/Fe_c3d.001/data/mufluor`  

## Measurement Technique

- **Technique**: X‑Ray Absorption Spectroscopy (XAS)  
  - **Term Code**: `XAS`  
  - **URI**: <https://w3id.org/geochem/1.0/analyticalmethod/xrayabsorptionspectrometry>  
  - **Defined Term Set**: <https://w3id.org/geochem/1.0/analyticalmethod/method>

## Key Variables (Instance Variables)

| Variable | ID | Unit | Range | Description |
|----------|----|------|-------|-------------|
| Monochromator energy | `nx:monochromatorEnergy` | eV | 7052 – 7380.83 | Photon energy selected by the monochromator; independent variable of an XAS scan. |
| Incident intensity (monitor) | `nx:incidentIntensity` | counts | ≥ 0 | X‑ray flux hitting the sample (ionization chamber or photodiode). |
| Fluorescence intensity | `nx:fluorescenceIntensity` | counts | ≥ 0 | Fluorescent X‑ray photons emitted by the sample. |
| Fluorescence absorption coefficient | `nx:mufluorescence` | unitless | ≥ 0 | μ(E) inferred from fluorescence yield. |

### Variable Metadata (SKOS Concepts)

| Concept ID | PrefLabel | Definition |
|------------|-----------|------------|
| `nx:monochromatorEnergyConcept` | Monochromator Energy | Photon energy delivered to the sample; independent variable. |
| `nx:incidentIntensityConcept` | Incident X‑ray Intensity | Measured flux before the sample. |
| `nx:transmittedIntensityConcept` | Transmitted X‑ray Intensity | Flux transmitted through the sample. |
| `nx:fluorescenceAbsorptionCoefficientConcept` | Fluorescence Absorption Coefficient | μ(E) derived from fluorescence. |
| `nx:absorptionCoefficientConcept` | Absorption Coefficient | μ(E) from incident / transmitted flux. |

All concepts belong to the **X‑ray Absorption Spectroscopy Dictionary** (`#xasDict`).

## Instrumentation

- **Facility**: APS (Advanced Photon Source) – <https://ror.org/aps>
- **Beamline**: 13‑ID‑E  
  - Harmonic rejection: 2 Si mirrors, 3 mrad.  
- **Monochromator**: Si 311  
  - d‑spacing: 1.637514293 Å  
- **Location**: <https://ror.org/aps> – 7 GeV undulator, 36 mm aperture, 66 poles.

## Provenance

- **Event**: Analysis event (`nx:analysisEvent`)  
  - **Start**: 2020‑08‑12 04:34:49  
  - **Location**: APS facility (same as above)  
  - **Edge energy**: 7112.000 eV (approx.)  
  - **Sample**: unspecified material.

## Metadata Record

The metadata itself is a separate dataset (`nx:metadata.fe_c3d.001`):

| Field | Value |
|-------|-------|
| **Modified** | 2025‑08‑20 |
| **Creator** | Richard, Stephen M. (ORCID) |
| **About** | `nx:fe_c3d.001` |
| **Conforms To** | `CDIF_basic_1.0`, `nx:nxxasCDIF` |

---

> **Note** – The license information is currently a placeholder and should be updated to a FAIR‑compliant license (e.g., CC‑BY‑4.0) before public release.
