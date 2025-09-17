# mobile/lib/main.dart

// mobile/lib/main.dart
/**
 * Flutter app entry: Sets up MaterialApp, localization, Bloc.
 * Initializes DB, connectivity, and auth.
 * Mobile-first: Optimized for 320-414px widths.
 */
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'core/db/local_db.dart';
import 'core/auth/auth_bloc.dart';
import 'screens/pos_screen.dart';
import 'screens/inventory_screen.dart';
import 'screens/dashboard_screen.dart';
import 'screens/consent_screen.dart';
import 'core/config.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await LocalDb.instance.init();  // Init SQflite
  final prefs = await SharedPreferences.getInstance();
  final initialRoute = prefs.getBool('hasConsent') == true ? '/pos' : '/consent';
  runApp(MyApp(initialRoute: initialRoute));
}

class MyApp extends StatelessWidget {
  final String initialRoute;
  MyApp({required this.initialRoute});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider(create: (_) => AuthBloc()..add(CheckAuthEvent())),
      ],
      child: MaterialApp(
        title: 'Retail Insights',
        theme: ThemeData(
          primarySwatch: Colors.blue,
          visualDensity: VisualDensity.adaptivePlatformDensity,
        ),
        supportedLocales: [
          Locale('en', 'US'),
          Locale('hi', 'IN'),  // Hindi
          Locale('ta', 'IN'),  // Tamil
          // Add Telugu, Bengali, Marathi, Kannada, Malayalam
        ],
        localizationsDelegates: [
          GlobalMaterialLocalizations.delegate,
          GlobalWidgetsLocalizations.delegate,
          GlobalCupertinoLocalizations.delegate,
        ],
        initialRoute: initialRoute,
        routes: {
          '/pos': (context) => PosScreen(),
          '/inventory': (context) => InventoryScreen(),
          '/dashboard': (context) => DashboardScreen(),
          '/consent': (context) => ConsentScreen(),
        },
      ),
    );
  }
}