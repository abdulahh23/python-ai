
# Sweet Crumbs AI Content Studio — Design

## 1. Business facts

| Key | Value |
|---|---|
| name | Sweet Crumbs Bakery |
| business_type | Bakery |
| city | Lahore |
| hours | 9 AM to 10 PM |
| delivery | Available in Lahore |
| delivery_fee | 200 PKR |
| free_delivery | Free delivery on orders of 3,000 PKR or more |
| customers | Students, families, and dessert lovers |
| prices | See the product price table below |

### Product prices

| Product | Price |
|---|---:|
| Chocolate Cake | 1,500 PKR |
| Cupcake | 250 PKR |
| Brownie | 300 PKR |
| Mango Tart | 0 PKR (coming soon) |

## 2. Social media tones

| Tone | Description sent to the AI |
|---|---|
| fun | Playful and full of energy, using short and exciting sentences |
| premium | Elegant and calm, focused on quality and craftsmanship |
| urgent | Creates a sense of urgency and encourages customers to order today |

## 3. Model selection

| Job | Model and temperature | Why |
|---|---|---|
| Menu descriptions | Creative, 0.8 | Marketing descriptions should be varied and engaging |
| Social media posts | Creative, 0.8 | Posts need different writing styles and creative language |
| Customer chat | Precise, 0.2 | Customer answers should be consistent and grounded in business facts |
| Price questions | Python dictionary, no AI | Prices must be accurate and should not cost AI tokens |

Both models use the Ollama `gemma3:1b` model with different temperature settings.

## 4. Feature test results

| You type | Expected result | Pass? |
|---|---|---|
| `/menu` | Mango Tart skipped; numbered menu and comma-formatted prices | yes |
| `/post fun` | A streamed fun post | yes |
| `/post premium` | A streamed premium post | yes |
| `/post urgent` | A streamed urgent post | yes |
| `/post pirate` | Default fun tone used without an error | yes |
| `/price CUPCAKE` | Cupcake costs 250 PKR | yes |
| `/price mango tart` | Mango Tart is coming soon | yes |
| `/price donut` | Donut is not on the menu | yes |
| `My name is Ali` then `What is my name?` | Remembers Ali | yes |
| `/reset`, then `What is my name?` | Does not know the name | yes |
| Press Enter without text | Asks for input again | yes |
| `BYE` | Goodbye and session report | yes |

## 5. Testing notes

- Menu generation should skip zero-price products before calling the AI.
- Price lookups should use the Python dictionary, not the AI.
- Chat should retain the system message while trimming old conversation messages.
- Social media posts should display chunks as they arrive.
- The session report should show the totals for all AI activity.
