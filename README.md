# Sliding Mode Control in Robotics: A Fifty-Year Review and Tutorial Since Utkin — data and code

Companion repository of the review article by Claudio Urrea (Department of Electrical Engineering, Faculty of Engineering, University of Santiago of Chile, Las Sophoras 165, Estación Central, Santiago 9170020, Chile), submitted to *Mathematics* (MDPI).

## Contents
| Folder | Content |
|---|---|
| `data/` | Table S1 (synthesis set, 311 works), Table S2 (flow of records), Table S3 (excluded records with reasons, 6464), Table S4 (mapping corpus 2016–2026, 5931 works, and pre-2016 canon, 79 works), File S1 (search strategies), File S2 (PRISMA 2020 checklists) |
| `protocol/` | Review protocol with dated amendments (in Spanish, as written before screening) |
| `code/rs2/` | Record merging and deduplication, rule-based screening, citation chasing, canon checks and recall estimate |
| `code/rs3/` | Text normalization, screening/eligibility rules, coding and blind-coding agreement (Cohen's kappa) |
| `code/rs4/` | Trends, co-occurrence, validation models (logistic regression), robustness tests |
| `code/rs5/` | Figures (Palatino-type font, true minus sign) and consistency checks of the manuscript |
| `code/rs6/` | Claim-by-claim audit: checks of the numbers corrected in the audit against the coded corpus |
| `tutorial/` | Two-link arm tutorial: 4 controllers × 3 sampling periods × 2 noise levels (108 runs), results and table |
| `figures/` | Figures of the article (PDF) |

## Reproducing the tutorial
```
pip install -r requirements.txt
python tutorial/smc_tutorial.py          # writes tutorial_raw.json (deterministic seeds)
python tutorial/tutorial_tabla_fig.py     # Table 4 values and Figure 9
```
Pure Python for the simulation (no external solver). Runtime: about 10 s on 2 cores.

## Reproducing the corpus statistics
```
python code/reproduce_from_S4.py data/Table_S4.csv [Manuscript.tex]
```
With the LaTeX source of the article as second argument, every printed value is also checked against the text. Regenerates from Table S4 alone the corpus figures reported in the article (corpus size, shares, validation rates, Wilson intervals, adjusted odds ratios, strict core, platform counts, chattering techniques, code mentions). Indicators obtained by keyword search of abstracts (Figure 6 and the discretization indicator) need the abstracts, which cannot be redistributed; the identifiers and DOIs of Table S4 allow the records to be retrieved.

## Notes
- Coding was done on titles, author keywords and abstracts; see Section 2 of the article.
- The raw Web of Science and Scopus exports are not redistributed because of database license terms. Tables S1, S3 and S4 give identifiers and DOIs to retrieve every record.
- `code/rs2`–`code/rs6` document the full pipeline. They read the raw exports and intermediate files from a working folder (`./work` at the top of each script), which is not included.

## Licenses
Code: MIT (`LICENSE`). Data and figures: CC BY 4.0 (`LICENSE-DATA.md`).

## Citation
See `CITATION.cff`. Data and code DOI: https://doi.org/10.6084/m9.figshare.34989193. Repository: https://github.com/ClaudioUrrea/smc-robotics-review.
