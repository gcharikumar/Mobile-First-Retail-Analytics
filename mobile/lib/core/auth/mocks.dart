// mobile/lib/core/auth/mocks.dart
/**
 * Mockito mocks for testing.
 * Used in pos_test.dart, extendable for other screens.
 */
import 'package:mockito/annotations.dart';
import '../services/api_service.dart';
import '../core/db/local_db.dart';

@GenerateMocks([ApiService, LocalDb])
void main() {}