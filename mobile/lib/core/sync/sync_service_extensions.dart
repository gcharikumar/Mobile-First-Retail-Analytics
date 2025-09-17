// mobile/lib/core/sync/sync_service_extensions.dart
/**
 * Extensions to SyncService for inventory updates.
 * Queues updates for offline sync.
 */
import 'package:sqflite/sqflite.dart';
import '../db/local_db.dart';
import '../services/api_service.dart';

extension SyncServiceExtensions on SyncService {
  static Future<void> queueInventoryUpdate(String id, int stock) async {
    final db = await LocalDb.instance.database;
    await db.insert(
      'pending_inventory_updates',
      {'id': id, 'stock': stock, 'created_at': DateTime.now().toIso8601String()},
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  static Future<void> syncPendingInventoryUpdates() async {
    final connectivity = await Connectivity().checkConnectivity();
    if (connectivity == ConnectivityResult.none) return;
    
    final db = await LocalDb.instance.database;
    final updates = await db.query('pending_inventory_updates');
    for (var update in updates) {
      try {
        await ApiService.updateInventoryItem(update['id'], update['stock']);
        await db.delete('pending_inventory_updates', where: 'id = ?', whereArgs: [update['id']]);
      } catch (e) {
        print('Sync failed: $e');
      }
    }
  }
}