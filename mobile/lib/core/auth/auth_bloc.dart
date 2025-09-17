// mobile/lib/core/auth/auth_bloc.dart
/**
 * Auth Bloc: Manages JWT, consent state.
 * Persists token to SharedPreferences.
 * DPDP: Tracks consent for customer data.
 */
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_service.dart';

abstract class AuthEvent {}
class CheckAuthEvent extends AuthEvent {}
class LoginEvent extends AuthEvent {
  final String email;
  final String password;
  LoginEvent(this.email, this.password);
}
class GrantConsentEvent extends AuthEvent {
  final List<String> purposes;
  GrantConsentEvent(this.purposes);
}
class LogoutEvent extends AuthEvent {}

class AuthState {
  final String? token;
  final bool hasConsent;
  AuthState({this.token, this.hasConsent = false});
}

class AuthBloc extends Bloc<AuthEvent, AuthState> {
  AuthBloc() : super(AuthState()) {
    on<CheckAuthEvent>(_onCheckAuth);
    on<LoginEvent>(_onLogin);
    on<GrantConsentEvent>(_onGrantConsent);
    on<LogoutEvent>(_onLogout);
  }

  Future<void> _onCheckAuth(CheckAuthEvent event, Emitter<AuthState> emit) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('jwt_token');
    final hasConsent = prefs.getBool('hasConsent') ?? false;
    emit(AuthState(token: token, hasConsent: hasConsent));
  }

  Future<void> _onLogin(LoginEvent event, Emitter<AuthState> emit) async {
    final response = await ApiService.login(event.email, event.password);  // Extend ApiService
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('jwt_token', response['access_token']);
    emit(AuthState(token: response['access_token'], hasConsent: state.hasConsent));
  }

  Future<void> _onGrantConsent(GrantConsentEvent event, Emitter<AuthState> emit) async {
    await ApiService.grantConsent(event.purposes);  // POST /auth/consent
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('hasConsent', true);
    emit(AuthState(token: state.token, hasConsent: true));
  }

  Future<void> _onLogout(LogoutEvent event, Emitter<AuthState> emit) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('jwt_token');
    await prefs.remove('hasConsent');
    emit(AuthState());
  }
}