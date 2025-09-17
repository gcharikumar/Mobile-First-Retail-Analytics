// mobile/lib/core/sync/sync_service.dart
/**
 * Sync Service: Queues offline actions (bills), syncs on connect.
 * Uses LocalDb for storage, ApiService for sync.
 */
import 'package:connectivity_plus/connectivity_plus.dart';
import '../db/local_db.dart';
import '../services/api_service.dart';

class SyncService {
  static Future<void> queueBill(Map<String, dynamic> bill) async {
    await LocalDb.instance.insertBill(bill);
  }

  static Future<void> syncPendingBills() async {
    final connectivity = await Connectivity().checkConnectivity();
    if (connectivity == ConnectivityResult.none) return;
    
    final pendingBills = await LocalDb.instance.getPendingBills();
    for (var bill in pendingBills) {
      try {
        await ApiService.createBill(bill);
        await LocalDb.instance.clearPendingBills();
      } catch (e) {
        print('Sync failed: $e');  // Log to Sentry in prod
      }
    }
  }
}