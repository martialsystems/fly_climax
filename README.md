# fly_climax

The public-connectome equivalent of Zer-Krispil et al. 2018, as far as MaleCNS v1.0 can go. Four `INXXX149` candidates clamped as CsChrimson. Identity is candidate. Climax is not simulated.

**Question.** If the four MaleCNS INXXX149 cells (Gautham core 4) are clamped as a CsChrimson pulse, how much one- and two-synapse weight lands on AbNT effectors versus local AG interneurons, and does a toy LIF cross an invented ejaculation threshold?

**Answer.** Hop-1 from FOUR: 24,234 synapses onto 457 posts. 11,596 (47.9%) stay in A7-A9 `vnc_intrinsic` cells. 8,132 (33.6%) hit `vnc_efferent` plus `vnc_motor`. 7,776 (32.1%) of the total is AbNT effectors. Named exiting cells are almost all octopaminergic EN00B*: OGN-shaped, ejaculatory-duct side. OGN-like OA AbNT / EN00B* take 3,327. The SGN-like hole is 13 unlabeled AbNT efferents, 3,564 synapses, consensus NT unclear. Consensus 5-HT on AbNT is 0. Predicted transmitter on the four command cells is ACh, not corazonin. The toy LIF (top 20 hop-1 partners, 100 Hz clamp, 3 s) does not cross the invented 40 Hz bar. That bar is a sanity check that the graph is wired toward AbNT, not a biological result. NeuronBridge / Crz-GAL4 still has to match these four bodies to abgCrz.

This circuit shape matches Gautham/Thornquist and the Tayler command-cell story at the level of posterior AG cells that dump about a third of their synapses onto trunk-nerve effectors. It does not lock peptide identity. `INXXX149` is not typed Crz.

| Question | Answer |
|----------|--------|
| Did you find named abgCrz in MaleCNS? | No |
| Best candidate? | INXXX149 four-cell core |
| Does driving them hit reproductive-tract nerves? | Yes, ~32% hop-1 to AbNT |
| OGN / duct path? | Present (EN00B010 and other OA EN00B*) |
| SGN / accessory-gland 5-HT path? | Missing |
| Locked Crz identity? | No. Need Crz-GAL4 or antibody against these body IDs |
| Orgasm simulated? | No |

Copied from `logs/`. Weight is synapse count on the MaleCNS v1.0 significant-only table. Sign: ACh/Glu/OA/5HT excitatory, GABA inhibitory, unclear unsigned. FOUR are ACh, so hop-1 current is excitatory. Sensitivity bodies 801013 and 800166 are not in the drive sum. The next experiment is wet: NeuronBridge / Crz-GAL4 MCFO against these four meshes, and transmitter ID on the 13 unlabeled AbNT cells. Do not run another ejaculation threshold.

## Working set

| bodyId | set | type | side | neuromere | mancBodyid | consensus NT |
|-------:|-----|------|------|-----------|----------:|--------------|
| 800571 | four | INXXX149 | R | A8 | 16132 | acetylcholine |
| 800986 | four | INXXX149 | L | A9 | 14161 | acetylcholine |
| 802096 | four | INXXX149 | R | A7 | 14938 | acetylcholine |
| 904047 | four | INXXX149 | L | A8 | 13190 | acetylcholine |
| 801013 | sensitivity | INXXX149 | L | A7 | 16802 | acetylcholine |
| 800166 | sensitivity | INXXX149 | R | A9 | 16597 | acetylcholine |

## Hop-1 from FOUR

`logs/drive_summary.json`, `logs/hop1.json`

| pool | n | weight | fraction |
|------|--:|-------:|---------:|
| total | 457 | 24,234 | 1 |
| local AG INs (A7-A9 vnc_intrinsic) | 156 | 11,596 | 0.4785 |
| all vnc_intrinsic |  | 14,880 | 0.6140 |
| exiting effectors (vnc_efferent + vnc_motor) | 96 | 8,132 | 0.3356 |
| AbNT efferents + motor | 67 | 7,776 | 0.3209 |
| AbNT efferent | 34 | 6,891 |  |
| AbNT motor | 33 | 885 |  |
| OGN-like (OA AbNT / EN00B*) | 21 | 3,327 |  |
| SGN-like hole (unlabeled AbNT, NT not OA) | 13 | 3,564 |  |

Signed hop-1 weight: +13,450 excitatory, -3,055 inhibitory, 7,729 unsigned. Reciprocal synapses among FOUR: 1,834.

### EN00B*

| bodyId | type | exitNerve | hop1 | consensus NT |
|-------:|------|-----------|-----:|--------------|
| 808163 | EN00B010 | AbNT | 478 | octopamine |
| 809974 | EN00B010 | AbNT | 409 | octopamine |
| 907835 | EN00B010 | AbNT | 396 | octopamine |
| 804275 | EN00B010 | AbNT | 353 | octopamine |
| 808856 | EN00B004 | AbNT_L,AbNT | 306 | octopamine |
| 803005 | EN00B004 | AbNT | 295 | octopamine |
| 803015 | EN00B020 | AbNT | 222 | octopamine |
| 810453 | EN00B016 | AbNT | 195 | octopamine |
| 806591 | EN00B012 | AbNT | 149 | octopamine |
| 811414 | EN00B016 | AbNT | 117 | octopamine |
| 817838 | EN00B013 | AbNT | 95 | octopamine |
| 802672 | EN00B016 | AbNT | 73 | octopamine |
| 800615 | EN00B013 | AbNT | 66 | octopamine |
| 808353 | EN00B013 | AbNT | 54 | octopamine |
| 801636 | EN00B013 | AbNT | 40 | octopamine |
| 802372 | EN00B018 | AbNT | 30 | octopamine |
| 903484 | EN00B003 | AbNT | 20 | octopamine |
| 811431 | EN00B019 | AbNT,AbN4 | 19 | octopamine |
| 801521 | EN00B002 | AbNT | 8 | octopamine |
| 803500 | EN00B003 | AbNT | 1 | octopamine |
| 819342 | EN00B023 | AbNT | 1 | octopamine |

EN00B010 four copies: 1,636. Every EN00B* hop-1 target is consensus octopamine AbNT.

### Unlabeled AbNT efferents (SGN-like hole)

NT is not OA. Consensus is unclear. The public feather has a single predicted-NT confidence, not a per-class vector.

| bodyId | hop1 | consensus NT | predicted NT | pred conf |
|-------:|-----:|--------------|--------------|----------:|
| 814470 | 380 | unclear | unclear | 0.220 |
| 936838 | 378 | unclear | unclear | 0.919 |
| 815445 | 339 | unclear | unclear | 0.732 |
| 808454 | 331 | unclear | unclear | 0.975 |
| 816976 | 324 | unclear | unclear | 0.593 |
| 818737 | 296 | unclear | unclear | 0.651 |
| 800930 | 291 | unclear | unclear | 0.488 |
| 808456 | 285 | unclear | unclear | 0.593 |
| 909643 | 266 | unclear | unclear | 0.423 |
| 808457 | 262 | unclear | unclear | 0.900 |
| 911713 | 230 | unclear | unclear | 0.521 |
| 802978 | 118 | unclear | unclear | 0.888 |
| 810859 | 64 | unclear | unclear | 0.282 |

## Unlabeled AbNT vs Maggio/Chaverra

`logs/unlabeled_abnt.json`. Annotations and NT only. Hop tables not rebuilt. Chaverra et al. eLife 14:RP108225 define SGN as 5-HT+Glu (accessory-gland biased) and OGN as OA+Glu (ejaculatory-duct biased). That paper does not publish MaleCNS or MANC body IDs. Consensus serotonin on AbNT is 0. Axon after AbNT (accessory gland vs seminal vesicle vs ejaculatory duct vs body wall) is not in the annotation table.

| bodyId | type | superclass | exitNerve | soma | pred / consensus NT | MANC | axon after AbNT | Maggio class | grade |
|-------:|------|------------|-----------|------|---------------------|------|-----------------|--------------|-------|
| 808163 | EN00B010 | vnc_efferent | AbNT | A10 M | unclear 0.654 / octopamine | 168470 EN00B010 | no organ target in annotations | OGN-like | morphological guess |
| 809974 | EN00B010 | vnc_efferent | AbNT | A10 M | unclear 0.488 / octopamine | 11765 EN00B010 | no organ target in annotations | OGN-like | morphological guess |
| 907835 | EN00B010 | vnc_efferent | AbNT | A10 M | unclear 0.768 / octopamine | 11092 EN00B010 | no organ target in annotations | OGN-like | morphological guess |
| 804275 | EN00B010 | vnc_efferent | AbNT | A10 M | unclear 0.905 / octopamine | 11453 EN00B010 | no organ target in annotations | OGN-like | morphological guess |
| 814470 | unlabeled | vnc_efferent | AbNT | A10 M 00B | unclear 0.220 / unclear | 23324, no mancType | no organ target in annotations | unknown | no data |
| 936838 | unlabeled | vnc_efferent | AbNT | A10 M 00B | unclear 0.919 / unclear | unmapped | no organ target in annotations | unknown | no data |
| 815445 | unlabeled | vnc_efferent | AbNT | A10 M 00B | unclear 0.732 / unclear | 28535, no mancType | no organ target in annotations | unknown | no data |
| 808454 | unlabeled | vnc_efferent | AbNT | A10 M 00B | unclear 0.975 / unclear | 15736, no mancType | no organ target in annotations | unknown | no data |
| 816976 | unlabeled | vnc_efferent | AbNT | A10 M 00B | unclear 0.593 / unclear | 17776, no mancType | no organ target in annotations | unknown | no data |
| 818737 | unlabeled | vnc_efferent | AbNT | A8 M 00B | unclear 0.651 / unclear | 16791, no mancType | no organ target in annotations | unknown | no data |
| 800930 | unlabeled | vnc_efferent | AbNT | A10 M 00B | unclear 0.488 / unclear | 13826, no mancType | no organ target in annotations | unknown | no data |
| 808456 | unlabeled | vnc_efferent | AbNT | A10 M 00B | unclear 0.593 / unclear | 11334, no mancType | no organ target in annotations | unknown | no data |
| 909643 | unlabeled | vnc_efferent | AbNT | A10 M 00B | unclear 0.423 / unclear | 13576, no mancType | no organ target in annotations | unknown | no data |
| 808457 | unlabeled | vnc_efferent | AbNT | A10 M 00B | unclear 0.900 / unclear | 21104, no mancType | no organ target in annotations | unknown | no data |
| 911713 | unlabeled | vnc_efferent | AbNT | A10 M 00B | unclear 0.521 / unclear | 11469, no mancType | no organ target in annotations | unknown | no data |
| 802978 | unlabeled | vnc_efferent | AbNT | A8 M 00B | unclear 0.888 / unclear | 11296, no mancType | no organ target in annotations | unknown | no data |
| 810859 | unlabeled | vnc_efferent | AbNT | A9 R | unclear 0.282 / unclear | 11972, no mancType | no organ target in annotations | unknown | no data |

EN00B010 controls come out OGN-like: typed EN00B010, consensus octopamine, AbNT. The 13 have no type, no mancType, consensus NT unclear, consensus serotonin absent. The Tayler SGN step is not in these 13 as identified 5-HT. Only the OGN duct-shaped OA EN00B path is in the graph.

### MNad* (hop1 >= 10; 60 posts in `logs/hop1.json`)

| bodyId | type | exitNerve | hop1 | consensus NT |
|-------:|------|-----------|-----:|--------------|
| 802114 | MNad66 | AbNT | 281 | unclear |
| 806779 | MNad09 | AbNT | 168 | unclear |
| 908285 | MNad50 | AbNT | 118 | unclear |
| 905584 | MNad66 | AbNT | 101 | unclear |
| 802137 | MNad19 | AbN4 | 72 | unclear |
| 801491 | MNad19 | AbN4 | 44 | unclear |
| 811952 | MNad07 | AbN4 | 38 | unclear |
| 806643 | MNad05 | AbN4 | 35 | unclear |
| 800664 | MNad64 | AbNT | 31 | gaba |
| 801394 | MNad67 | AbNT | 30 | unclear |
| 811554 | MNad07 | AbN4 | 27 | unclear |
| 812385 | MNad07 | AbN4 | 23 | unclear |
| 903679 | MNad67 | AbNT | 21 | unclear |
| 801158 | MNad64 | AbNT | 16 | gaba |
| 800248 | MNad07 | AbN4 | 14 | unclear |
| 800478 | MNad68 | AbNT | 14 | unclear |
| 814989 | MNad03 | AbN4 | 14 | unclear |
| 815075 | MNad17 | AbNT | 12 | acetylcholine |
| 908158 | MNad17 | AbNT | 12 | acetylcholine |
| 805980 | MNad07 | AbN4 | 11 | unclear |
| 802201 | MNad68 | AbNT | 10 | unclear |
| 806689 | MNad09 | AbNT | 10 | unclear |
| 810069 | MNad09 | AbNT | 10 | unclear |
| 812718 | MNad07 | AbN4 | 10 | unclear |

## Hop-2 from hop-1 partners

Weight is synapse count from hop-1 posts. FOUR are excluded as presynaptic so hop-1 is not counted twice. `logs/hop2.json`

| pool | n | weight | fraction |
|------|--:|-------:|---------:|
| total | 11,675 | 850,051 | 1 |
| local AG INs (A7-A9 vnc_intrinsic) |  | 191,411 | 0.2252 |
| exiting effectors |  | 247,903 | 0.2916 |
| AbNT efferents + motor | 104 | 154,333 | 0.1816 |

Hop-2 EN00B* top 12:

| bodyId | type | hop2 | consensus NT |
|-------:|------|-----:|--------------|
| 903484 | EN00B003 | 5,744 | octopamine |
| 802372 | EN00B018 | 2,293 | octopamine |
| 808163 | EN00B010 | 1,854 | octopamine |
| 817838 | EN00B013 | 1,755 | octopamine |
| 803005 | EN00B004 | 1,718 | octopamine |
| 907835 | EN00B010 | 1,678 | octopamine |
| 808353 | EN00B013 | 1,662 | octopamine |
| 803015 | EN00B020 | 1,656 | octopamine |
| 808856 | EN00B004 | 1,650 | octopamine |
| 811414 | EN00B016 | 1,649 | octopamine |
| 800615 | EN00B013 | 1,637 | octopamine |
| 810453 | EN00B016 | 1,595 | octopamine |

Hop-2 unlabeled AbNT efferents: same 13 bodies, 1,260 to 2,201 synapses, consensus unclear.

Hop-2 MNad* top: MNad68 802201 (5,462), MNad68 800478 (5,327), MNad66 802114 (5,168).

## Toy LIF

`src/fly_climax/lif_toy.py`, lock `logs/lif_toy.json`. Four command cells clamped at 100 Hz for 3 s. One-synapse hop onto the top 20 hop-1 partners excluding FOUR. 0.01 mV per contact is a grid pick because 0.005 left AbNT silent, not a fly biophysics constant. AbNT effector mean 26.974 Hz does not cross invented threshold 40 Hz. The ejaculation threshold is invented and is not biology. Change the threshold, the millivolts-per-contact, or the 100 Hz clamp and that sentence flips. Useful only as a check that the graph is wired toward AbNT cells.

## 5-HT accessory-gland step

Missing. Consensus serotonin is 48 bodies in MaleCNS v1.0, 0 on AbNT, 0 on `vnc_efferent` or `vnc_motor`. Predicted-serotonin AbNT body 806679 (MNad12) has hop-1 weight 0 from FOUR and consensus NT unclear (pred conf 0.520).

## Reproduce

```bash
/opt/homebrew/bin/python3.12 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m pytest
.venv/bin/python -m fly_climax tables
.venv/bin/python -m fly_climax lif
```

Optional rebuild from Janelia feathers (pandas, pyarrow):

```bash
.venv/bin/python -m pip install -e ".[malecns]"
.venv/bin/python scripts/rebuild_from_feathers.py --ann ANN --nt NT --weights WEIGHTS --out logs
.venv/bin/python -m fly_climax lif
```

## Files

| path | role |
|------|------|
| `logs/drive_summary.json` | hop-1/hop-2 totals |
| `logs/hop1.json` | ranked EN00B*, unlabeled AbNT, MNad*, OGN/SGN |
| `logs/hop2.json` | hop-2 ranked tables |
| `logs/hop1_top20.json` | LIF partners |
| `logs/lif_toy.json` | toy pulse lock |
| `logs/working_set.json` | FOUR plus sensitivity |
| `logs/unlabeled_abnt.json` | 13 unlabeled AbNT plus EN00B010 Maggio/Chaverra map |
| `src/fly_climax/lif_toy.py` | LIF |
| `data-provenance/malecns_v1/source.lock.json` | GCS sha256 |
| `AGENTS.md` | claim bans, no GraphForge |
| `THIRD_PARTY.md` | MaleCNS CC BY 4.0 |

[Fly research index](https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178)
