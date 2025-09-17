// mobile/lib/screens/consent_screen.dart
/**
 * Consent Screen: DPDP compliance for data usage.
 * Required on first use if no consent.
 * Localized prompts.
 */
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../core/auth/auth_bloc.dart';

class ConsentScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Privacy Consent')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'We need your consent to process customer data for loyalty and analytics.',
              style: TextStyle(fontSize: 16),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                context.read<AuthBloc>().add(GrantConsentEvent(['loyalty', 'analytics']));
                Navigator.pushReplacementNamed(context, '/pos');
              },
              child: Text('Accept'),
            ),
            TextButton(
              onPressed: () {
                Navigator.pushReplacementNamed(context, '/pos');  // Allow without consent (minimal data)
              },
              child: Text('Deny'),
            ),
          ],
        ),
      ),
    );
  }
}