
[success_criteria.md](https://github.com/user-attachments/files/26161832/success_criteria.md)
# Project Success Criteria

**Project:** Structural Vibration Monitoring System  
**Author:** Rafe Farrant — MEng General Engineering, University of York  
**Defined:** Day 1 | **Evaluated:** Day 53

---

## Pass/Fail Criteria

| Criterion | Target | How to Measure | Pass/Fail (Day 53) |
|---|---|---|---|
| Frequency detection accuracy | ±5% of theoretical value | `% error = |f_exp − f_theory| / f_theory × 100` | |
| Measurement repeatability | Std dev < 0.5 Hz across 5 runs | Standard deviation of 5 repeated baseline measurements | |
| Structural change detection | Detect both Change A (mass addition) and Change B (loosened clamp) | Frequency shift > 3× std dev threshold for both changes | |
| Detection sensitivity | Detect shift ≥ 5% with no false positives | Test detection rule against both damaged and baseline datasets | |
| Damping ratio estimation | Extract ζ for baseline and both damaged conditions | `scipy.optimize.curve_fit` R² > 0.90 | |
| Code quality | Modular structure, all functions documented | 4 separate modules, docstrings on all functions | |
| GitHub README | Readable by a non-specialist in 60 seconds | Ask someone outside engineering to read the first two sections | |

---

## Notes

- These criteria were defined on Day 1, before any data was collected.
- A project that tests a hypothesis and reports pass/fail is significantly stronger than one that just reports results.
- Fill in the Pass/Fail column on Day 53 — this becomes the basis of your LinkedIn post and CV bullet.
