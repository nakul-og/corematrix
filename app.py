from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# ─── DATA STORE ───────────────────────────────────────────────────────────────

WORKOUT_PLANS = [
    {
        "id": 1,
        "name": "Alpha Shred",
        "level": "Advanced",
        "duration": "12 Weeks",
        "category": "Fat Loss",
        "sessions_per_week": 5,
        "description": "Elite fat-loss protocol combining HIIT, strength supersets and metabolic conditioning for maximum caloric burn.",
        "image": "shred",
        "color": "#FF4D00",
        "exercises": ["Barbell Complex", "Sprint Intervals", "Cable Supersets", "Plyo Circuits"],
        "goal": "Lose 8-12% body fat while preserving lean muscle"
    },
    {
        "id": 2,
        "name": "Titan Build",
        "level": "Intermediate",
        "duration": "16 Weeks",
        "category": "Muscle Gain",
        "sessions_per_week": 4,
        "description": "Progressive hypertrophy system built on compound lifts, strategic volume manipulation and precision nutrition timing.",
        "image": "build",
        "color": "#C0A060",
        "exercises": ["Squat Variations", "Deadlift Progressions", "Press Patterns", "Pull Supinations"],
        "goal": "Pack on 8-15 lbs of lean muscle mass"
    },
    {
        "id": 3,
        "name": "Apex Athlete",
        "level": "Elite",
        "duration": "20 Weeks",
        "category": "Performance",
        "sessions_per_week": 6,
        "description": "Sport-science driven athletic development protocol. Power, speed, endurance — all elevated simultaneously.",
        "image": "athlete",
        "color": "#00C9FF",
        "exercises": ["Olympic Lifts", "Plyometrics", "Agility Drills", "Zone 2 Cardio"],
        "goal": "Peak athletic performance and VO2 Max improvement"
    },
    {
        "id": 4,
        "name": "Foundation Reset",
        "level": "Beginner",
        "duration": "8 Weeks",
        "category": "Fundamentals",
        "sessions_per_week": 3,
        "description": "Master the fundamentals with evidence-based movement patterns. Build the base that every elite physique is built on.",
        "image": "foundation",
        "color": "#A0FF60",
        "exercises": ["Bodyweight Mastery", "Mobility Work", "Basic Compounds", "Core Stability"],
        "goal": "Build strength, posture and movement quality from zero"
    }
]

TRAINERS = [
    {
        "id": 1,
        "name": "Marcus Vane",
        "title": "Head of Strength & Conditioning",
        "specialties": ["Powerlifting", "Athletic Performance", "Body Recomposition"],
        "experience": "12 Years",
        "certifications": ["NSCA-CSCS", "CF-L3", "USAW Sports Performance"],
        "bio": "Former professional athlete turned elite coach. Marcus has trained 3 Olympians and 200+ competitive athletes across 15 sports.",
        "clients_trained": 847,
        "rating": 4.9,
        "emoji": "💪"
    },
    {
        "id": 2,
        "name": "Zara Soleil",
        "title": "Nutrition & Transformation Specialist",
        "specialties": ["Fat Loss", "Nutrition Science", "Mindset Coaching"],
        "experience": "9 Years",
        "certifications": ["PRECISION NUTRITION L2", "ACE-CPT", "NASM-CNC"],
        "bio": "Biochemist turned fitness coach. Zara's science-first approach has helped over 500 clients achieve sustainable transformations.",
        "clients_trained": 612,
        "rating": 4.8,
        "emoji": "🔬"
    },
    {
        "id": 3,
        "name": "Dante Cruz",
        "title": "Movement & Mobility Director",
        "specialties": ["Functional Movement", "Injury Rehab", "Flexibility"],
        "experience": "14 Years",
        "certifications": ["FMS L2", "SFMA", "DNS Certified"],
        "bio": "Physical therapist and movement specialist. Dante rebuilds athletes from the ground up with his proprietary CoreMatrix Movement System.",
        "clients_trained": 1023,
        "rating": 5.0,
        "emoji": "🎯"
    },
    {
        "id": 4,
        "name": "Kai Nakamura",
        "title": "HIIT & Metabolic Conditioning Expert",
        "specialties": ["HIIT", "Endurance", "Group Training"],
        "experience": "8 Years",
        "certifications": ["ACSM-EP", "Orangetheory Elite", "TRX Master Trainer"],
        "bio": "Ultra-marathon finisher and metabolic conditioning specialist. Kai's sessions are legendary — intense, precise and transformative.",
        "clients_trained": 445,
        "rating": 4.9,
        "emoji": "⚡"
    }
]

TRANSFORMATIONS = [
    {
        "id": 1,
        "name": "Jordan M.",
        "duration": "16 Weeks",
        "plan": "Alpha Shred",
        "weight_lost": "38 lbs",
        "body_fat_change": "-11%",
        "testimonial": "CoreMatrix didn't just change my body — it rewired how I think about fitness entirely.",
        "trainer": "Marcus Vane"
    },
    {
        "id": 2,
        "name": "Sofia R.",
        "duration": "20 Weeks",
        "plan": "Titan Build",
        "muscle_gained": "14 lbs",
        "body_fat_change": "-4%",
        "testimonial": "I've tried every program. Nothing compares to the CoreMatrix methodology. Period.",
        "trainer": "Zara Soleil"
    },
    {
        "id": 3,
        "name": "Alex T.",
        "duration": "12 Weeks",
        "plan": "Apex Athlete",
        "performance": "+40% strength",
        "body_fat_change": "-7%",
        "testimonial": "My lifts went through the roof. CoreMatrix is the real deal for serious athletes.",
        "trainer": "Dante Cruz"
    }
]

FITNESS_CONTENT = [
    {
        "id": 1,
        "type": "tip",
        "title": "Progressive Overload Explained",
        "content": "Add 2.5-5% more load or 1-2 reps every session. This single principle drives 80% of all muscle growth.",
        "category": "Training",
        "icon": "📈",
        "likes": 2847
    },
    {
        "id": 2,
        "type": "nutrition",
        "title": "Protein Timing Myth Busted",
        "content": "Total daily protein (0.8-1g per lb bodyweight) matters far more than the 30-minute anabolic window. Consistency beats timing.",
        "category": "Nutrition",
        "icon": "🥩",
        "likes": 1923
    },
    {
        "id": 3,
        "type": "science",
        "title": "Sleep: The Real Performance Drug",
        "content": "7-9 hours of sleep increases testosterone by 15%, reduces cortisol by 37%, and boosts recovery speed by 2x. No supplement replicates this.",
        "category": "Recovery",
        "icon": "😴",
        "likes": 3401
    },
    {
        "id": 4,
        "type": "mindset",
        "title": "The 40% Rule",
        "content": "When your mind tells you you're done, you're actually only at 40% capacity. Elite athletes train in this mental gap.",
        "category": "Mindset",
        "icon": "🧠",
        "likes": 4122
    },
    {
        "id": 5,
        "type": "tip",
        "title": "Deload Week Protocol",
        "content": "Every 4-6 weeks, drop volume by 40-50%. Counter-intuitive but deloads prevent overtraining and often trigger breakthroughs.",
        "category": "Training",
        "icon": "🔄",
        "likes": 1567
    },
    {
        "id": 6,
        "type": "nutrition",
        "title": "Creatine: The GOAT Supplement",
        "content": "5g daily creatine monohydrate. Backed by 1000+ studies. Increases strength 5-15%, delays fatigue, and costs pennies. Non-negotiable.",
        "category": "Nutrition",
        "icon": "⚗️",
        "likes": 5238
    }
]

STATS = {
    "members": 12847,
    "transformations": 4200,
    "trainers": 24,
    "countries": 38,
    "avg_rating": 4.9,
    "programs": 16
}

# ─── API ROUTES ────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({"success": True, "data": STATS})

@app.route('/api/workouts', methods=['GET'])
def get_workouts():
    category = request.args.get('category')
    level = request.args.get('level')
    plans = WORKOUT_PLANS
    if category:
        plans = [p for p in plans if p['category'].lower() == category.lower()]
    if level:
        plans = [p for p in plans if p['level'].lower() == level.lower()]
    return jsonify({"success": True, "data": plans, "total": len(plans)})

@app.route('/api/workouts/<int:plan_id>', methods=['GET'])
def get_workout(plan_id):
    plan = next((p for p in WORKOUT_PLANS if p['id'] == plan_id), None)
    if not plan:
        return jsonify({"success": False, "error": "Plan not found"}), 404
    return jsonify({"success": True, "data": plan})

@app.route('/api/trainers', methods=['GET'])
def get_trainers():
    return jsonify({"success": True, "data": TRAINERS, "total": len(TRAINERS)})

@app.route('/api/trainers/<int:trainer_id>', methods=['GET'])
def get_trainer(trainer_id):
    trainer = next((t for t in TRAINERS if t['id'] == trainer_id), None)
    if not trainer:
        return jsonify({"success": False, "error": "Trainer not found"}), 404
    return jsonify({"success": True, "data": trainer})

@app.route('/api/transformations', methods=['GET'])
def get_transformations():
    return jsonify({"success": True, "data": TRANSFORMATIONS})

@app.route('/api/content', methods=['GET'])
def get_content():
    content_type = request.args.get('type')
    category = request.args.get('category')
    content = FITNESS_CONTENT
    if content_type:
        content = [c for c in content if c['type'] == content_type]
    if category:
        content = [c for c in content if c['category'].lower() == category.lower()]
    return jsonify({"success": True, "data": content, "total": len(content)})

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('email', '')
    name = data.get('name', '')
    if not email or '@' not in email:
        return jsonify({"success": False, "error": "Valid email required"}), 400
    return jsonify({
        "success": True,
        "message": f"Welcome to CoreMatrix, {name or 'Athlete'}! Your transformation starts now.",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()
    required = ['name', 'email', 'message']
    for field in required:
        if not data.get(field):
            return jsonify({"success": False, "error": f"{field} is required"}), 400
    return jsonify({
        "success": True,
        "message": "Message received. A CoreMatrix coach will respond within 24 hours.",
        "ticket_id": f"CM-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
