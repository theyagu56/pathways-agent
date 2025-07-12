import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String _baseUrl =
      String.fromEnvironment('API_URL', defaultValue: 'https://api.jeffandsons.us');

  Future<String> fetchRootMessage() async {
    final response = await http.get(Uri.parse('$_baseUrl/'));
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return data['message'] as String? ?? 'No message';
    } else {
      throw Exception('Failed to load message');
    }
  }

  Future<String> sendSymptoms(String symptoms) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/symptoms'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'symptoms': symptoms}),
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return data['message'] as String? ?? 'No response';
    } else {
      throw Exception('Failed to submit symptoms');
    }
  }
}
