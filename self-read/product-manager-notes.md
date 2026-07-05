# Ground Rules for Modern AI Product Managers

## 1. Start from the problem, not the model
- Don't reach for AI because it's available — reach for it because it's the best way to solve a real user problem.
- Be able to articulate what a *non-AI* solution would look like, and why AI is worth the added complexity, cost, and unpredictability.
- Beware "solution in search of a problem" — a flashy demo is not a product.

## 2. Get comfortable with probabilistic systems
- Traditional software is deterministic: same input, same output. AI systems are probabilistic — the same input can produce different outputs.
- Design the product experience assuming the model **will** be wrong sometimes. Ask: what happens on a bad answer? Is the failure mode annoying, costly, or dangerous?
- Define acceptable error rates per use case. A wrong movie recommendation is low-stakes; a wrong medical or financial suggestion is not.

## 3. Own the evaluation strategy
- "It feels good in the demo" is not an evaluation strategy. Build a real eval set (golden examples, adversarial cases, edge cases) before launch.
- Track quality metrics continuously in production, not just at launch — model behavior drifts as usage patterns shift and as underlying models are updated.
- Distinguish between offline evals (benchmarks, regression tests) and online signals (user feedback, thumbs up/down, task completion, retries).

## 4. Design for human oversight, not just automation
- Decide deliberately where the human stays in the loop, on the loop, or out of the loop — this is a product decision, not just an engineering one.
- For high-stakes actions (sending money, deleting data, contacting a customer), default to confirmation steps until trust is earned.
- Make it easy for users to see *why* the AI did something, and to correct or override it.

## 5. Treat prompts and context as product surface area
- Prompts, system instructions, and retrieved context are effectively part of your product's logic — version them, test them, and review changes to them like you would code.
- A "small prompt tweak" can silently change behavior across the whole product. Don't let this happen outside of a review process.

## 6. Understand the cost and latency tradeoffs
- Every AI feature has a marginal cost per request (tokens, compute) — know your unit economics before scaling a feature broadly.
- Latency matters: users tolerate different wait times for chat vs. background processing vs. real-time interactions. Design UX (streaming, progress indicators) around this rather than pretending latency doesn't exist.
- Bigger/smarter models aren't always the right call — know when a smaller, cheaper, faster model is "good enough."

## 7. Plan for model and vendor change
- Models get updated, deprecated, or replaced. Don't hard-couple your product's behavior to quirks of one specific model version.
- Abstract the model layer where practical so you can swap providers/models without a full rewrite.
- Re-run your eval suite whenever the underlying model changes — a silent upgrade can silently break your product.

## 8. Take data privacy and security seriously
- Know exactly what user data is sent to which model/provider, and whether it's used for further training. Get this in writing from vendors.
- Apply the same data classification and access-control rigor to AI pipelines as to any other system handling sensitive data.
- Be able to answer: "What happens if this conversation/data leaks?" before launch, not after.

## 9. Set honest expectations with users
- Don't market AI features as more capable or more certain than they are. Overpromising erodes trust faster than an occasional visible mistake.
- Clearly disclose when a user is interacting with AI-generated content or an AI agent, especially where decisions affect them materially.
- Give users an easy path to report bad outputs — and actually close the loop by using that feedback to improve the system.

## 10. Measure real outcomes, not vanity AI metrics
- "We shipped an AI feature" and "we used a bigger model" are not outcomes. Task success rate, time saved, reduction in support tickets, retention — these are outcomes.
- Watch for Goodhart's Law: once a proxy metric (e.g., response length, engagement) becomes the target, it stops being a good measure of quality.
- Run controlled experiments (A/B tests) where possible — AI features can look impressive anecdotally while not moving the metrics that matter.

## 11. Build a fast feedback and iteration loop
- AI product quality is rarely "done" at launch — plan for continuous tuning of prompts, retrieval, guardrails, and models based on real usage.
- Instrument everything: inputs, outputs, user actions after the AI response, and explicit feedback signals.
- Make it cheap and fast to ship prompt/config changes separately from full app releases, so iteration doesn't require a full deploy cycle.

## 12. Understand guardrails aren't optional
- Define what the system must never do (leak PII, give unlicensed legal/medical/financial advice, generate harmful content) and enforce it with actual guardrails — not just a line in the system prompt.
- Red-team your own product before launch: try to break it, jailbreak it, and misuse it the way real users eventually will.
- Have an incident response plan specifically for AI failures (a bad viral output, a hallucinated claim, a leaked prompt) — these move faster and more publicly than typical bugs.

---

*Living document — update as practices mature and new lessons are learned.*
