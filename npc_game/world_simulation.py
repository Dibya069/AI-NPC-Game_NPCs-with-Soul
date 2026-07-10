"""
World Simulation Core
The living, breathing world that evolves independently
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from enum import Enum
import random
from datetime import datetime, timedelta


class TimeOfDay(Enum):
    """Time periods in the game world"""
    DAWN = "dawn"
    MORNING = "morning"
    NOON = "noon"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"
    MIDNIGHT = "midnight"


class Weather(Enum):
    """Weather conditions"""
    CLEAR = "clear"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    STORMY = "stormy"
    FOGGY = "foggy"
    SNOWY = "snowy"


@dataclass
class TimeEngine:
    """Manages world time and day/night cycles"""
    
    current_hour: int = 8  # 24-hour format
    current_day: int = 1
    minutes_per_tick: int = 15  # Each tick = 15 game minutes
    
    def advance(self, ticks: int = 1):
        """Advance time by number of ticks"""
        minutes = ticks * self.minutes_per_tick
        hours = minutes // 60
        
        self.current_hour = (self.current_hour + hours) % 24
        if self.current_hour < hours:  # Rolled over to new day
            self.current_day += 1
    
    def get_time_of_day(self) -> TimeOfDay:
        """Get current time period"""
        if 5 <= self.current_hour < 7:
            return TimeOfDay.DAWN
        elif 7 <= self.current_hour < 12:
            return TimeOfDay.MORNING
        elif 12 <= self.current_hour < 14:
            return TimeOfDay.NOON
        elif 14 <= self.current_hour < 18:
            return TimeOfDay.AFTERNOON
        elif 18 <= self.current_hour < 21:
            return TimeOfDay.EVENING
        elif 21 <= self.current_hour < 24:
            return TimeOfDay.NIGHT
        else:
            return TimeOfDay.MIDNIGHT
    
    def is_night(self) -> bool:
        """Check if it's nighttime"""
        return self.current_hour < 6 or self.current_hour >= 21
    
    def get_time_string(self) -> str:
        """Get formatted time string"""
        period = "AM" if self.current_hour < 12 else "PM"
        hour = self.current_hour if self.current_hour <= 12 else self.current_hour - 12
        hour = 12 if hour == 0 else hour
        return f"Day {self.current_day}, {hour}:00 {period} ({self.get_time_of_day().value})"


@dataclass
class WeatherEngine:
    """Manages dynamic weather"""
    
    current_weather: Weather = Weather.CLEAR
    weather_duration: int = 0  # Ticks remaining
    
    def update(self):
        """Update weather (potentially change it)"""
        self.weather_duration -= 1
        
        if self.weather_duration <= 0:
            # Time to change weather
            self.change_weather()
    
    def change_weather(self):
        """Change to new weather"""
        # Weather transition probabilities
        transitions = {
            Weather.CLEAR: [Weather.CLEAR, Weather.CLOUDY, Weather.FOGGY],
            Weather.CLOUDY: [Weather.CLEAR, Weather.CLOUDY, Weather.RAINY],
            Weather.RAINY: [Weather.RAINY, Weather.STORMY, Weather.CLOUDY],
            Weather.STORMY: [Weather.RAINY, Weather.CLOUDY],
            Weather.FOGGY: [Weather.CLEAR, Weather.CLOUDY],
            Weather.SNOWY: [Weather.SNOWY, Weather.CLOUDY, Weather.CLEAR]
        }
        
        possible = transitions.get(self.current_weather, [Weather.CLEAR])
        self.current_weather = random.choice(possible)
        self.weather_duration = random.randint(4, 12)  # 1-3 hours
    
    def get_description(self) -> str:
        """Get weather description"""
        descriptions = {
            Weather.CLEAR: "☀️ The sky is clear and bright",
            Weather.CLOUDY: "☁️ Clouds cover the sky",
            Weather.RAINY: "🌧️ Rain is falling steadily",
            Weather.STORMY: "⛈️ A fierce storm rages",
            Weather.FOGGY: "🌫️ Thick fog blankets the area",
            Weather.SNOWY: "❄️ Snow falls gently"
        }
        return descriptions.get(self.current_weather, "Weather is normal")


@dataclass
class Location:
    """A location in the world"""
    name: str
    description: str
    location_type: str  # tavern, market, home, etc.
    connected_to: List[str] = field(default_factory=list)
    npcs_present: Set[str] = field(default_factory=set)
    
    def add_npc(self, npc_name: str):
        """Add NPC to this location"""
        self.npcs_present.add(npc_name)
    
    def remove_npc(self, npc_name: str):
        """Remove NPC from this location"""
        self.npcs_present.discard(npc_name)
    
    def get_present_npcs(self) -> List[str]:
        """Get list of NPCs at this location"""
        return list(self.npcs_present)


@dataclass
class WorldSimulation:
    """
    The living world - orchestrates all systems
    """

    # Core engines
    time_engine: TimeEngine = field(default_factory=TimeEngine)
    weather_engine: WeatherEngine = field(default_factory=WeatherEngine)

    # World state
    locations: Dict[str, Location] = field(default_factory=dict)
    simulation_running: bool = False
    tick_count: int = 0

    def __post_init__(self):
        """Initialize world with default locations"""
        if not self.locations:
            self.locations = {
                "tavern": Location(
                    name="The Rusty Flagon Tavern",
                    description="A cozy tavern with warm fireplace",
                    location_type="tavern",
                    connected_to=["market", "town_square"]
                ),
                "market": Location(
                    name="Town Market",
                    description="Bustling marketplace with various stalls",
                    location_type="market",
                    connected_to=["tavern", "town_square", "merchant_quarter"]
                ),
                "town_square": Location(
                    name="Town Square",
                    description="Central square with a fountain",
                    location_type="public",
                    connected_to=["tavern", "market", "guard_house"]
                ),
                "guard_house": Location(
                    name="Guard House",
                    description="Official guard barracks and office",
                    location_type="official",
                    connected_to=["town_square"]
                ),
                "merchant_quarter": Location(
                    name="Merchant Quarter",
                    description="Wealthy district with shops",
                    location_type="commercial",
                    connected_to=["market"]
                ),
            }

    def tick(self) -> Dict[str, str]:
        """
        Advance world simulation by one tick
        Returns dict of events that occurred
        """
        events = {}

        # 1. Advance time
        self.time_engine.advance(1)
        events["time"] = self.time_engine.get_time_string()

        # 2. Update weather
        self.weather_engine.update()
        events["weather"] = self.weather_engine.get_description()

        # 3. Increment tick counter
        self.tick_count += 1

        return events

    def get_world_status(self) -> str:
        """Get current world status"""
        lines = [
            "🌍 WORLD STATUS",
            "=" * 50,
            f"⏰ {self.time_engine.get_time_string()}",
            f"{self.weather_engine.get_description()}",
            f"🔄 Tick: {self.tick_count}",
            "",
            "📍 LOCATIONS:",
        ]

        for loc_name, location in self.locations.items():
            npcs = location.get_present_npcs()
            npc_str = f" [{', '.join(npcs)}]" if npcs else ""
            lines.append(f"  • {location.name}{npc_str}")

        return "\n".join(lines)

    def npc_at_location(self, npc_name: str, location_name: str):
        """Register NPC at a location"""
        # Remove from all locations first
        for loc in self.locations.values():
            loc.remove_npc(npc_name)

        # Add to new location
        if location_name in self.locations:
            self.locations[location_name].add_npc(npc_name)

    def get_npcs_at_location(self, location_name: str) -> List[str]:
        """Get NPCs at a specific location"""
        if location_name in self.locations:
            return self.locations[location_name].get_present_npcs()
        return []
