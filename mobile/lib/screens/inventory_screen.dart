// mobile/lib/screens/inventory_screen.dart
/**
 * Inventory Screen: View/update stock, low stock alerts.
 * Offline: Uses LocalDb, syncs via SyncService.
 * Mobile-first: Simple list, filterable.
 */
import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../core/db/local_db.dart';
import '../core/sync/sync_service.dart';

class InventoryScreen extends StatefulWidget {
  @override
  _InventoryScreenState createState() => _InventoryScreenState();
}

class _InventoryScreenState extends State<InventoryScreen> {
  List<Map<String, dynamic>> _items = [];
  bool _isOffline = false;

  @override
  void initState() {
    super.initState();
    _loadInventory();
  }

  Future<void> _loadInventory() async {
    final connectivity = await Connectivity().checkConnectivity();
    setState(() => _isOffline = connectivity == ConnectivityResult.none);
    if (_isOffline) {
      final dbItems = await LocalDb.instance.getInventoryItems();  // Extend LocalDb
      setState(() => _items = dbItems);
    } else {
      final items = await ApiService.getInventoryItems();  // Extend ApiService
      setState(() => _items = items);
      await LocalDb.instance.updateInventory(items);  // Cache locally
    }
  }

  Future<void> _updateStock(String id, int newStock) async {
    if (_isOffline) {
      await LocalDb.instance.updateInventoryItem(id, newStock);
      await SyncService.queueInventoryUpdate(id, newStock);  // Extend SyncService
    } else {
      await ApiService.updateInventoryItem(id, newStock);  // Extend ApiService
    }
    _loadInventory();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Inventory')),
      body: ListView.builder(
        itemCount: _items.length,
        itemBuilder: (context, index) {
          final item = _items[index];
          return ListTile(
            title: Text(item['name']),
            subtitle: Text('Stock: ${item['stock']}'),
            trailing: item['stock'] < 5
                ? Icon(Icons.warning, color: Colors.red)
                : null,
            onTap: () => _showStockDialog(item['id'], item['stock']),
          );
        },
      ),
    );
  }

  void _showStockDialog(String id, int currentStock) {
    final controller = TextEditingController(text: currentStock.toString());
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Update Stock'),
        content: TextField(
          controller: controller,
          keyboardType: TextInputType.number,
          decoration: InputDecoration(labelText: 'New Stock'),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              _updateStock(id, int.parse(controller.text));
              Navigator.pop(context);
            },
            child: Text('Save'),
          ),
        ],
      ),
    );
  }
}