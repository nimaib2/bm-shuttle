# Shuttle Flutter App

A Flutter mobile application for managing groups, polls, and users through the Shuttle API.

## Features

### 🏠 Home Screen
- Clean, modern UI with card-based navigation
- Quick access to all main features
- Settings placeholder for future enhancements

### 👥 Groups Management
- View all groups from your Supabase database
- Create new groups with simple form
- Responsive list view with group avatars
- Error handling for API failures

### 📊 Polls Management
- Display all polls with event and open dates
- View poll details including group associations
- Future: Create and manage polls

### 👤 Users Management
- View all registered users
- Create new users with name and phone number
- User avatars with initials
- Full CRUD operations

## API Integration

The app connects to your Supabase API at:
```
https://yrqmrdfwqiihwlecisco.supabase.co/rest/v1
```

### Supported Endpoints:
- `/users` - User management
- `/groups` - Group management
- `/polls` - Poll viewing
- `/memberships` - User-group relationships
- `/poll-responses` - Poll submissions
- `/poll-series` - Poll series management

## Getting Started

### Prerequisites
- Flutter SDK installed
- iOS Simulator or Android Emulator (for testing)
- Active Supabase database

### Installation

1. Clone and navigate to the project:
   ```bash
   cd shuttle_flutter_app
   ```

2. Install dependencies:
   ```bash
   flutter pub get
   ```

3. Run the app:
   ```bash
   flutter run
   ```

## Project Structure

```
lib/
├── models/          # Data models for API entities
│   ├── user.dart
│   ├── group.dart
│   ├── poll.dart
│   └── ...
├── services/        # API service layer
│   └── api_service.dart
├── screens/         # UI screens
│   ├── home_screen.dart
│   ├── groups_screen.dart
│   ├── polls_screen.dart
│   └── users_screen.dart
└── main.dart        # App entry point
```

## Features in Development

- [ ] Authentication system
- [ ] Poll creation and management
- [ ] Real-time updates
- [ ] Push notifications
- [ ] Advanced poll analytics
- [ ] User profile management
- [ ] Group membership management

## API Configuration

To modify the API endpoint, update the `baseUrl` in `lib/services/api_service.dart`:

```dart
static const String baseUrl = 'https://your-supabase-url.supabase.co/rest/v1';
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
