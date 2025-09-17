// mobile/lib/core/db/local_db.dart
/**
 * Local DB: SQflite for offline storage (bills, inventory).
 * Schema mirrors backend models (bills, inventory_items).
 */
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class LocalDb {
  static final LocalDb instance = LocalDb._init();
  static Database? _database;

  LocalDb._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('retail.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);
    
    return await openDatabase(
      path,
      version: 1,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE pending_bills (
            id TEXT PRIMARY KEY,
            line_items TEXT,
            customer_phone TEXT,
            total_amount REAL,
            created_at TEXT
          )
        ''');
        await db.execute('''
          CREATE TABLE inventory_items (
            id TEXT PRIMARY KEY,
            name TEXT,
            stock INTEGER,
            price REAL
          )
        ''');
      },
    );
  }

  Future<void> insertBill(Map<String, dynamic> bill) async {
    final db = await database;
    await db.insert('pending_bills', bill, conflictAlgorithm: ConflictAlgorithm.replace);
  }

  Future<List<Map<String, dynamic>>> getPendingBills() async {
    final db = await database;
    return await db.query('pending_bills');
  }

  Future<void> clearPendingBills() async {
    final db = await database;
    await db.delete('pending_bills');
  }
}