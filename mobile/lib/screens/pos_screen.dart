// mobile/lib/screens/pos_screen.dart
/**
 * Mobile-First POS Screen: Line item capture, offline billing.
 * Uses Bloc for state, SQflite for local storage, sync on reconnect.
 * Minimal setup: Scan/add items via text/QR.
 * Localization: Use flutter_localizations.
 * Offline: Queue bills in local DB, sync via API service.
 * DPDP: Consent dialog on first use for customer data.
 */
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:sqflite/sqflite.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import '../core/db/local_db.dart';  // SQflite helper
import '../services/api_service.dart';
import '../blocs/pos_bloc.dart';

class PosScreen extends StatefulWidget {
  @override
  _PosScreenState createState() => _PosScreenState();
}

class _PosScreenState extends State<PosScreen> {
  final TextEditingController _productController = TextEditingController();
  final List<Map<String, dynamic>> _lineItems = [];
  Database? _localDb;
  bool _isOffline = false;

  @override
  void initState() {
    super.initState();
    _initDb();
    _checkConnectivity();
  }

  Future<void> _initDb() async {
    _localDb = await LocalDb.instance.database;  // Init SQflite
  }

  Future<void> _checkConnectivity() async {
    var connectivity = await Connectivity().checkConnectivity();
    setState(() => _isOffline = connectivity == ConnectivityResult.none);
  }

  Future<void> _addItem() async {
    if (_productController.text.isEmpty) return;
    // NLP unification: Call local service or API
    String unifiedName = await NlpService.unifyProduct(_productController.text);  // Fuzzy local
    setState(() {
      _lineItems.add({'name': unifiedName, 'qty': 1, 'price': 100.0});  // Default price
    });
    _productController.clear();
  }

  Future<void> _createBill() async {
    final bill = {'line_items': _lineItems, 'customer_phone': '', 'consent': false};
    if (_isOffline) {
      // Store locally
      await _localDb!.insert('pending_bills', bill);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Bill queued for sync')));
    } else {
      // API call
      await ApiService.createBill(bill);  // POST /pos/bills
    }
    setState(() => _lineItems.clear());
    // Trigger inventory update if online
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('POS Billing'), actions: [
        IconButton(
          icon: Icon(_isOffline ? Icons.wifi_off : Icons.wifi),
          onPressed: _checkConnectivity,
        )
      ]),
      body: Column(
        children: [
          // Consent check (DPDP)
          if (!context.read<AuthBloc>().state.hasConsent)
            AlertDialog(
              title: Text('Privacy Consent'),  // Localized: Localizations.of(context).of(MaterialApp.of(context).localizationsDelegate!)
              content: Text('We need consent to store customer phone for loyalty.'),
              actions: [
                TextButton(onPressed: () => Navigator.pop(context), child: Text('Deny')),
                ElevatedButton(onPressed: () {
                  context.read<AuthBloc>().add(GrantConsentEvent());
                  Navigator.pop(context);
                }, child: Text('Accept')),
              ],
            ),
          TextField(
            controller: _productController,
            decoration: InputDecoration(labelText: 'Product Name (e.g., saree)'),
            onSubmitted: (_) => _addItem(),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: _lineItems.length,
              itemBuilder: (context, index) => ListTile(
                title: Text(_lineItems[index]['name']),
                subtitle: Text('${_lineItems[index]['qty']} x ${_lineItems[index]['price']}'),
              ),
            ),
          ),
          ElevatedButton(onPressed: _createBill, child: Text('Checkout')),
        ],
      ),
    );
  }
}

// In pubspec.yaml: dependencies: flutter_bloc: ^8.1.3, sqflite: ^2.3.3, connectivity_plus: ^6.0.5, fuzzywuzzy: ^0.0.2 (for NLP)