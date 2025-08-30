import google.generativeai as genai
import dotenv, os
import asyncio

dotenv.load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("⚠️ GEMINI_API_KEY not found in .env file")

# Configure Gemini API
genai.configure(api_key=API_KEY)
print("✅ Gemini API Key configured successfully!")

model = genai.GenerativeModel("gemini-2.5-flash")

async def generate_itinerary(destination, duration, budget, interests):
    if not destination.strip() or not duration.strip():
        return "⚠️ Please enter a destination and a Duration for your trip."

    prompt = f"""
    You are an expert travel agent and tour guide. Your task is to create a personalized,
    day-by-day travel itinerary for a user.

    **Travel Details:**
    *   **Destination:** {destination}
    *   **Duration of Stay:** {duration}
    *   **Budget:** {budget}
    *   **User's Interests:** {interests}

    **Instructions:**
    - Create a logical and efficient day-by-day itinerary. Group activities geographically to minimize travel time.
    - For each day, suggest activities for the morning, afternoon, and evening.
    - Include a mix of famous landmarks and local experiences based on the user's interests.
    - Suggest at least one food or restaurant type for each day that fits the local cuisine.
    - The tone should be enthusiastic and helpful.
    - Ensure that the output is formatted so that it fits in a a telegram message.

    **Output Format**

    Trip planned for {destination}!
    Day 1: [Give the day a theme, e.g., Historical Heart & Local Flavors]**
    [Activity 1 Description]
    [Activity 2 Description]
    [Activity 3, including a dinner suggestion]
    Estimated Budget

    Day 2: [Give the day a theme, e.g., Historical Heart & Local Flavors]**
    [Activity 1 Description]
    [Activity 2 Description]
    [Activity 3, including a dinner suggestion]
    Estimated Budget

    **(Continue for the number of days specified in the duration)...**

    **Travel Tip:** [Provide one useful tip for traveling in the specified destination.]
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ An error occurred while generating the itinerary: {e}"