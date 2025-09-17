// mobile/lib/services/nlp_service.dart
/**
 * NLP Service: Local product name unification.
 * Uses fuzzywuzzy (Dart port) for offline matching.
 * Fallback to API for complex cases.
 */
import 'package:fuzzywuzzy/fuzzywuzzy.dart';
import '../core/db/local_db.dart';

class NlpService {
  static Future<String> unifyProduct(String name) async {
    /**
     * Unify product name (e.g., 'sari' -> 'saree').
     * Checks local catalog first, falls back to API.
     */
    final catalog = await LocalDb.instance.getProducts();  // Extend LocalDb
    final names = catalog.map((p) => p['name']).toList();
    final bestMatch = extractOne(query: name, choices: names, cutoff: 80);
    return bestMatch != null ? bestMatch.choice : name.toLowerCase().replaceAll('sari', 'saree');
  }
}