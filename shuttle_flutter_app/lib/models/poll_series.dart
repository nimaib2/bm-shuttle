class PollSeries {
  final int? id;
  final DateTime startDate;
  final DateTime endDate;
  final String title;
  final int groupId;
  final String frequency;
  final int playOffset;
  final int reservationOffset;

  PollSeries({
    this.id,
    required this.startDate,
    required this.endDate,
    required this.title,
    required this.groupId,
    required this.frequency,
    required this.playOffset,
    required this.reservationOffset,
  });

  factory PollSeries.fromJson(Map<String, dynamic> json) {
    return PollSeries(
      id: json['id'],
      startDate: DateTime.parse(json['start_date']),
      endDate: DateTime.parse(json['end_date']),
      title: json['title'] ?? '',
      groupId: json['group_id'] ?? 0,
      frequency: json['frequency'] ?? '',
      playOffset: json['play_offset'] ?? 0,
      reservationOffset: json['reservation_offset'] ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      if (id != null) 'id': id,
      'start_date': startDate.toIso8601String().split('T')[0],
      'end_date': endDate.toIso8601String().split('T')[0],
      'title': title,
      'group_id': groupId,
      'frequency': frequency,
      'play_offset': playOffset,
      'reservation_offset': reservationOffset,
    };
  }
} 