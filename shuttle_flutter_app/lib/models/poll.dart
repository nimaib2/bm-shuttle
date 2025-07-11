class Poll {
  final int? id;
  final int pollSeriesId;
  final DateTime openDate;
  final int groupId;
  final DateTime eventDate;
  final int reservationOffset;

  Poll({
    this.id,
    required this.pollSeriesId,
    required this.openDate,
    required this.groupId,
    required this.eventDate,
    required this.reservationOffset,
  });

  factory Poll.fromJson(Map<String, dynamic> json) {
    return Poll(
      id: json['id'],
      pollSeriesId: json['poll_series_id'] ?? 0,
      openDate: DateTime.parse(json['open_date']),
      groupId: json['group_id'] ?? 0,
      eventDate: DateTime.parse(json['event_date']),
      reservationOffset: json['reservation_offset'] ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      if (id != null) 'id': id,
      'poll_series_id': pollSeriesId,
      'open_date': openDate.toIso8601String().split('T')[0],
      'group_id': groupId,
      'event_date': eventDate.toIso8601String().split('T')[0],
      'reservation_offset': reservationOffset,
    };
  }
} 