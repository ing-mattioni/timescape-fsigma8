# AGENTS.md — permanent rules for the timescape-fsigma8 project

These rules apply to every agent and every phase of this project. They are
not phase-specific and must not be weakened without explicit human approval.

1. **Scientific equations must never be changed without an explicit equation
   reference and human approval.**

2. **Every implemented equation must cite its paper equation number** (e.g.
   "Eq. (4.27) of arXiv:2511.17160") in a docstring or adjacent comment.

3. **Distinguish numerical refactoring from scientific-model changes.**
   Refactoring (vectorisation, caching, restructuring) must be demonstrably
   equivalent; model changes require human approval and a paper reference.

4. **Never silently change units, normalisations, initial conditions,
   independent variables, or sign conventions.** Any such change must be
   explicit, documented, and approved.

5. **New scientific code requires tests** for dimensions, limiting cases,
   normalisation, and published reference values.

6. **Upstream notebook code is reference-only until licensing is clarified.**
   The upstream repository (see UPSTREAM.lock) has no license file. Do not
   copy its source into files intended for publication or redistribution.

7. **Do not publish or push without explicit human approval.** No remote
   changes of any kind (push, fork, PR, issue, release).

8. **Prefer pure functions and typed Python modules** for the future
   independent implementation.

9. **Record numerical tolerances explicitly.** Never rely on library
   defaults without documenting that the default is being used and why.

10. **Do not suppress warnings unless their cause has been documented.**
