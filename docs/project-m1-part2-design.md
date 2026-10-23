
# Module 1 Checkpoint 2: AI Front Desk Design

## Business

**Business name:** Sweet Crumbs Bakery

**Purpose:** Answer common customer questions, calculate accurate order quotes, route unanswered questions to an AI model, and report customer activity.

## 1. Intent Design

| Intent | Keywords | Reply |
|---|---|---|
| Complaint | `refund`, `complaint`, `late` | Sorry about that. A manager will call you within 1 hour. |
| Greeting | `hi`, `hello`, `hey` | Hello! How can I help you today? |
| Hours | `hours`, `timings`, `open`, `close` | We are open 9 am to 10 pm, every day. |
| Location | `location`, `where` | We are located in Lahore. Please contact us for the exact address. |
| Delivery | `delivery`, `deliver`, `shipping` | Delivery costs 200 PKR. It is free for orders of 3,000 PKR or more after discount. |
| Prices and menu | `fee`, `fees`, `price`, `prices`, `menu` | Cupcakes are 250 PKR, brownies are 300 PKR, and chocolate cakes are 1,500 PKR. |
| Human handover | `agent`, `human` | Connecting you to a human... |
| AI fallback | No matching rule | Prepare a prompt and route the question to a local or cloud model. |

## 2. Business Rules

| Rule | Value |
|---|---|
| Cupcake price | 250 PKR each |
| Brownie price | 300 PKR each |
| Chocolate cake price | 1,500 PKR each |
| Bulk discount | 10% off when quantity is 10 or more |
| Delivery fee | 200 PKR |
| Free delivery limit | 3,000 PKR after discount |
| Private keywords | `phone`, `cnic`, `address` |
| Local model | llama3.2 (local, private) |
| Local model estimated cost | 0 PKR |
| Cloud model | Small cloud model (cheap) |
| Example cloud price | 0.1 PKR per 1,000 tokens |
| Token estimate | Approximately 1 token per 4 characters |
| Maximum question length | 150 characters |

## 3. Rule Test Results

Run each test and update the Pass? column honestly based on the actual output.

| You type / action | Expected result | Pass? |
|---|---|---|
| ` WHAT are your hours ` | Hours reply; spaces and capitals handled | Pass |
| `which cake is best?` | AI fallback, not a greeting | Pass |
| `my order is late` | Manager reply; complaint counted | Pass |
| `/quote`, item `chocolate cake`, quantity `1` | 1,500 PKR subtotal and 200 PKR delivery | Pass |
| `/quote`, item `chocolate cake`, quantity `2` | 3,000 PKR subtotal and free delivery | Pass |
| `/quote`, item `cupcake`, quantity `10` | 10% discount applied | Pass |
| `/quote`, item `pizza`, quantity `2` | Not-on-menu reply; no crash | Pass |
| `can I change my phone number?` | Routed to local model; 0 PKR AI cost | Pass |
| `my address is incorrect` | Routed to local model; 0 PKR AI cost | Pass |
| Press Enter without text | Asks for a message again | Pass |
| `BYE` | Goodbye message and session report | Pass |
| Enter `letters` for quantity | Polite validation message; no crash | Pass |
| `human` or `agent` | Human handover message and session report | Pass |

## 4. Rule Order Explanation

1. **Complaint handling comes first** so unhappy customers receive priority.
2. Human handover is checked before normal FAQs and AI fallback.
3. `bye` exits the conversation using `break`.
4. Empty messages are rejected before incrementing the message counter.
5. `/quote` is processed before FAQ rules so the price calculator runs correctly.
6. Greeting checks use equality or `startswith()` rather than checking whether `hi` appears anywhere in a message.
7. FAQs handle common questions without AI costs.
8. Only unmatched questions reach the AI fallback.
9. Private questions containing `phone`, `cnic`, or `address` use the local model with an estimated cost of zero.
10. Other unmatched questions use the example cloud price to estimate AI costs.

## 5. Price Calculation Example

For 12 cupcakes:

- Subtotal: 12 × 250 = 3,000 PKR
- Discount: 10% × 3,000 = 300 PKR
- Discounted subtotal: 3,000 − 300 = 2,700 PKR
- Delivery: 200 PKR because 2,700 is below the free-delivery limit
- Final total: 2,700 + 200 = 2,900 PKR

For two chocolate cakes:

- Subtotal: 2 × 1,500 = 3,000 PKR
- Discount: 0 PKR
- Delivery: 0 PKR because the subtotal reaches the free-delivery limit
- Final total: 3,000 PKR