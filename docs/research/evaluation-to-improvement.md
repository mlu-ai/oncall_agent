# Turning evaluations into AI improvement loops

Evaluations become **training signals** when they identify which candidate response or trajectory is better, why it failed, or whether it passed a check.[14][3]

They remain **release evidence** when they are kept independent of model selection and training.[16] A useful programme uses both roles; optimizing only the measured score is not evidence of broad capability, truthfulness, robustness, or safety.[11][16]

## Practical taxonomy

- **Human preferences → RLHF.** Fine-tune on demonstrations, fit a reward model to comparisons, then optimize it with RL (commonly PPO).[1][14] This is suitable when quality is subjective or multi-dimensional, but the reward score must not replace held-out human evaluation.[11]
- **Chosen/rejected pairs → DPO.** DPO reformulates a KL-constrained RLHF objective as a classification loss, avoiding a separately fitted reward model and online RL.[2] It is simpler when comparison data already exist, while inheriting their coverage, bias, and ambiguity.[2]
- **Deterministic outcome checks → RL with verifiable rewards.** Generate candidates, execute/check them, and use pass/fail or a graded score for rejection sampling, RL, or best-of-*N* selection.[13] This is strongest for tests, compilers, formal proof checkers, simulators, and exact answers; a passing final answer need not diagnose an invalid intermediate step.[5]
- **Learned outcome verifier → search and later training.** Train a verifier to rank complete candidates, use it for search/reranking, then feed scored candidates into SFT, preference data, or RL.[4] Verifier errors can be amplified by selection and optimization, so a verifier-only serving system is not yet a learning loop.[11]
- **Step labels → process reward model (PRM).** Train a PRM to score intermediate steps, guide search or reward trajectories with it, and label uncertain cases preferentially.[3] This helps with long-horizon reasoning and diagnosis, but is task-specific, expensive, and does not prove faithful internal reasoning.[3][5]
- **Rule-guided model judgement → RLAIF / iterative DPO.** Sample, critique/revise, and have a model judge comparisons; train on the revisions or AI preferences.[10] It scales feedback beyond per-output human labels, but correlated generator/judge blind spots mean it is data generation, not independent validation.[11]
- **Production failure slices → iterative system improvement.** Log representative failures, add targeted scenarios and labels, retrain, and repeat with a refreshed policy or judge.[7][9] For an agent, score the complete trajectory—tool use, final state, cost/latency, and safety—not just its final text.[7]

## A conservative improvement flywheel

1. **Write an evaluation contract.** Define the user outcome, allowable actions, cost/latency budget, and safety constraints.[16] Preserve a frozen, hidden test set and an adversarial/OOD suite; version the public/trainable evaluation separately.[16]
2. **Turn only the trainable portion into feedback.** For each prompt or trajectory, sample diverse candidates and attach the strongest available signal: an executable check, human comparison, expert rubric, or calibrated judge.[14][16] Keep the raw artefacts, evaluator version, and provenance.[16]
3. **Choose the update by signal quality.** Use exact outcome rewards for RL/rejection sampling, preference data for DPO or reward-model RL, and step feedback for PRM-guided search/RL.[13] Start with a small, KL-regularized update and keep a reference policy.[2]
4. **Evaluate independently before expanding.** Compare against the frozen suite, new real-world failure slices, and counter-metrics such as refusal quality, calibration, tool-side effects, verbosity, cost, and latency.[9][16] Make promotion conditional on these gates, not on the training reward.[11]
5. **Refresh the evaluator deliberately.** Sample disagreements, low-confidence cases, and high-reward outliers for human/expert audit; fix the rubric/verifier and retrain only when that audit supports it.[11][16] Active learning improved PRM label efficiency in the reported math setting.[3]

## Anti-Goodhart rules

- Never tune, select checkpoints, or set prompts against the only score that determines release.[11] A learned reward is imperfect; both RL and best-of-*N* optimization can eventually reduce a more faithful (“gold”) reward even while the proxy rises.[11]
- Use **independent evaluators and data splits**: train reward model/judge on one pool, tune on another, and retain hidden human/expert, adversarial, and shifted-distribution tests for release.[16] This reduces correlated error; it does not establish a guarantee.[11][16]
- Audit reward-winning examples manually.[11] Look for shortcut features (formatting, verbosity, reference-answer leakage, tool-call theatre), bad side effects, and plausible-looking but invalid reasoning.[11] Outcome-only optimization can reduce legibility; prover–verifier training is one studied way to explicitly reward checkability.[12]
- Preserve diversity and a KL/reference constraint, cap optimization pressure, and stop or roll back when independent metrics regress.[1][11] KL penalties are a control knob, not a substitute for an external gold evaluation—one reward-overoptimization study found no measurable gold-score improvement from its KL penalty setting.[11]
- Do not call self-judging “self-validation.”[8] Constitutional AI and self-rewarding models show ways to generate scalable feedback, but the principles/judge remain part of the system being optimized and require outside audits.[10]

## Decision shortcut

- Use RL with a deterministic verifier when correctness is cheap to check and hard to produce.[13]
- Use PRMs when one bad intermediate action ruins a long trajectory and step labels can be obtained.[3]
- Use DPO/RLHF when the target is a human preference that cannot be reduced to a rule.[1][2]
- In all three cases, a separate, versioned evaluation gate should be allowed to reject a seemingly higher-reward model.[11][16]

DeepSeekMath introduced GRPO as a PPO variant for mathematical reasoning, illustrating one concrete policy-optimization implementation.[6] The OpenAI Evals repository documents evaluation contributions as an input considered for future-model improvements.[15]

## Sources

[1] https://arxiv.org/abs/2203.02155
[2] https://arxiv.org/abs/2305.18290
[3] https://arxiv.org/abs/2305.20050
[4] https://arxiv.org/abs/2110.14168
[5] https://arxiv.org/abs/2211.14275
[6] https://arxiv.org/abs/2402.03300
[7] https://arxiv.org/abs/2308.08998
[8] https://arxiv.org/abs/2401.10020
[9] https://arxiv.org/abs/2204.05862
[10] https://arxiv.org/abs/2212.08073
[11] https://proceedings.mlr.press/v202/gao23h.html
[12] https://openai.com/index/prover-verifier-games-improve-legibility
[13] https://arxiv.org/abs/2501.12948
[14] https://arxiv.org/abs/1706.03741
[15] https://github.com/openai/evals
[16] https://github.com/openai/evals/blob/main/docs/build-eval.md
