# Third-party materials

Original `fly_climax` code is MIT (see `LICENSE`). That license does not relicense research data.

## MaleCNS v1.0

Credit: FlyEM at HHMI Janelia, the University of Cambridge Department of Zoology, the MRC Laboratory of Molecular Biology, and Google Research, with the authors of Berg et al., *Cell* 2026.

- Dataset: https://male-cns.janelia.org/download/
- License: Creative Commons Attribution 4.0 International (https://creativecommons.org/licenses/by/4.0/)
- This slice ships locked hop tables in `logs/`. It is not the MaleCNS reconstruction. Feathers stay CC BY. Hashes: `data-provenance/malecns_v1/source.lock.json`.

## Named circuit literature (aliases only)

Gautham et al., *Nature* 632:850 (2024) mapped six MANC bodies and chose four as Crz. Maggio and Chaverra, eLife 108225, split SGNs (5-HT+Glu, accessory glands) from OGNs (OA+Glu, ejaculatory duct). Zer-Krispil et al. 2018 is the CsChrimson pulse this hop table approximates. Those are literature names. MaleCNS type `INXXX149` is the working set. Identity stays candidate until NeuronBridge / Crz-GAL4 matches the four bodies.
