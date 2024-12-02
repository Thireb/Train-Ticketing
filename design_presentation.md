# CTA Ticketing System Design Documentation

## 1. System Functionality

### Zone-Based Structure
- **Three Main Zones**:
  - Central Zone
  - Midtown Zone
  - Downtown Zone
- **Implementation**:
```python
zone_map = {
    "Central": {
        "Centrala": ["Rede", "Ninia", "Bylyn", "Frestin", "Lomil", "Yaen", "Jaund", "Tallan"],
        "Frestin": ["Soth"]
    },
    "Midtown": { /* stations */ },
    "Downtown": { /* stations */ }
}
```

### Fare Calculation System
- **Traveler Categories**:
```python
FARES = {
    'adult': 2105,    # cents per zone
    'child': 1410,    # cents per zone
    'senior': 1025,   # cents per zone
    'student': 1750,  # cents per zone
}
```
- Zone-based pricing
- Multi-traveler support
- Automatic zone calculation

### Station Management
- Hierarchical station structure
- Connected stations tracking
- Zone assignment system

## 2. User Interface Design

### Main Interface Components
```html
<!-- Key UI Elements -->
<div class="zone-section">
    <div class="zone-title">
        <!-- Zone Headers -->
    </div>
    <div class="station-connections">
        <!-- Station Lists -->
    </div>
</div>

<div class="form-section">
    <!-- Ticket Booking Form -->
</div>

<div class="ticket">
    <!-- Ticket Display -->
</div>
```

### Visual Design Elements
- Clean, minimalist layout
- Color-coded zones
- Intuitive navigation
- Responsive design
- Clear fare breakdown

### User Flow
1. Select departure station
2. Select destination station
3. Input traveler counts
4. View fare calculation
5. Generate ticket

## 3. Design Justification

### Functionality Decisions

#### 1. Zone-Based Structure
- **Decision**: Implemented hierarchical zone mapping
- **Justification**:
  - Easier maintenance
  - Flexible station management
  - Efficient zone calculations
  ```python
  def calculate_zones_traveled(start_station: str, end_station: str) -> int:
      zone_order = ['Central', 'Midtown', 'Downtown']
      start_zone = get_station_zone(start_station)
      end_zone = get_station_zone(end_station)
      return abs(zone_order.index(end_zone) - zone_order.index(start_zone)) + 1
  ```

#### 2. Fare Categories
- **Decision**: Implemented multiple traveler types
- **Justification**:
  - Supports diverse user base
  - Flexible pricing structure
  - Easy to modify rates

#### 3. Station Connections
- **Decision**: Used nested dictionary structure
- **Justification**:
  - Represents real-world connections
  - Efficient pathfinding
  - Easy to update

### UI Design Decisions

#### 1. Layout Structure
- **Decision**: Three-section layout (Zones, Form, Ticket)
- **Justification**:
  - Logical user flow
  - Clear visual hierarchy
  - Minimizes user errors

#### 2. Styling Choices
```css
.zone-section {
    margin: 20px 0;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.ticket {
    margin-top: 30px;
    padding: 20px;
    border: 2px solid #000;
    border-radius: 5px;
    background-color: #f9f9f9;
}
```
- **Justification**:
  - High contrast for readability
  - Consistent visual language
  - Clear section separation

#### 3. Interactive Elements
- **Decision**: Real-time fare calculation
- **Justification**:
  - Immediate user feedback
  - Reduces user confusion
  - Prevents input errors

## 4. Future Enhancements

### Planned Features
1. Mobile responsiveness
2. Real-time updates
3. Multi-language support
4. Accessibility improvements

### Technical Improvements
1. Caching system
2. Performance optimization
3. Enhanced error handling
4. Additional payment methods
