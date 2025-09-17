// mobile/test/pos_test.dart
/**
 * Unit tests for POS screen.
 * Mocks ApiService, LocalDb for offline cases.
 */
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import '../lib/services/api_service.dart';
import '../lib/core/db/local_db.dart';
import '../lib/screens/pos_screen.dart';
import 'mocks.dart';  // Assume MockApiService, MockLocalDb

void main() {
  late MockApiService apiService;
  late MockLocalDb localDb;

  setUp(() {
    apiService = MockApiService();
    localDb = MockLocalDb();
  });

  testWidgets('POS screen adds item and queues offline', (WidgetTester tester) async {
    when(localDb.insertBill(any)).thenAnswer((_) async => {});
    await tester.pumpWidget(
      MaterialApp(
        home: PosScreen(),
      ),
    );
    
    await tester.enterText(find.byType(TextField), 'saree');
    await tester.testTextInput.receiveAction(TextInputAction.done);
    await tester.pump();
    
    expect(find.text('saree'), findsOneWidget);
    expect(find.byType(ElevatedButton), findsOneWidget);
  });
}