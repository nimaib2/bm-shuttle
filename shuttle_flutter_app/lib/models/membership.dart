class Membership {
  final int? id;
  final int groupId;
  final int userId;
  final String role;

  Membership({
    this.id,
    required this.groupId,
    required this.userId,
    required this.role,
  });

  factory Membership.fromJson(Map<String, dynamic> json) {
    return Membership(
      id: json['id'],
      groupId: json['group_id'] ?? 0,
      userId: json['user_id'] ?? 0,
      role: json['role'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      if (id != null) 'id': id,
      'group_id': groupId,
      'user_id': userId,
      'role': role,
    };
  }
} 