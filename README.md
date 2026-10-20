***Python-ai***

## Task 1.8: Business Helper Bot — Intent Design

**Business:** City Care Clinic

| Intent | What the user wants | Keywords to look for | Bot reply |
|---|---|---|---|
| Greeting | Say hello | `hi`, `hello`, `hey` | Hello! How can I help you today? |
| Timings | Know opening hours | `timings`, `hours`, `open`, `close` | We are open 10 am to 8 pm, Monday to Saturday. |
| Fees | Know the consultation fee | `fee`, `fees`, `price`, `cost` | Consultation fee is 2,000 PKR. |
| Location | Find the clinic | `location`, `address`, `where` | We are located in Lahore. Please contact us for the exact address. |
| Appointments | Book an appointment | `appointment`, `book`, `booking` | Please call the clinic to book an appointment. |
| Complaints | Report a problem | `complaint`, `late`, `problem`, `issue` | Sorry about that. The clinic manager will call you today. |
| Human handover | Speak to a person | `agent`, `human` | Connecting you to a human... |

**Fallback behavior:** If no intent matches, the bot counts the question as unanswered

**Exit behavior:** When the user types `bye`, the bot ends the conversation and displays the total message count, unanswered questions, and complaints received.