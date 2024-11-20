from genai import credentials, Client

# Step 1: Set up credentials
api_key = "AIzaSyAShoNIrwCbeirFQ-BQh5OZDKuZiA7XQhQ"  # Replace with your actual Gemini API key
credentials = Credentials(api_key)

# Step 2: Initialize the client
client = Client(credentials)

# Step 3: Define your input prompt
prompt = "Write a short story about a robot exploring Mars."

# Step 4: Generate content
response = client.generate(
    model="gemini-1.5-flash",  # Use the desired model
    prompts=[prompt],
    parameters={
        "max_tokens": 200,  # Set the max token limit for response
        "temperature": 0.7,  # Creativity level (higher = more creative)
        "top_p": 0.9        # Probabilistic sampling parameter
    }
)

# Step 5: Print the generated content
for i, result in enumerate(response.results):
    print(f"Generated Content {i+1}:\n{result.generated_text}")
