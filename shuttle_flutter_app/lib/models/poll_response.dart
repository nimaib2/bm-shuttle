class PollResponse {
  final int? id;
  final int userId;
  final int pollId;
  final String response;
  final DateTime submissionDate;

  PollResponse({
    this.id,
    required this.userId,
    required this.pollId,
    required this.response,
    required this.submissionDate,
  });

  factory PollResponse.fromJson(Map<String, dynamic> json) {
    return PollResponse(
      id: json['id'],
      userId: json['user_id'] ?? 0,
      pollId: json['poll_id'] ?? 0,
      response: json['response'] ?? '',
      submissionDate: DateTime.parse(json['submission_date']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      if (id != null) 'id': id,
      'user_id': userId,
      'poll_id': pollId,
      'response': response,
      'submission_date': submissionDate.toIso8601String().split('T')[0],
    };
  }
} 