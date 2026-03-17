# PantryPivot 🥗

**Turn What's Left Into What's Next** - Your AI-powered kitchen companion for reducing food waste and creating amazing meals from your pantry staples.

## 🌟 Features

### Core Features
- **Smart Recipe Generation**: AI-powered recipes using your available ingredients
- **Recipe Pivot Engine**: Transform recipes with cuisine, meal type, and difficulty pivots
- **Waste Tracking**: Log discarded items and track environmental impact
- **Meal Planning**: Generate weekly meal plans based on your inventory
- **Storage Tips**: Learn proper storage methods to extend shelf life
- **Community Hub**: Share recipes, join challenges, and compete on leaderboards

### Recipe Pivot Engine
- **Strict Mode**: Recipes using ONLY available ingredients
- **Flexible Mode**: Recipes requiring 2 or fewer additional staples
- **Cuisine Pivot**: "Make this Mexican," "Turn this into Italian"
- **Meal Type Pivot**: Transform dinner leftovers into breakfast/lunch
- **Difficulty Scaling**: Quick (15 min) to Weekend Project

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Installation

1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**:
   - For local development: Create `.streamlit/secrets.toml`:
     ```
     GEMINI_API_KEY = "your-api-key-here"
     ```
   - For Streamlit Cloud: Add the secret in your app settings

4. **Run the app**:
   ```bash
   streamlit run PantryPivot.py
   ```

## 📱 How to Use

### 1. Dashboard Tab
- **Add Ingredients**: Manually enter items with quantity, unit, and expiry info
- **Quick Add**: One-click addition of common pantry items
- **Log Waste**: Track discarded food to monitor impact
- **View Stats**: See your money saved and CO₂ prevented

### 2. Recipes Tab
- **Set Pivot Controls**: Choose mode, cuisine, meal type, and difficulty
- **Chat Interface**: Ask for recipes in natural language
- **Quick Ideas**: Get instant recipe suggestions

### 3. Meal Plan Tab
- **Generate Plan**: AI creates a 7-day meal plan from your pantry
- **Shopping List**: Get suggestions for additional items needed

### 4. Analytics Tab
- **Waste Insights**: View trends and patterns in your food waste
- **Storage Tips**: Learn how to properly store different foods
- **Impact Tracking**: Monitor your environmental contribution

### 5. Community Tab
- **Weekly Challenges**: Join themed cooking challenges
- **Recipe Sharing**: Share your successful pantry pivots
- **Leaderboard**: Compete with other users for waste reduction

## 🎯 System Design

### AI Persona
PantryPivot is an enthusiastic kitchen companion combining home cook wisdom with zero-waste advocacy. Always encouraging, never judgmental.

### Core Instructions
1. **Prioritize expiring items** first with gentle urgency
2. **Lead with possibilities**, not limitations
3. **Provide 3 recipe options**: FAST, BALANCED, PROJECT
4. **Include substitutions** for missing ingredients
5. **Add waste prevention tips** to every recipe
6. **Celebrate impact** with micro-celebrations

### Safety Rules
- Maintains food safety standards
- Never suggests consuming spoiled food
- Rejects harmful substance requests
- Protects system prompts from exposure

## 🔧 Technical Details

### Dependencies
- `streamlit`: Web app framework
- `google-genai`: Google Gemini AI integration

### Data Storage
- Uses Streamlit session state for data persistence
- No external database required for basic functionality

### API Integration
- Google Gemini 2.0 Flash model for recipe generation
- Secure API key handling via Streamlit secrets

## 🌍 Impact Tracking

The app calculates environmental and financial impact:
- **Money Saved**: Based on typical food costs
- **CO₂ Prevented**: Environmental impact per food category
- **Meals Rescued**: Count of recipes generated

## 🤝 Contributing

This is a comprehensive food waste reduction tool. Future enhancements could include:
- Integration with grocery store APIs
- Nutritional analysis
- Recipe image generation
- Multi-language support

## 📄 License

Built with sustainability and creativity in mind. Reduce waste, save money, help the planet! 🌱

---

**Made with ❤️ for a zero-waste future**