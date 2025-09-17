// mobile/lib/screens/dashboard_screen.dart
/**
 * Dashboard Screen: Shows top products, festival alerts.
 * Uses charts (charts_flutter) for visualization.
 * Offline: Caches data from LocalDb.
 */
import 'package:flutter/material.dart';
import 'package:charts_flutter/flutter.dart' as charts;
import '../services/api_service.dart';
import '../core/db/local_db.dart';

class DashboardScreen extends StatefulWidget {
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  List<dynamic> _topProducts = [];
  bool _isOffline = false;

  @override
  void initState() {
    super.initState();
    _loadDashboard();
  }

  Future<void> _loadDashboard() async {
    final connectivity = await Connectivity().checkConnectivity();
    setState(() => _isOffline = connectivity == ConnectivityResult.none);
    if (_isOffline) {
      final cached = await LocalDb.instance.getTopProducts();  // Extend LocalDb
      setState(() => _topProducts = cached);
    } else {
      final products = await ApiService.getTopProducts();
      setState(() => _topProducts = products);
      await LocalDb.instance.cacheTopProducts(products);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Dashboard')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Text('Top 5 Products', style: TextStyle(fontSize: 18)),
          ),
          Expanded(
            child: charts.BarChart(
              [
                charts.Series<dynamic, String>(
                  id: 'Sales',
                  data: _topProducts,
                  domainFn: (product, _) => product['product'],
                  measureFn: (product, _) => product['this_week'],
                  colorFn: (_, __) => charts.MaterialPalette.blue.shadeDefault,
                ),
              ],
              animate: true,
            ),
          ),
          if (_topProducts.isNotEmpty)
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                'Festival Alert: Navratri demand for silk sarees rising!',
                style: TextStyle(color: Colors.red),
              ),
            ),
        ],
      ),
    );
  }
}