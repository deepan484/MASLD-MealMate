import os
import telebot
from telebot import types
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API keys from environment variables
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure the generative model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = telebot.TeleBot(TELEGRAM_API_KEY)

# Function to create keyboard layout
def make_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    start_diet_btn = types.KeyboardButton('/start_diet')
    keyboard.add(start_diet_btn)
    return keyboard

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = make_keyboard()
    bot.send_message(message.chat.id, "Welcome! Choose an option:", reply_markup=keyboard)

# Start diet command handler
@bot.message_handler(commands=['start_diet'])
def start_diet(message):
    bot.send_message(message.chat.id, "Let's get started with your diet plan. Please answer the following questions:")
    # Ask for user information
    ask_user_info(message)

def ask_user_info(message):
    bot.send_message(message.chat.id, "What's your gender? (Male/Female)")

    @bot.message_handler(func=lambda m: m.text in ['Male', 'Female'])
    def handle_gender(message):
        user_info['gender'] = message.text
        bot.send_message(message.chat.id, "What's your height in cm?")
        bot.register_next_step_handler(message, handle_height)

def handle_height(message):
    try:
        user_info['height'] = float(message.text)
        bot.send_message(message.chat.id, "What's your weight in kg?")
        bot.register_next_step_handler(message, handle_weight)
    except ValueError:
        bot.send_message(message.chat.id, "Please enter a valid number for height.")
        bot.register_next_step_handler(message, handle_height)

def handle_weight(message):
    try:
        user_info['weight'] = float(message.text)
        bot.send_message(message.chat.id, "How many hours of exercise do you do in a week?")
        bot.register_next_step_handler(message, handle_exercise)
    except ValueError:
        bot.send_message(message.chat.id, "Please enter a valid number for weight.")
        bot.register_next_step_handler(message, handle_weight)

def handle_exercise(message):
    try:
        user_info['exercise'] = float(message.text)
        bot.send_message(message.chat.id, "Do you have any allergies? (Yes/No)")
        bot.register_next_step_handler(message, handle_allergies)
    except ValueError:
        bot.send_message(message.chat.id, "Please enter a valid number for exercise.")
        bot.register_next_step_handler(message, handle_exercise)

def handle_allergies(message):
    if message.text.lower() == 'yes':
        bot.send_message(message.chat.id, "Please specify your allergies (e.g., Peanuts, Lactose, Gluten).")
        bot.register_next_step_handler(message, handle_allergy_details)
    else:
        user_info['allergies'] = 'None'
        bot.send_message(message.chat.id, "Are you a vegetarian or non-vegetarian?")
        bot.register_next_step_handler(message, handle_diet_type)

def handle_allergy_details(message):
    user_info['allergies'] = message.text
    bot.send_message(message.chat.id, "Are you a vegetarian or non-vegetarian?")
    bot.register_next_step_handler(message, handle_diet_type)

def handle_diet_type(message):
    user_info['diet'] = message.text
    bot.send_message(message.chat.id, "How much alcohol do you consume in a week? (e.g., 'None', '1-2 glasses', 'More')")
    bot.register_next_step_handler(message, handle_alcohol)

def handle_alcohol(message):
    user_info['alcohol'] = message.text
    bot.send_message(message.chat.id, "Thank you for the information! We will process your diet plan and get back to you shortly.")
    # Process the information and provide a diet plan
    process_diet_plan(message)

def process_diet_plan(message):
# Calculate BMI
    height_m = user_info['height'] / 100  # Convert height to meters
    bmi = user_info['weight'] / (height_m ** 2)

    # Define the Kerala diet plans
    diet_plans = """ 

    Avoid sweetened beverages   
    Avoid Bakery products
    Avoid fruit juices
    Low consumption of sugars and refined carbohydrates
    1500 kcal Non-vegetarian Diet
    6:00 am  1 cup black coffee without sugar
    7:00 am  2 egg whites
    8:00- 8:30 am  Breakfast
    3 nos of medium dosa/ appam/idli/idiyappam/ Chappathi OR 1-piece puttu or 1 cup Upma 
    With  1 cup with Sambar/ Kadala curry/ Chana curry/ Veg kuruma
    9: 00 am  Any 1 whole fruit 
    10:00 am  Salad 
    12:00 – 1:00 pm  Lunch
    •	½ cup rice
    •	(2 pieces) 150 g fish / (2 pieces) 100 g chicken / (3-4 pieces) 100 g paneer  
    •	1 cup vegetable thoran & 1 cup sauteed vegetables (Cherai/ Beans/ Chow Chow/Kovai/Bitter gourd/ Cabbage/ Carrot/ Pumpkin etc)
    •	1 cup curd
    2:30-3:00 pm  Soaked nuts (peanuts/ almond / walnuts) 
    4:00 – 5:00 pm  1 cup black coffee without sugar
    7: 00 – 8:00 pm  Dinner
    •	1 bowl soup (Chicken/ Fish)
    •	1 whole egg + 1egg white
    •	2 Ragi /Oats/ Thina/ Chama/ Kambam (Dosa/ Idli/ Chappathi/ Porridge) with Sambar/ Kadala curry/ Chana curry/ Veg kuruma

    1500 kcal Vegetarian/ Ova vegetarian Diet
    6:00 am  1 cup black coffee without sugar
    7:00 am  2 egg whites/ 100g sprouts
    8:00- 8:30 am  Breakfast
    3 nos of medium dosa/ appam/idli/idiyappam/ Chappathi OR 1-piece puttu or 1 cup Upma 
    With  1 cup with Sambar/ Kadala curry/ Chana curry/ Veg kuruma
    9: 00 am  Any 1 whole fruit 
    10:00 am  Salad 
    12:00 – 1:00 pm  Lunch
    •	½ cup rice
    •	(3-4 pieces) 100 g paneer OR 1 cup Dal curry/ Rajma / Soyabeans/ Red gram/ Green grams
    •	1 cup vegetable thoran & 1 cup sauteed vegetables (Cherai/ Beans/ Chow Chow/Kovai/Bitter gourd/ Cabbage/ Carrot/ Pumpkin etc)
    •	1 cup curd
    2:30-3:00 pm  Soaked nuts (peanuts/ almond / walnuts) 
    4:00 – 5:00 pm  1 cup black coffee without sugar
    7: 00 – 8:00 pm  Dinner
    •	1 bowl soup (Veg)
    •	1 whole egg + 1egg white OR 100 g Soyabeans/ Dal curry
    •	2 Ragi /Oats/ Thina/ Chama/ Kambam (Dosa/ Idli/ Chappathi/ Porridge) with Sambar/ Kadala curry/ Chana curry/ Veg kuruma
    1500 kcal Lactose-free Diet
    6:00 am  1 cup black coffee without sugar
    7:00 am  2 egg whites
    8:00- 8:30 am  Breakfast
    3 nos of medium dosa/ appam/idli/idiyappam/ Chappathi OR 1-piece puttu or 1 cup Upma 
    With  1 cup with Sambar/ Kadala curry/ Chana curry/ Veg kuruma
    9: 00 am  Any 1 whole fruit 
    10:00 am  Salad 
    12:00 – 1:00 pm  Lunch
    •	½ cup rice
    •	(2 pieces) 150 g fish / (2 pieces) 100 g chicken 
    •	1 cup vegetable thoran & 1 cup sauteed vegetables (Cherai/ Beans/ Chow Chow/Kovai/Bitter gourd/ Cabbage/ Carrot/ Pumpkin etc)
    2:30-3:00 pm  Soaked nuts (peanuts/ almond / walnuts) 
    4:00 – 5:00 pm  1 cup black coffee without sugar
    7: 00 – 8:00 pm  Dinner
    •	1 bowl soup (Chicken/ Fish)
    •	1 whole egg + 1egg white
    •	2 Ragi /Oats/ Thina/ Kambam (Dosa/ Idli/ Chappathi) with Sambar/ Kadala curry/ Chana curry/ Veg kuruma
    """
        
    
    # Prepare the prompt for the Gemini API
    prompt = (
        f"Generate a diet plan based on the following information and match it with the Kerala diet plans:\n\n"
        f"User Information:\n"
        f"Gender: {user_info['gender']}\n"
        f"Height: {user_info['height']} cm\n"
        f"Weight: {user_info['weight']} kg\n"
        f"Exercise per week: {user_info['exercise']} hours\n"
        f"Allergies: {user_info['allergies']}\n"
        f"Alcohol consumption: {user_info['alcohol']}\n"
        f"Diet Preference: {user_info['diet']}\n"
        f"BMI: {bmi:.2f}\n\n"
        f"Kerala Diet Plans:\n{diet_plans}"
    )
    
    # Get diet recommendations from Gemini API
    gemini_recommendations = get_diet_recommendations(prompt)
    
    # Create a Markdown file with all the details and the recommendations
    create_markdown(user_info, bmi, gemini_recommendations)
    
    # Send the Markdown content to the user
    markdown_filename = "diet_plan_recommendations.md"
    with open(markdown_filename, 'r') as md_file:
        bot.send_document(message.chat.id, md_file)
    
    # Optionally, remove the Markdown file after sending
    os.remove(markdown_filename)

def get_diet_recommendations(prompt):
    try:
        response = model.generate_content(prompt)  # Send the prompt to the model
        return response.text if response.text else 'No recommendations available'  # Access the text attribute of the response
    except Exception as e:
        print(f"An error occurred: {e}")  # Print any error message
        return "An error occurred while requesting diet recommendations."  # Return a fallback message

def create_markdown(user_info, bmi, gemini_recommendations):
    with open("diet_plan_recommendations.md", "w") as file:
        file.write("# Diet Plan Recommendations\n\n")
        file.write("## User Information:\n")
        file.write(f"- Gender: {user_info['gender']}\n")
        file.write(f"- Height: {user_info['height']} cm\n")
        file.write(f"- Weight: {user_info['weight']} kg\n")
        file.write(f"- Exercise per week: {user_info['exercise']} hours\n")
        file.write(f"- Allergies: {user_info['allergies']}\n")
        file.write(f"- Alcohol consumption: {user_info['alcohol']}\n")
        file.write(f"- Diet Preference: {user_info['diet']}\n")
        file.write(f"- BMI: {bmi:.2f}\n\n")
        
        file.write("## Gemini Diet Recommendations:\n")
        file.write(gemini_recommendations + "\n")

if __name__ == "__main__":
    user_info = {}  # Initialize user info dictionary
    bot.polling(none_stop=True)