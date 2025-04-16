# PA-EndoMesh

**Mesh-based Extraction of Pulmonary Artery Geometry at End-Diastole from UK Biobank CINE MRI**

## Overview

This project focuses on extracting geometric features of the **pulmonary artery (PA)** from **end-diastolic cardiac meshes** derived from **UK Biobank CINE MRI**. Unlike conventional segmentation-based approaches, we propose a method that leverages the standardized mesh representation of the right heart to localize and quantify the PA.

## Motivation

Pulmonary artery geometry—such as cross-sectional area, major/minor diameters, and shape—plays an important role in cardiovascular health, especially in conditions like pulmonary hypertension and right heart failure.

While prior studies (e.g., Bello et al. 2019, Meng et al. 2021) have used deep learning or segmentation methods to analyze cardiac structure and motion, this work aims to explore an alternative mesh-based pipeline with potential for high anatomical consistency and reproducibility.

## Core Idea

1. **Mesh Standardization**  
   We assume the availability of a standard reference mesh for the right heart at **end-diastole**, generated via deformable registration or template modeling.

2. **Pulmonary Artery Localization**  
   A **reference plane** is manually or programmatically intersected with the template mesh to identify **pulmonary artery (PA) region points** based on their intersection.

3. **Region Propagation**  
   The **point indices** corresponding to the PA region on the template mesh are propagated to individual subject meshes (registered to the same space).

4. **Feature Extraction**  
   Using these localized regions, we compute:
   - Cross-sectional **area**
   - **Major and minor diameters**
   - Optional: curvature, shape features, etc.

## Future Directions

- Integration with segmentation-based localization for better anatomical fidelity
- Temporal tracking of PA region across cardiac cycle
- Population-wide statistical analysis of PA metrics
- Incorporating PA motion or flow information from velocity-encoded MRI

## Dataset

- **UK Biobank CINE MRI**
- Focus: Right heart end-diastole phase
- Mesh format: `.vtk`, standardized across subjects

## References

- Duan J. et al. (2019), *IEEE TMI*
- Bello GA. et al. (2019), *Nature Machine Intelligence*
- Meng Q. et al. (2021), *DeepMesh: Mesh-Based Cardiac Motion Tracking*
- Pirruccello JP. et al. (2022), *Genetic analysis of right heart structure and function*

## Status

🚧 Work in progress.  
📌 Currently building template intersection and PA region mapping module.

---

