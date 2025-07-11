import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const ShuttleApp());
}

class ShuttleApp extends StatelessWidget {
  const ShuttleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Shuttle',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}
