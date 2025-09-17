// mobile/lib/core/localization/localization.dart
/**
 * Localization Setup: Loads translations for UI.
 * Supports Hindi, Tamil, etc. via ARB files.
 */
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart';

// Placeholder: Use ARB files in `lib/l10n/` (e.g., app_en.arb, app_hi.arb)
class AppLocalizations {
  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  static AppLocalizations of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations)!;
  }

  String get appTitle => Intl.message('Retail Insights', name: 'appTitle');
  String get posButton => Intl.message('Checkout', name: 'posButton');
  // Add more: lowStockAlert, consentPrompt, etc.
}

class _AppLocalizationsDelegate extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) => ['en', 'hi', 'ta'].contains(locale.languageCode);

  @override
  Future<AppLocalizations> load(Locale locale) async {
    Intl.defaultLocale = locale.languageCode;
    return AppLocalizations();
  }

  @override
  bool shouldReload(covariant LocalizationsDelegate<AppLocalizations> old) => false;
}