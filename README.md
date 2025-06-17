# 🎯 Habit Tracker Pro Max

A comprehensive, feature-rich habit tracking application built with Python and Tkinter. Track your daily habits, build streaks, earn achievements, and visualize your progress with beautiful contribution graphs and analytics.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### 🏆 Core Habit Tracking
- **Smart Habit Management**: Create habits with categories, difficulty levels, and daily goals
- **Streak Tracking**: Real-time streak calculation with best streak records
- **Achievement System**: 20+ achievements to unlock based on your progress
- **Points & Leveling**: Earn points based on habit difficulty and level up your virtual pet
- **Progress Analytics**: Detailed statistics and completion rate tracking

### 📊 Visualization & Analytics
- **Contribution Graphs**: GitHub-style activity visualization for the last 12 weeks
- **Calendar View**: Monthly calendar showing completion patterns
- **Category Breakdown**: Performance analytics by habit category
- **Smart Insights**: AI-powered suggestions and pattern recognition
- **Progress Bars**: Visual daily goal tracking

### 🎨 User Experience
- **6 Beautiful Themes**: Dark, Light, Forest, Ocean, Sunset, and Cosmic themes
- **Modern UI**: Clean, responsive interface with smooth animations
- **Keyboard Shortcuts**: Quick actions with Space, Ctrl+N, Ctrl+S, etc.
- **Virtual Pet**: Cute companion that grows with your habit consistency
- **Mood Tracking**: Daily mood logging with emoji interface

### 📱 Social Features (Demo)
- **Buddy Codes**: Compare progress with friends (simulated)
- **Leaderboard**: Global ranking system (demo mode)
- **Social Sharing**: Export achievements and stats for sharing

### 🔧 Advanced Features
- **Habit Dependencies**: Set prerequisite habits that must be completed first
- **Smart Reminders**: Time-based notifications for habit completion
- **Notes & Photos**: Attach contextual information to habit completions
- **Data Export/Import**: CSV and JSON support for data portability
- **Habit Templates**: Quick-start templates for common habits

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)
- Standard library modules: `json`, `csv`, `datetime`, `threading`, `random`

### Installation

1. **Download the application**:
   - Download `habit_tracker.py` to your desired folder

2. **Run the application**:
   ```bash
   python habit_tracker.py
   ```

### First Time Setup
1. Launch the app
2. Add your first habit using the "Add New Habit" section
3. Set category, difficulty, and daily goal
4. Start tracking by clicking habits and using the "✓ Complete" button
5. Explore different views: Dashboard, Analytics, Achievements, Social, Settings

## 📖 Usage Guide

### Creating Habits
```
📝 Habit Name: "Morning Exercise"
📁 Category: Health
⚡ Difficulty: Medium (3 points)
🎯 Daily Goal: 1
📅 Type: Daily
```

### Keyboard Shortcuts
- `Space`: Toggle selected habit completion
- `Ctrl+N`: Focus on new habit input
- `Ctrl+S`: Export data
- `Ctrl+A`: Open achievements view
- `Ctrl+T`: Cycle through themes

### Habit Dependencies
Set up habit chains where completing one habit unlocks another:
```
"Brush Teeth" → "Morning Vitamins" → "Workout"
```

### Quick Actions
- **✓ Complete**: Mark habit as done for today
- **✗ Remove**: Undo today's completion
- **📝 Note**: Add context or reflection
- **📸 Photo**: Attach visual progress
- **📅 Calendar**: View completion history
- **⏰ Reminder**: Set notification times

## 📊 Data & Analytics

### Contribution Graph
Visual representation of your consistency over the last 12 weeks, similar to GitHub's contribution graph.

### Statistics Tracked
- Current and best streaks
- Completion rates (7-day, 30-day)
- Category performance
- Total completions and points
- Perfect day streaks
- Early bird / night owl patterns

### Achievement Categories
- **Milestone**: First completion, streak goals, point thresholds
- **Consistency**: Perfect weeks/months, long streaks
- **Variety**: Multiple categories, habit collection
- **Social**: Sharing achievements (demo)
- **Special**: Early morning, late night completions

## 🎨 Themes

Choose from 6 carefully crafted themes:

| Theme | Description |
|-------|-------------|
| **Dark** | Classic dark mode with purple accents |
| **Light** | Clean light theme with blue highlights |
| **Forest** | Nature-inspired green tones |
| **Ocean** | Calming blue ocean vibes |
| **Sunset** | Warm orange and red gradients |
| **Cosmic** | Deep purple space theme |

## 💾 Data Management

### Local Storage
- **Habits**: `habits_pro_max.json`
- **Settings**: `settings_max.json`
- **Location**: Same directory as the application

### Export Formats
- **CSV**: Spreadsheet-compatible habit completion logs
- **JSON**: Complete data backup including settings and achievements

### Backup Strategy
1. Regular exports via Settings → Data Management
2. Copy JSON files to cloud storage
3. Version control your data files

## 🔧 Configuration

### Settings File Structure
```json
{
  "theme": "dark",
  "sound_enabled": true,
  "total_points": 150,
  "pet_level": 3,
  "pet_happiness": 75,
  "achieved": ["first_step", "week_warrior"],
  "buddy_code": "A1B2C3D4"
}
```

### Habit Data Structure
```json
{
  "Morning Exercise": {
    "completions": ["2024-01-15", "2024-01-16"],
    "category": "Health",
    "difficulty": "Medium",
    "daily_goal": 1,
    "habit_type": "Daily",
    "notes": {"2024-01-15": "Felt great today!"},
    "reminders": ["07:00"],
    "dependencies": [],
    "completion_times": {"2024-01-15": ["07:30"]},
    "mood_ratings": {"2024-01-15": 4},
    "photos": {}
  }
}
```

## 🤝 Contributing

Contributions are welcome! Here are some areas for improvement:

### Real Features to Implement
- **Cloud Sync**: Firebase or AWS backend for data synchronization
- **Real Social**: Actual buddy system with user accounts
- **Mobile App**: React Native or Flutter companion
- **Web Dashboard**: Browser-based analytics and management
- **Smart Notifications**: OS-level notifications with scheduling

### Enhancement Ideas
- **Habit Streaks Visualization**: More detailed streak analytics
- **Goal Setting**: Weekly, monthly, and yearly goals
- **Habit Insights**: Machine learning for pattern recognition
- **Integrations**: Fitness apps, calendar apps, weather APIs
- **Gamification**: More achievements, levels, and rewards

### Development Setup
1. Download the source code
2. Create a feature branch for your changes
3. Make your modifications
4. Test thoroughly with different habits and scenarios
5. Share your improvements

## 📋 Known Limitations

### Simulated Features
- **Buddy Code System**: Generates fake comparison data
- **Weather Correlations**: Placeholder data, not real weather API
- **Global Leaderboard**: Random simulated users
- **Cloud Backup**: Shows "coming soon" message
- **AI Predictions**: Basic rule-based suggestions

### Platform Limitations
- **Sound Effects**: Windows-only (winsound), fallback to terminal bell
- **Notifications**: Basic threading, not OS-level notifications
- **File Dialogs**: Uses tkinter's basic file dialogs

## 🐛 Troubleshooting

### Common Issues

**Application won't start**:
- Ensure Python 3.7+ is installed
- Check that tkinter is available: `python -c "import tkinter"`

**Data not saving**:
- Check file permissions in the application directory
- Ensure sufficient disk space

**Themes not changing**:
- Restart the application after theme change
- Check if settings file is writable

**Missing achievements**:
- Achievements are calculated in real-time
- Some require specific conditions (e.g., early morning completions)

### Performance Tips
- Keep total habits under 50 for optimal performance
- Regular data exports to prevent large file sizes
- Close unused views when working with many habits

## 🙏 Acknowledgments

- **Tkinter**: Python's standard GUI toolkit
- **GitHub**: Inspiration for contribution graph design
- **Habitica**: Gamification concepts and achievement ideas
- **Streaks**: iOS app inspiration for streak tracking

