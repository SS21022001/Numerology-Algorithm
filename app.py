from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

NUMEROLOGY_DETAILS = {
    1: {"planet": "Sun", "quality": "Leadership, Independence, Creativity"},
    2: {"planet": "Moon", "quality": "Sensitivity, Diplomacy, Cooperation"},
    3: {"planet": "Jupiter", "quality": "Optimism, Enthusiasm, Communication"},
    4: {"planet": "Rahu (North Node)", "quality": "Discipline, Practicality, Hard Work"},
    5: {"planet": "Mercury", "quality": "Adaptability, Communication, Curiosity"},
    6: {"planet": "Venus", "quality": "Harmony, Beauty, Love"},
    7: {"planet": "Ketu (South Node)", "quality": "Spirituality, Introspection, Analysis"},
    8: {"planet": "Saturn", "quality": "Ambition, Discipline, Responsibility"},
    9: {"planet": "Mars", "quality": "Energy, Courage, Initiative"},
    11: {"planet": "Uranus", "quality": "Intuition, Vision, Innovation"},
    22: {"planet": "Neptune", "quality": "Master Builder, Idealism, Sensitivity"}
}

def reduce_to_single_digit(number):
    while number > 9 and number not in [11, 22]:
        number = sum(int(digit) for digit in str(number))
    return number

def calculate_life_path_number(day, month, year):
    total_sum = day + month + sum(int(digit) for digit in str(year))
    return reduce_to_single_digit(total_sum)

def calculate_birth_day_number(day):
    return reduce_to_single_digit(day)

def calculate_personal_year_number(day, month):
    current_year = datetime.now().year
    total_sum = day + month + sum(int(digit) for digit in str(current_year))
    return reduce_to_single_digit(total_sum)

def get_numerology_details(number):
    return NUMEROLOGY_DETAILS.get(number, {"planet": "Unknown", "quality": "Unknown"})

def generate_lo_shu_grid(dob):
    lo_shu_grid = {i: 0 for i in range(1, 10)}
    digits = [int(digit) for part in dob.split('-') for digit in part]
    for digit in digits:
        if (digit != 0):
            lo_shu_grid[digit] += 1
    return lo_shu_grid

def interpret_lo_shu_grid(grid):
    predictions = []

    # Mental Plane (1st Row: 4, 9, 2)
    if grid[4] > 0 and grid[9] > 0 and grid[2] > 0:
        predictions.append("Mental Plane: You are a genius with strong intellectual abilities.")
    elif grid[4] > 0 and grid[9] == 0 and grid[2] == 0:
        predictions.append("Mental Plane: You are flexible in nature.")
    elif grid[9] > 0 and grid[4] == 0 and grid[2] == 0:
        predictions.append("Mental Plane: You are religious and spiritually inclined.")
    elif grid[2] > 0 and grid[4] == 0 and grid[9] == 0:
        predictions.append("Mental Plane: You have strong emotional intelligence.")
    else:
        predictions.append("Mental Plane: There are gaps in your mental plane which may need attention.")

    # Emotional Plane (2nd Row: 3, 5, 7)
    if grid[3] > 0 and grid[5] > 0 and grid[7] > 0:
        predictions.append("Emotional Plane: You have balanced emotional qualities.")
    elif grid[3] > 0 and grid[5] == 0 and grid[7] == 0:
        predictions.append("Emotional Plane: You are expressive and creative.")
    elif grid[5] > 0 and grid[3] == 0 and grid[7] == 0:
        predictions.append("Emotional Plane: You are adaptable and communicative.")
    elif grid[7] > 0 and grid[3] == 0 and grid[5] == 0:
        predictions.append("Emotional Plane: You are introspective and analytical.")
    else:
        predictions.append("Emotional Plane: Your emotional balance may need some work.")

    # Physical Plane (3rd Row: 8, 1, 6)
    if grid[8] > 0 and grid[1] > 0 and grid[6] > 0:
        predictions.append("Physical Plane: You have strong physical vitality and practicality.")
    elif grid[8] > 0 and grid[1] == 0 and grid[6] == 0:
        predictions.append("Physical Plane: You are ambitious and disciplined.")
    elif grid[1] > 0 and grid[8] == 0 and grid[6] == 0:
        predictions.append("Physical Plane: You are a natural leader.")
    elif grid[6] > 0 and grid[8] == 0 and grid[1] == 0:
        predictions.append("Physical Plane: You appreciate beauty and harmony.")
    else:
        predictions.append("Physical Plane: You may need to focus on grounding yourself physically.")

    # Vision Plane (Column 1: 4, 3, 8)
    if grid[4] > 0 and grid[3] > 0 and grid[8] > 0:
        predictions.append("Vision Plane: You have a balanced vision with practical implementation.")
    elif grid[4] > 0 and grid[3] == 0 and grid[8] == 0:
        predictions.append("Vision Plane: You are disciplined but need to express your creativity.")
    elif grid[3] > 0 and grid[4] == 0 and grid[8] == 0:
        predictions.append("Vision Plane: You are creative and expressive but may need to focus on discipline.")
    elif grid[8] > 0 and grid[4] == 0 and grid[3] == 0:
        predictions.append("Vision Plane: You are ambitious and practical.")
    else:
        predictions.append("Vision Plane: Your vision and its execution may need alignment.")

    # Will Plane (Column 2: 9, 5, 1)
    if grid[9] > 0 and grid[5] > 0 and grid[1] > 0:
        predictions.append("Will Plane: You have strong willpower, balanced by intellect and communication.")
    elif grid[9] > 0 and grid[5] == 0 and grid[1] == 0:
        predictions.append("Will Plane: Your strong will is driven by spiritual or intellectual pursuits.")
    elif grid[5] > 0 and grid[9] == 0 and grid[1] == 0:
        predictions.append("Will Plane: You have a flexible will, adaptable and communicative.")
    elif grid[1] > 0 and grid[9] == 0 and grid[5] == 0:
        predictions.append("Will Plane: You have strong leadership qualities.")
    else:
        predictions.append("Will Plane: Your willpower may require more balance.")

    # Action Plane (Column 3: 2, 7, 6)
    if grid[2] > 0 and grid[7] > 0 and grid[6] > 0:
        predictions.append("Action Plane: You are driven by a balanced approach in emotions, analysis, and love.")
    elif grid[2] > 0 and grid[7] == 0 and grid[6] == 0:
        predictions.append("Action Plane: Your actions are driven by sensitivity and diplomacy.")
    elif grid[7] > 0 and grid[2] == 0 and grid[6] == 0:
        predictions.append("Action Plane: Your actions are guided by deep introspection and analysis.")
    elif grid[6] > 0 and grid[2] == 0 and grid[7] == 0:
        predictions.append("Action Plane: You are driven by a love for beauty and harmony.")
    else:
        predictions.append("Action Plane: Your actions may need more focus and alignment.")

    return predictions

def numerology_predictions(dob):
    day, month, year = map(int, dob.split('-'))

    life_path_number = calculate_life_path_number(day, month, year)
    birth_day_number = calculate_birth_day_number(day)
    personal_year_number = calculate_personal_year_number(day, month)

    life_path_details = get_numerology_details(life_path_number)
    birth_day_details = get_numerology_details(birth_day_number)
    personal_year_details = get_numerology_details(personal_year_number)

    lo_shu_grid = generate_lo_shu_grid(dob)
    lo_shu_predictions = interpret_lo_shu_grid(lo_shu_grid)
    
    return {
        "Life Path Number": life_path_number,
        "Life Path Details": life_path_details,
        "Birth Day Number": birth_day_number,
        "Birth Day Details": birth_day_details,
        "Personal Year Number": personal_year_number,
        "Personal Year Details": personal_year_details,
        "Lo Shu Grid": lo_shu_grid,
        "Lo Shu Predictions": lo_shu_predictions
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    dob = request.form['birthdate']
    predictions = numerology_predictions(dob)
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)
