// mobile/lib/core/db/local_db_extensions.dart
/**
 * Extensions to LocalDb for inventory, analytics caching.
 * Adds methods referenced in screens.
 */
import 'package:sqflite/sqflite.dart';
import 'local_db.dart';

extension LocalDbExtensions on LocalDb {
  Future<List<Map<String, dynamic>>> getInventoryItems() async {
    final db = await database;
    return await db.query('inventory_items');
  }

  Future<void> updateInventoryItem(String id, int stock) async {
    final db = await database;
    await db.update(
      'inventory_items',
      {'stock': stock},
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  Future<List<Map<String, dynamic>>> getTopProducts() async {
    final db = await database;
    return await db.query('top_products');  // Assume table created
  }

  Future<void> cacheTopProducts(List<dynamic> products) async {
    final db = await database;
    await db.execute('CREATE TABLE IF NOT EXISTS top_products (product TEXT, this_week INTEGER, last_week INTEGER)');
    await db.delete('top_products');
    for (var product in products) {
      await db.insert('top_products', product);
    }
  }

  Future<List<Map<String, dynamic>>> getProducts() async {
    final db = await database;
    return await db.query('products');  // Assume table for catalog
  }
}