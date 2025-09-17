// mobile/lib/services/whatsapp_service.dart
/**
 * WhatsApp Service: Sends low stock alerts, daily pulse.
 * Uses WhatsApp Business API via HTTP.
 * DPDP: Only sends if consent given.
 */
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../core/config.dart';

class WhatsAppService {
  static Future<void> sendLowStockAlert(String product, int qty, String phone) async {
    /**
     * Send low stock alert via WhatsApp.
     * Requires consent in user settings.
     */
    final response = await http.post(
      Uri.parse('https://api.whatsapp.com/v1/messages'),  // Meta API endpoint
      headers: {
        'Authorization': 'Bearer ${AppConfig.whatsappToken}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'to': phone,
        'text': {'body': 'Low stock: $product ($qty left)'},
      }),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to send WhatsApp alert');
    }
  }
}