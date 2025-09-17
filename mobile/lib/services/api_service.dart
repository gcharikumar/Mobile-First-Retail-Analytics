// mobile/lib/services/api_service.dart
/**
 * API Service: HTTP client for backend calls.
 * Handles JWT auth, offline queueing via sync service.
 * Base URL from config; error handling for DPDP consent.
 */
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';  // For token storage
import '../core/config.dart';  // AppConfig.baseUrl

class ApiService {
  static const String baseUrl = AppConfig.baseUrl;  // e.g., 'https://api.retailinsights.com/api/v1'
  static Future<String?> _getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('jwt_token');
  }

  static Future<http.Response> _request(String endpoint, {Map<String, dynamic>? body, String method = 'GET'}) async {
    final token = await _getToken();
    final headers = {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
    final uri = Uri.parse('$baseUrl$endpoint');
    if (method == 'POST') {
      return http.post(uri, headers: headers, body: jsonEncode(body));
    }
    // Add PUT/DELETE as needed
    return http.get(uri, headers: headers);
  }

  static Future<Map<String, dynamic>> createBill(Map<String, dynamic> billData) async {
    /**
     * Create bill: POST /pos/bills.
     * If offline, queue via SyncService.
     * DPDP: Include consent; throw if false and phone present.
     */
    if (billData['customer_phone'] != null && !billData['consent_given']) {
      throw Exception('Consent required for customer data');
    }
    try {
      final response = await _request('/pos/bills', body: billData, method: 'POST');
      if (response.statusCode == 200 || response.statusCode == 201) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to create bill: ${response.body}');
      }
    } catch (e) {
      // Offline fallback
      await SyncService.queueBill(billData);
      return {'status': 'queued_offline'};
    }
  }

  static Future<List<dynamic>> getTopProducts() async {
    /**
     * Fetch analytics: GET /analytics/top-products.
     * Cache locally if offline.
     */
    final response = await _request('/analytics/top-products');
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to fetch products');
  }
}

// In pubspec.yaml: http: ^1.2.2, shared_preferences: ^2.3.2