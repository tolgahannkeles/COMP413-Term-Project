import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:flutter_map_marker_cluster/flutter_map_marker_cluster.dart';
import 'package:latlong2/latlong.dart';
import 'package:mobile_app/parking_data.dart';
import 'package:http/http.dart' as http;

class MapPage extends StatefulWidget {
  const MapPage({super.key});

  @override
  State<MapPage> createState() => _MapPageState();
}

class _MapPageState extends State<MapPage> {
  final LatLng _center = const LatLng(38.737886, 35.475344);
  final String mapUrl = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';
  List<Marker> _markerList = [];
  late MapController _mapController;

  @override
  void initState() {
    super.initState();
    _mapController = MapController(); // Initialize here
    getMarkers().then((value) => setState(() {}));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("IOT Project"),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              getMarkers().then((value) => setState(() {}));
            },
          ),
        ],
      ),
      body: FlutterMap(
        mapController: _mapController,
        options: MapOptions(
          initialCenter: _center,
        ),
        children: [
          TileLayer(
            urlTemplate: mapUrl,
            //tileBounds: _bounds,
          ),
          MarkerClusterLayerWidget(
            options: MarkerClusterLayerOptions(
              rotate: true,
              maxClusterRadius: 100,
              size: const Size(40, 40),
              markers: _markerList,
              builder: (BuildContext context, List<Marker> markers) {
                return Container(
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.black, width: 2),
                    shape: BoxShape.circle,
                    color: Colors.white,
                  ),
                  width: 40,
                  height: 40,
                  child: Center(
                    child: Text(markers.length.toString()),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Future<void> getMarkers() async {
    Uri? uri = Uri.tryParse(
        "https://firestore.googleapis.com/v1/projects/iot-project-db90a/databases/(default)/documents/gateway_data");
    if (uri != null) {
      http.Response response = await http.get(uri);
      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);

        // Extract documents
        final List<dynamic> documents = data['documents'] ?? [];

        // Parse ParkingData list
        List<ParkingData> parkingDataList = documents.map((doc) {
          final docId = doc['name'].toString().split('/').last;
          return ParkingData.fromJson(docId, doc['fields']);
        }).toList();

        // Convert ParkingData list to Marker list
        setState(() {
          _markerList = parkingDataList
              .map((parkingData) => Marker(
                    width: 40.0,
                    height: 40.0,
                    point:
                        LatLng(parkingData.latitude!, parkingData.longitude!),
                    child: Icon(
                      Icons.location_on,
                      color:
                          parkingData.status == 1 ? Colors.green : Colors.red,
                    ),
                  ))
              .toList();
        });
      } else {
        print('Error: ${response.statusCode}');
      }
    }
  }
}
