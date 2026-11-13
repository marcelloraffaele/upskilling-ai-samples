# Example Prompts for a RAG Demo - Contoso Electronics / Northwind Health

## Demo objective

These prompts are designed to demonstrate how a RAG agent can:

- retrieve specific information from a knowledge base;
- combine information from multiple documents;
- compare plans and policies;
- produce structured answers with source citations;
- handle ambiguous questions or information not covered by the documents;
- maintain context across follow-up questions.

> Note: the documents state that their content is synthetic and generated for demonstration purposes. It does not represent actual insurance plans or company policies.

## Knowledge base documents

- `Benefit_Options.pdf`: overview and comparison of Northwind Health Plus and Northwind Standard.
- `Northwind_Standard_Benefits_Details.pdf`: details, costs, and coverage of the Northwind Standard plan.
- `Northwind_Health_Plus_Benefits_Details.pdf`: details, costs, and coverage of the Northwind Health Plus plan.
- `employee_handbook.pdf`: Contoso Electronics' mission, values, performance reviews, workplace safety, privacy, whistleblowing, data security, and job roles.

---

# 1. Introductory prompts

Use these prompts to begin the demo with straightforward questions whose answers are easy to verify.

### Prompt 1 - Plan overview

```text
Which health plans are available to Contoso Electronics employees? For each plan, summarize the main coverage in no more than five bullet points and cite the document used.
```

**Information the agent should retrieve:**

- Northwind Health Plus and Northwind Standard;
- medical, dental, and vision coverage;
- general differences involving emergency care, mental health, prescription drugs, and out-of-network services.

### Prompt 2 - Employee-friendly summary

```text
I am a new Contoso Electronics employee. Give me a short, easy-to-understand introduction to the available health benefits and tell me where I can find more details.
```

### Prompt 3 - Tabular response

```text
Create a comparison table for Northwind Health Plus and Northwind Standard with these columns: medical services, preventive care, prescription drugs, emergency care, mental health, out-of-network care, vision, and dental. Cite the source for every statement.
```

---

# 2. Prompts that demonstrate precise retrieval

### Prompt 4 - Standard plan costs

```text
What are the annual individual deductible, primary care copay, specialist copay, coinsurance rate, and annual out-of-pocket maximum for Northwind Standard? Provide a list and cite the source for each value.
```

**Verifiable knowledge base details:**

- $2,000 annual individual deductible;
- $30 primary care copay;
- $50 specialist copay;
- 20% coinsurance after the deductible has been met;
- $6,000 annual individual out-of-pocket maximum.

### Prompt 5 - Office visit costs under the Plus plan

```text
Under Northwind Health Plus, how much can a primary care visit, specialist visit, and mental health visit cost? Distinguish between the general indicative amounts and the amounts stated in the split copay section. Clearly identify any differences between the sections.
```

**Why it is useful in the demo:** it shows that a RAG system must retrieve multiple passages from the same document, identify potential discrepancies, and disclose them rather than hide them.

### Prompt 6 - Preventive care

```text
Which preventive care services are mentioned in the documents, and what do the documents say about their costs? Do not add services that are not present in the sources.
```

### Prompt 7 - Prescription drugs

```text
Compare prescription drug coverage under the two plans. Specify which drug categories are explicitly mentioned and which limitations can be identified from the documents.
```

---

# 3. Comparison and multi-document reasoning prompts

### Prompt 8 - Which plan covers a specific need?

```text
An employee wants coverage that includes mental health, substance abuse treatment, emergency services, and the ability to use out-of-network providers. Which plan better meets these requirements? Explain the answer by comparing the documents and cite the sources.
```

### Prompt 9 - Vision and dental

```text
Compare the vision and dental coverage of Northwind Health Plus and Northwind Standard in detail. If a detail is unavailable or inconsistent across the documents, state that explicitly.
```

### Prompt 10 - Decision scenario

```text
Compare the two plans for someone who expects frequent specialist visits and wants to limit the risk of unexpected expenses. Use only the data in the documents, separate facts from considerations, and do not provide medical or financial advice.
```

### Prompt 11 - Benefits and limitations matrix

```text
For each plan, create a matrix containing: main benefits, main limitations, excluded or unspecified services, and items to verify before enrollment. Associate every point with its source document.
```

---

# 4. Prompts combining the employee handbook and benefit documents

### Prompt 12 - New employee guide

```text
Create an onboarding checklist for a new Contoso Electronics employee. Include company values, performance reviews, workplace safety, privacy and data security, and an overview of the health plans. Group the information by document and cite the sources.
```

### Prompt 13 - Performance reviews

```text
How does the performance review process work at Contoso Electronics? Describe its frequency, purpose, possible participants, and resulting documentation, using only the employee handbook.
```

### Prompt 14 - Company values

```text
What are Contoso Electronics' company values? Present them as a concise list and explain in one sentence how each value could translate into an employee's daily behavior. Clearly distinguish document content from your interpretation.
```

### Prompt 15 - Workplace safety and violence prevention

```text
Summarize the employee handbook rules concerning workplace safety and violence prevention. Include what an employee should do if they believe they are in danger or witness an incident.
```

### Prompt 16 - Privacy and personal information

```text
Which principles and safeguards does Contoso Electronics describe for collecting, using, accessing, and protecting personal information? Return the answer as a compliance checklist and cite the relevant employee handbook sections.
```

### Prompt 17 - Data security

```text
Extract all operational data security rules from the employee handbook. Organize them under these categories: access, encryption, passwords, antivirus, backups, data destruction, training, and audits.
```

### Prompt 18 - Whistleblowing

```text
Explain Contoso Electronics' whistleblower policy: what can be reported, how a report should be handled, and which protections are provided. If the document does not specify a channel or detail, say so without inventing it.
```

---

# 5. Prompts involving calculations grounded in retrieved data

### Prompt 19 - Coinsurance example

```text
Using the Northwind Standard plan data, assume a covered service has an allowed cost of $1,000 after the deductible has been met. Calculate how much the employee would pay by applying only the coinsurance stated in the document. Show the formula, calculation, and source of the rate used.
```

**Expected result:** 20% of $1,000, or $200, excluding any copays or other conditions not specified in the scenario.

### Prompt 20 - Progress toward the out-of-pocket maximum

```text
An employee enrolled in Northwind Standard has already incurred $5,500 in expenses that count toward the individual out-of-pocket maximum. Based on the plan's stated limit, how many dollars remain before the limit is reached? Explain the limitations of the calculation and cite the source.
```

**Expected result:** $500, assuming that all stated expenses are eligible to count toward the limit.

### Prompt 21 - Deductible, copay, coinsurance, and out-of-pocket maximum

```text
Explain the difference between a deductible, copay, coinsurance, and out-of-pocket maximum, using the amounts from Northwind Standard as concrete examples. Cite the source of each amount.
```

---

# 6. Conversational prompts demonstrating context retention

Use the following prompts in sequence, without repeating the plan name in every question.

### Conversation A - Progressive exploration

```text
What are the main differences between Northwind Health Plus and Northwind Standard?
```

```text
Which one includes mental health coverage?
```

```text
What about out-of-network emergency care?
```

```text
Now summarize only the differences we discussed in a table with sources.
```

### Conversation B - From overview to detail

```text
Give me a concise description of Northwind Standard.
```

```text
What is its individual deductible?
```

```text
After I meet it, what percentage do I pay as coinsurance?
```

```text
Give me an example for an $800 service.
```

### Conversation C - Employee handbook

```text
What main topics are covered by the employee handbook?
```

```text
Focus only on data security.
```

```text
Turn those rules into a checklist for a new employee.
```

---

# 7. Prompts that test citations and grounding

### Prompt 22 - Mandatory citations

```text
Answer the question using only the knowledge base. After every relevant statement, provide the document name and the section from which the information was retrieved. Question: which services primarily distinguish Northwind Health Plus from Northwind Standard?
```

### Prompt 23 - Supporting evidence

```text
Find the evidence supporting the statement: "Northwind Health Plus is more comprehensive than Northwind Standard." Return a table with the claim, summarized evidence, document, and section. Do not use external knowledge.
```

### Prompt 24 - Auditable answer

```text
Prepare an auditable answer about emergency coverage under both plans. Separate confirmed facts, possible ambiguities, and unavailable information. Always cite the source.
```

### Prompt 25 - Conflicts between sources

```text
Check whether the documents contain potentially inconsistent values, descriptions, or coverage details between the plan overview and the detailed plan documents. List the discrepancies without attempting to resolve them, and cite both relevant passages.
```

---

# 8. Prompts demonstrating safe behavior when an answer is unavailable

Use these prompts to verify that the agent does not invent information.

### Prompt 26 - Exact information unavailable

```text
What exact monthly premium will I pay for Northwind Health Plus?
```

**Expected behavior:** the agent should explain that the cost depends on factors such as the plan type, services, and providers, or that an exact amount is not available in the documents.

### Prompt 27 - Missing personal data

```text
Which health plan did Mario Rossi select, and how many reimbursement claims has he submitted this year?
```

**Expected behavior:** do not invent an answer. The documents do not contain this personal information.

### Prompt 28 - Undocumented policy

```text
How many remote-working days per week are Contoso Electronics employees allowed?
```

**Expected behavior:** state that the policy is not included in the available knowledge base.

### Prompt 29 - Question outside the knowledge base

```text
What is the current share price of Contoso Electronics?
```

**Expected behavior:** explain that the knowledge base does not contain current financial information and do not infer an answer.

### Prompt 30 - Anti-hallucination instruction

```text
Search only the available documents. If you cannot find explicit information, answer "Information not available in the knowledge base" and identify the documents you checked. Question: what is the HR office telephone number?
```

---

# 9. Advanced prompts for a technical RAG demonstration

### Prompt 31 - Query decomposition

```text
Break the request into subquestions and search the appropriate documents: a new employee wants to understand both the data security rules and which health plan covers mental health and emergency services. Produce a single response, but identify the source for each section.
```

### Prompt 32 - JSON output

```text
Extract the main characteristics of both plans as valid JSON using this structure: planName, medical, vision, dental, preventiveCare, prescriptionDrugs, mentalHealth, emergencyServices, outOfNetwork, deductible, copays, coinsurance, outOfPocketMaximum, sources. Use null when a value is unavailable and do not invent data.
```

### Prompt 33 - Role-based answer

```text
Act as a Contoso Electronics HR assistant. Answer an employee who asks which plan includes mental health coverage and out-of-network emergency care. Use a clear, neutral tone, cite the sources, and remind the employee that the final decision should be verified against the plan documents.
```

### Prompt 34 - FAQ generation

```text
Generate 12 FAQs for the Contoso Electronics HR portal using these documents. Include questions about plan selection, costs, emergency care, mental health, preventive care, data security, and whistleblowing. Cite the source for every answer and do not add external information.
```

### Prompt 35 - Retrieval quality assessment

```text
Answer the question and then show which knowledge base passages were used, why they are relevant, and whether other potentially relevant but conflicting passages exist. Question: what is the cost of a specialist visit under each plan?
```

---

# 10. Suggested sequence for a 10-minute demo

1. **Simple question:** Prompt 1, to demonstrate retrieval of a general overview.
2. **Precise fact:** Prompt 4, to demonstrate extraction of exact values.
3. **Multi-document comparison:** Prompt 8, to demonstrate retrieval and synthesis.
4. **Contextual follow-up:** use Conversation A.
5. **Grounded calculation:** Prompt 19.
6. **Citations and conflicts:** Prompt 25.
7. **Unavailable answer:** Prompt 28 or Prompt 30, to demonstrate hallucination control.

## Suggested system instruction for the demo agent

```text
Answer exclusively with information retrieved from the knowledge base. Always cite the document and, when available, the relevant section. If the sources are incomplete, ambiguous, or conflicting, state this explicitly. Do not invent values, coverage details, policies, or personal data. Clearly distinguish facts found in the documents from calculations, inferences, and suggestions derived from those facts.
```
