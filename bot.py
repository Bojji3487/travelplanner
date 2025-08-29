import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import dotenv,os

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")
API_URL = "http://127.0.0.1:8000/plan-trip"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class PlanTripStates(StatesGroup):
    destination = State()
    days = State()
    budget = State()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("👋 Hi! Use /plantrip to plan a trip interactively.")

@dp.message(Command("plantrip"))
async def plantrip_cmd(message: types.Message, state: FSMContext):
    await message.answer("✈️ Where do you want to go?")
    await state.set_state(PlanTripStates.destination)

@dp.message(PlanTripStates.destination)
async def process_destination(message: types.Message, state: FSMContext):
    await state.update_data(destination=message.text)
    await message.answer("📅 How many days?")
    await state.set_state(PlanTripStates.days)

@dp.message(PlanTripStates.days)
async def process_days(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Please enter a number for days.")
        return
    await state.update_data(days=int(message.text))
    await message.answer("💰 What’s your budget?")
    await state.set_state(PlanTripStates.budget)

@dp.message(PlanTripStates.budget)
async def process_budget(message: types.Message, state: FSMContext):
    try:
        budget = float(message.text)
    except ValueError:
        await message.answer("❌ Please enter a valid number for budget.")
        return

    await state.update_data(budget=budget)
    data = await state.get_data()

    async with httpx.AsyncClient() as client:
        resp = await client.post(API_URL, json=data)
        trip = resp.json()

    reply = (
        f"✅ Trip planned!\n"
        f"Destination: {trip['destination']}\n"
        f"Days: {trip['days']}\n"
        f"Budget: {trip['budget']}\n\n"
        f"Itinerary:\n- " + "\n- ".join(trip["itinerary"])
    )
    await message.answer(reply)
    await state.clear()
