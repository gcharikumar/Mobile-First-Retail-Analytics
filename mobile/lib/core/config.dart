// mobile/lib/core/config.dart
/**
 * App configuration: API base URL, env vars.
 * Loaded from .env via flutter_dotenv or hardcoded for simplicity.
 */
class AppConfig {
  static const String baseUrl = 'https://api.retailinsights.com/api/v1';  // Prod: Mumbai region
  static const String whatsappPhoneId = 'your_whatsapp_phone_id';
  static const String whatsappToken = 'your_whatsapp_token';
}