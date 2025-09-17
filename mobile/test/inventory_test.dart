// mobile/test/inventory_test.dart
/**
 * Unit tests for Inventory screen.
 * Mocks ApiService, LocalDb.
 */
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import '../lib/screens/inventory_screen.dart';
import '../lib/core/auth/mocks.dart';

void main() {
  late MockApiService apiService;
  late MockLocalDb localDb;

  setUp(() {
    apiService = MockApiService();
    localDb = MockLocalDb();
  });

  testWidgets('Inventory screen loads items', (WidgetTester tester) async {
    when(localDb.getInventoryItems()).thenAnswer((_) async => [
      {'id': '1', 'name': 'saree', 'stock': 10}
    ]);
    await tester.pumpWidget(
      MaterialApp(
        home: InventoryScreen(),
      ),
    );
    await tester.pump();
    
    expect(find.text('saree'), findsOneWidget);
    expect(find.text('Stock: 10'), findsOneWidget);
  });
}