# Implementation delta audit: GH-F9, GH-F10, GH-F11

Audited commit: `89cb041f901b51a3f90fa6831aab1b4553c1772c`. All work was
performed outside the audited tree, without tracked changes, commits or
remote writes. The disposable copies retain the unchanged repository tests.

## GH-F9: PARTIALLY_RESOLVED

All 19 rerun original invalid/nonfinite construction probes reject. The
four public records now have substantive finiteness and algebraic checks;
strict JSON serialization of factory outputs succeeds.

However, all five new replacements below are accepted and serialize as
strict JSON. They retain old computed values with changed scientific inputs
or directly false stored quantities:

| Replacement | Accepted stored value | Fresh calculation |
|---|---:|---:|
| `ConditionalGlobalLinearSigma.early_spectrum`, A_s times 4 | sigma 0.6493893103154803 | sigma 1.2987786206309606 |
| `ConditionalGlobalLinearSigma.radius`, valid resolved radius times 2 | sigma 0.6493893103154803 | sigma 0.40217828345358647 |
| `ConditionalGlobalLinearSigma.quadrature`, nodes 33/17 | relative change 6.037237376688154e-11 | factory refuses: change 9.387e-3 > 1e-6 |
| `EvaluatedVoidShare.closure`, seed radius times 2 | sigma_seed 0.0033975735001936717 | sigma_seed 0.0026377335114469718 |
| `AdmissibleGlobalLinearInterval.target_premise_rms` | 999 | unchanged correct value 0.06505162933276047 |

The first record's validation checks stored algebraic relations, not the
H10 integral from the spectrum/radius/nodes. The seed record does not store
enough input provenance to verify its seed sigma against a modified seed
radius. The interval's target premise rms is only required to be finite and
positive. The claim that every field is revalidated from the scientific
inputs is therefore too broad. Factory calculations remain correct.

Evidence: `probes_results.json`, `nodes_factory_check.json` and `probes.py`.

## GH-F10: RESOLVED in the tested numerical scope

The union of the original two probe files has 21 unique rho/c/n cases.
Twenty return accurate moments; the original start count 800 refuses
because the necessary node doubling would exceed the new 1024 cap. Maximum
analytic P11 error in the returned original cases is 5.184741525e-14 at
requested absolute tolerance 1e-12.

An independent QUADPACK grid has 99 cases, including unequal thresholds,
thresholds from -100 to +10 and correlations as close as 1-1e-12 to both
singular endpoints. All return; maximum absolute discrepancy is
6.661338148e-15. The reference integrates the conditional normal density
using adaptive panels and a separate normal-tail truncation of ±14, with
epsabs 2e-14 and epsrel 2e-13. This numerical audit does not establish a
universal rigorous error theorem.

Removing the ±8 conditional-transition edges returns about 3.136e-33 at
rho=-0.999999,c=0, versus analytic 0.0002250790977990913. The new repository
test kills this mutant. Removing refinement is also killed. Removing only
the centre split, with both transition edges retained, remains accurate on
all 99 independent cases and is a benign survivor over this tested grid.

Evidence: `supplementary_results.json`, `probes_results.json`,
`centre_split_mutant_grid.json` and mutation logs N5/N6/N7.

## GH-F11: RESOLVED as rounded-reference reproduction

The propagated input rounding budget plus output half-unit gives
0.0001137204081831 (GM) and 0.0001129441809951 (NW15), below 1.2e-4.
Observed absolute differences are 2.487558566e-5 and 2.307461453e-6. These
checks reproduce references quoted at four decimal places; they do not
certify full precision unrounded historical values.

The required removal of the output `+1` budget term survives the 35 focal
tests and full H evidence: the current reference discrepancies also fall
within the reduced budgets. The focal test calculates its own budget,
without calling the evidence script's budget calculation. A boundary test
would be needed to exercise that contribution.

## Mutation campaign and actual coverage

Baseline: 35 passed, warnings as errors. All eight original mutants are
killed, with M7 adapted to the new lower-limit expression. Fifteen further
mutants cover one control in each of the four public records, centre and
transition-edge splitting separately, refinement, Frechet bounds, the
void-share identity text and its executable PBS response counterpart,
reclosure amplitude, lognormal normalization, lambda squared, rounding and
step cutoff. Total: 23 mutants; 17 killed by unchanged focal tests or H
evidence, six survivors.

The six survivors are N1 (growth background consistency), N4 (interval
target-inside flag), N5 (centre split), N8 (Frechet gate), N9 (docstring
identity sign), N13 (output half-unit). Added independent audit probes
distinguish N1, N4 and N8 by constructing the exact invalid state each
deleted check would otherwise refuse; baseline refuses all of them. This
does not turn those probes into coverage of the unchanged repository suite.

Script mutants N10-N14 each also ran the full H evidence with no figures:

| Mutant | Repository tests | H evidence |
|---|---|---|
| Reclosure factor unsquared | 35 pass | Four constant-share reclosure gates fail, relative difference 1.504e-2 > 1e-10 |
| Lognormal normalization off | MC kernel test fails | PSD contract refuses min eigenvalue -3.314e-2 |
| Lognormal lambda squared replaced by lambda | MC kernel test fails | Both linear-limit gates fail |
| Output rounding half-unit removed | 35 pass | All gates pass |
| Cutoff multiplied by 0.9 | Counterexample test fails | Both premise gates fail, ratios 1.020 / 1.247 > 1 |

The literal identity p=f_v-df_v,L/d(delta_L) appears in docstrings and
independent tests but has no exported executable derivative helper. N9
therefore changes documentation only; N9b reverses the executable PBS
threshold response, which is killed. No full-suite mutation claim is made:
the campaign reruns the 35 H tests and, for N10-N14, H evidence. Main/full
suite validation is the parent audit's separate responsibility.

Machine-readable index: `implementation_summary.json`,
`mutation_results.json`, `defensive_results.json`. Reproduction scripts:
`mutations.py`, `probes.py`, `supplementary.py`, `defensive_probes.py`.
