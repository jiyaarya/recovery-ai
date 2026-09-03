# Recovery AI 💸

## AI-Powered Payment Recovery & Revenue Intelligence Platform

Recovery AI is an AI-powered payment recovery platform designed to help businesses identify failed-payment revenue opportunities, estimate recovery probability, prioritize transactions, and recommend the most suitable recovery strategy.

Instead of treating every failed payment equally, Recovery AI uses transaction, customer, and payment-history signals to determine:

> **What is worth recovering, how likely it is to be recovered, how much revenue could potentially be recovered, and what action should be taken next.**

---

## 🚀 Live Demo

🌐 **Live Application:**

https://recovery-ai-jiya.streamlit.app/

💻 **GitHub Repository:**

https://github.com/jiyaarya/recovery-ai

---

## 🎯 Problem Statement

Failed payments represent more than individual transaction failures.

For businesses processing large volumes of payments, manually identifying which failed transactions deserve attention can be difficult, inefficient, and costly.

The key questions are:

- Which failed payments are worth recovering?
- How likely is each payment to be recovered?
- How much revenue could potentially be recovered?
- Which recovery strategy should be used?
- Should the recommended action actually be allowed?

Recovery AI addresses these questions through an ML-driven recovery workflow.

---

## 💡 Solution

Recovery AI converts raw payment failure data into actionable recovery intelligence.

The platform:

1. Identifies revenue at risk
2. Estimates recovery probability
3. Calculates expected recovery value
4. Assigns transaction priority
5. Recommends a recovery strategy
6. Applies safety guardrails
7. Provides an explanation for the recommendation
8. Allows recovery decisions to be exported for further use

### Core Principle

> **The model recommends. The guardrails decide what the model is allowed to do.**

This creates a separation between prediction and action, making the recovery workflow more controlled and safety-aware.

---

## ✨ Key Features

### 📊 Recovery Command Center

Provides a high-level view of the recovery opportunity, including:

- Revenue at Risk
- Expected Recovery
- Total Transactions
- High-Priority Transactions
- Recovery Probability Distribution
- Priority Distribution
- Strategy Distribution
- Expected Recovery by Strategy
- Top Recovery Opportunities

The dashboard provides a quick overview of where the highest-value recovery opportunities exist.

---

### 📁 CSV Dataset Analysis

Users can upload transaction datasets and analyze them directly through the application.

The uploaded dataset is validated before analysis and processed to generate recovery intelligence.

The system generates:

- Recovery Probability
- Expected Recovery
- Priority
- Recommended Strategy
- Final Action
- Risk Level
- Guardrail Reason

The complete analysis can also be exported as a CSV file.

---

### 🤖 ML-Based Recovery Prediction

Recovery AI uses transaction and customer signals to estimate the probability of recovering a failed payment.

Signals include:

- Transaction amount
- Payment method
- Failure reason
- Customer lifetime value
- Successful payments
- Failed payments
- Previous recovery rate
- Hour of transaction
- Days since last payment
- Subscription status
- Checkout abandonment
- Retry count

The trained ML model uses these signals to generate a transaction-level recovery probability.

---

### 🎯 Transaction Prioritization

Transactions are categorized based on recovery probability:

| Recovery Probability | Priority |
|---|---|
| ≥ 70% | HIGH |
| 40% – <70% | MEDIUM |
| <40% | LOW |

This allows recovery teams to focus their efforts on the most promising opportunities first.

---

### 🔄 Recovery Strategy Recommendation

The system recommends an appropriate recovery strategy based on transaction characteristics and predicted recovery potential.

Possible strategies include:

- **RETRY_PAYMENT** — retry the payment when recovery probability is high and retry limits have not been exceeded.
- **SEND_PAYMENT_LINK** — provide a payment link when checkout abandonment indicates that the customer may still complete the payment.
- **RETRY_LATER** — revisit the transaction when there is a reasonable recovery opportunity but immediate intervention is not required.
- **ESCALATE** — recommend manual intervention when automated recovery is not appropriate.
- **NO_ACTION** — avoid further recovery action when the transaction has already been recovered or the recovery opportunity is too weak.

---

### 🔍 Transaction Analysis

Users can analyze an individual transaction and receive:

- Recovery Probability
- Expected Recovery
- Priority
- Recommended Strategy
- Final Action
- Risk Level
- Strategy Explanation
- Guardrail Status
- Guardrail Reason
- Decision Summary

This makes the ML prediction easier to understand and act upon.

---

### 🛡️ Recovery Guardrails

Recovery recommendations pass through a guardrail layer before becoming actionable.

The guardrail system helps prevent inappropriate or excessive recovery actions.

The decision flow is:

**Prediction → Recommendation → Guardrail Check → Final Action**

Examples of guardrails include:

- Maximum retry threshold
- Low-probability blocking
- Already-recovered transaction protection
- Risk classification
- Escalation for unsafe cases

This ensures that a high ML probability does not automatically mean that an action should be executed.

---

### 💰 Revenue Intelligence

Recovery AI connects machine-learning predictions with business impact.

Instead of only asking:

> "Will this payment recover?"

the system also asks:

> "How much revenue could this recovery opportunity represent?"

Expected recovery is calculated using:

**Expected Recovery = Transaction Amount × Recovery Probability**

This allows the platform to prioritize opportunities based on both probability and monetary value.

---

### 📈 Recovery Analytics

The dashboard provides visual analytics to understand recovery opportunities.

#### Priority Distribution

Shows how transactions are distributed across:

- HIGH
- MEDIUM
- LOW

#### Strategy Distribution

Shows how recovery opportunities are distributed across recommended strategies.

#### Expected Recovery by Strategy

Shows the potential recoverable revenue associated with each strategy.

#### Recovery Probability Distribution

Shows how ML recovery probabilities are distributed across the analyzed transactions.

---

### 🔥 Top Recovery Opportunities

Recovery AI automatically identifies transactions with the highest expected recovery value.

The dashboard displays:

| Field | Description |
|---|---|
| Transaction ID | Unique payment identifier |
| Amount | Failed payment amount |
| Recovery Probability | ML-estimated recovery probability |
| Expected Recovery | Estimated recoverable value |
| Priority | Recovery priority |
| Strategy | Recommended recovery strategy |

This provides a practical view of which transactions should receive attention first.

---

### 📥 Export Recovery Decisions

After analyzing a dataset, users can download the recovery analysis as a CSV file.

The exported results include:

- Transaction ID
- Customer ID
- Amount
- Payment Method
- Failure Reason
- Recovery Probability
- Expected Recovery
- Priority
- Recommended Strategy
- Final Action
- Risk Level
- Action Allowed

This makes the recovery intelligence usable outside the dashboard.

---

## 🧪 Demo Dataset

The application can be demonstrated using a transaction dataset containing:

- **50 transactions**
- Approximately **₹14 lakh (₹0.14 crore) revenue at risk**
- Approximately **₹7 lakh (₹0.07 crore) expected recovery**
- **3 high-priority opportunities**
- Approximately **50.3% recoverable revenue**

These figures represent the provided demonstration dataset and are intended to illustrate the platform's recovery intelligence workflow.

---

## 🔎 Demo Transaction

A sample transaction can be used to demonstrate the Transaction Analysis workflow.

### Transaction ID

`TX-DEMO-001`

### Example Input

| Field | Value |
|---|---|
| Transaction ID | TX-DEMO-001 |
| Amount | ₹45,000 |
| Payment Method | card |
| Failure Reason | network_error |
| Customer Lifetime Value | ₹2,40,000 |
| Successful Payments | 28 |
| Failed Payments | 2 |
| Previous Recovery Rate | 78% |
| Hour of Day | 14 |
| Days Since Last Payment | 30 |
| Subscription Status | active |
| Checkout Abandoned | 0 |
| Retry Count | 0 |
| Already Recovered | 0 |

### Example Output

The current demonstration shows:

- **Recovery Probability:** 71.24%
- **Expected Recovery:** ₹32,058.15
- **Priority:** HIGH
- **Recommended Strategy:** RETRY_LATER
- **Final Action:** RETRY_LATER
- **Risk Level:** LOW

The transaction demonstrates how the system combines payment, customer, and historical recovery signals to produce a bounded recovery decision.

> Model outputs can vary depending on the dataset and model configuration.

---

## 🏗️ System Workflow

```text
Payment Failure Data
        ↓
CSV Upload / Transaction Input
        ↓
Data Validation
        ↓
Feature Processing
        ↓
ML Recovery Prediction
        ↓
Recovery Probability
        ↓
Expected Recovery Calculation
        ↓
Priority Classification
        ↓
Recovery Strategy Recommendation
        ↓
Guardrail Validation
        ↓
Final Recovery Decision