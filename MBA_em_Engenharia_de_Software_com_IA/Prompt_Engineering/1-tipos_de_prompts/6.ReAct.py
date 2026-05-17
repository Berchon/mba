from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from utils import print_llm_result

load_dotenv()

msg1 = """
You are a Go backend engineer helping debug a REST API. 
Use the ReAct style reasoning: alternate between "Thought:" (your reasoning) and "Action:" (a concrete step or check you would perform). 
After each action, write "Observation:" to capture what you found. 
At the end, conclude with "Final Answer:" as your recommended fix.

Do not fabricate any information that is not provided in the context. Example: if the context does not provide errors logs, do not use error logs in your reasoning.

Context: A user reports that the endpoint `POST /products` always returns HTTP 500.  

Here is the handler code for `POST /products`:

```go
func CreateProduct(w http.ResponseWriter, r *http.Request) {
    var product Product
    err := json.NewDecoder(r.Body).Decode(&product)
    if err != nil {
        http.Error(w, "Bad Request", http.StatusBadRequest)
        return
    }

    stmt, err := db.Prepare("INSERT INTO products (id, name, description, price, stock) VALUES (?, ?, ?, ?, ?)")
    if err != nil {
        log.Fatal(err)
    }

    _, err = stmt.Exec(product.ID, product.Name, product.Description, product.Price, product.Stock)
    if err != nil {
        log.Println("Error during Exec:", err)
        http.Error(w, "Internal Server Error", http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusCreated)
}

type Product struct {
    ID          string  `json:"id"`
    Name        string  `json:"name"`
    Description string  `json:"description"`
    Price       string  `json:"price"` 
    Stock       int     `json:"stock"`
}
```
"""

msg2 = f"""
You are a travel planner helping a family choose the best way to go from Orlando to New York next month. 
Use the ReAct style reasoning: alternate between "Thought:" (your reasoning) and "Action:" (a step such as checking flight time, costs, or convenience). 
After each action, write "Observation:" with what you found. 
At the end, conclude with "Final Answer:" as your recommendation. 

Context:  
- The family has 2 adults and 2 children (ages 5 and 8).  
- Budget: max $1,000 for transport (not including hotel).  
- Dates: they must arrive on July 10 in the evening.  
- Options:  
  - **Flight**: $220 per person round trip, 3-hour flight, plus $80 total in baggage fees.  
  - **Train**: $150 per person round trip, 20-hour journey, with onboard WiFi and beds available for $50 extra per person.  
  - **Car rental**: $60/day, 2 days of driving each way (gas + tolls estimated $250 total). Kids get restless on long trips.  

Other details:  
- The kids’ school finishes on July 9 at noon.  
- Parents prefer not to arrive too tired, since they have a family wedding on July 11 in the morning.  

Start your reasoning now.
"""

model_strong = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
model_mid = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
model_light = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

response1_light = model_light.invoke(msg1)
response1_mid = model_mid.invoke(msg1)
response1_strong = model_strong.invoke(msg1)

print_llm_result(msg1, response1_light)
print_llm_result(msg1, response1_mid)
print_llm_result(msg1, response1_strong)

print("="*70)

response2_light = model_light.invoke(msg2)
response2_mid = model_mid.invoke(msg2)
response2_strong = model_strong.invoke(msg2)

print_llm_result(msg2, response2_light)
print_llm_result(msg2, response2_mid)
print_llm_result(msg2, response2_strong)