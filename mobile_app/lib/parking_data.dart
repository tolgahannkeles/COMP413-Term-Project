class ParkingData {
  final String? id;
  final int? status;
  final double? distance;
  final double? latitude;
  final double? longitude;

  // Constructor
  ParkingData({
    this.id,
    this.status,
    this.distance,
    this.latitude,
    this.longitude,
  });

  // Factory constructor to create an instance from a JSON map
  factory ParkingData.fromJson(String id, Map<String, dynamic> json) {
    return ParkingData(
      id: id,
      status: int.tryParse(json['status']?['integerValue'] ?? ''),
      distance: json['distance']?['doubleValue']?.toDouble(),
      latitude: json['latitude']?['doubleValue']?.toDouble(),
      longitude: json['longitude']?['doubleValue']?.toDouble(),
    );
  }

  // Method to convert an instance to a JSON map
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'status': status,
      'distance': distance,
      'latitude': latitude,
      'longitude': longitude,
    };
  }
}
