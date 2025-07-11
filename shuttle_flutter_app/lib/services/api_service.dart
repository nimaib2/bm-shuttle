import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/user.dart';
import '../models/group.dart';
import '../models/membership.dart';
import '../models/poll.dart';
import '../models/poll_response.dart';
import '../models/poll_series.dart';

class ApiService {
  static const String baseUrl = 'https://yrqmrdfwqiihwlecisco.supabase.co/rest/v1';
  
  // Headers for Supabase requests
  static const Map<String, String> headers = {
    'Content-Type': 'application/json',
    'Prefer': 'return=representation',
  };

  // User endpoints
  static Future<List<User>> getUsers() async {
    final response = await http.get(Uri.parse('$baseUrl/users'), headers: headers);
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((user) => User.fromJson(user)).toList();
    } else {
      throw Exception('Failed to load users');
    }
  }

  static Future<User> createUser(User user) async {
    final response = await http.post(
      Uri.parse('$baseUrl/users'),
      headers: headers,
      body: json.encode(user.toJson()),
    );
    if (response.statusCode == 201) {
      final List<dynamic> data = json.decode(response.body);
      return User.fromJson(data.first);
    } else {
      throw Exception('Failed to create user');
    }
  }

  // Group endpoints
  static Future<List<Group>> getGroups() async {
    final response = await http.get(Uri.parse('$baseUrl/groups'), headers: headers);
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((group) => Group.fromJson(group)).toList();
    } else {
      throw Exception('Failed to load groups');
    }
  }

  static Future<Group> createGroup(Group group) async {
    final response = await http.post(
      Uri.parse('$baseUrl/groups'),
      headers: headers,
      body: json.encode(group.toJson()),
    );
    if (response.statusCode == 201) {
      final List<dynamic> data = json.decode(response.body);
      return Group.fromJson(data.first);
    } else {
      throw Exception('Failed to create group');
    }
  }

  // Membership endpoints
  static Future<List<Membership>> getMemberships() async {
    final response = await http.get(Uri.parse('$baseUrl/memberships'), headers: headers);
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((membership) => Membership.fromJson(membership)).toList();
    } else {
      throw Exception('Failed to load memberships');
    }
  }

  static Future<Membership> createMembership(Membership membership) async {
    final response = await http.post(
      Uri.parse('$baseUrl/memberships'),
      headers: headers,
      body: json.encode(membership.toJson()),
    );
    if (response.statusCode == 201) {
      final List<dynamic> data = json.decode(response.body);
      return Membership.fromJson(data.first);
    } else {
      throw Exception('Failed to create membership');
    }
  }

  // Poll endpoints
  static Future<List<Poll>> getPolls() async {
    final response = await http.get(Uri.parse('$baseUrl/polls'), headers: headers);
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((poll) => Poll.fromJson(poll)).toList();
    } else {
      throw Exception('Failed to load polls');
    }
  }

  static Future<Poll> createPoll(Poll poll) async {
    final response = await http.post(
      Uri.parse('$baseUrl/polls'),
      headers: headers,
      body: json.encode(poll.toJson()),
    );
    if (response.statusCode == 201) {
      final List<dynamic> data = json.decode(response.body);
      return Poll.fromJson(data.first);
    } else {
      throw Exception('Failed to create poll');
    }
  }

  // Poll Response endpoints
  static Future<List<PollResponse>> getPollResponses() async {
    final response = await http.get(Uri.parse('$baseUrl/poll-responses'), headers: headers);
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((response) => PollResponse.fromJson(response)).toList();
    } else {
      throw Exception('Failed to load poll responses');
    }
  }

  static Future<PollResponse> createPollResponse(PollResponse pollResponse) async {
    final response = await http.post(
      Uri.parse('$baseUrl/poll-responses'),
      headers: headers,
      body: json.encode(pollResponse.toJson()),
    );
    if (response.statusCode == 201) {
      final List<dynamic> data = json.decode(response.body);
      return PollResponse.fromJson(data.first);
    } else {
      throw Exception('Failed to create poll response');
    }
  }

  // Poll Series endpoints
  static Future<List<PollSeries>> getPollSeries() async {
    final response = await http.get(Uri.parse('$baseUrl/poll-series'), headers: headers);
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((series) => PollSeries.fromJson(series)).toList();
    } else {
      throw Exception('Failed to load poll series');
    }
  }

  static Future<PollSeries> createPollSeries(PollSeries pollSeries) async {
    final response = await http.post(
      Uri.parse('$baseUrl/poll-series'),
      headers: headers,
      body: json.encode(pollSeries.toJson()),
    );
    if (response.statusCode == 201) {
      final List<dynamic> data = json.decode(response.body);
      return PollSeries.fromJson(data.first);
    } else {
      throw Exception('Failed to create poll series');
    }
  }
} 