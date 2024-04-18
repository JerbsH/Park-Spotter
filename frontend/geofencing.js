import * as Location from 'expo-location';
import {schedulePushNotification} from './notifications';

export const setupGeofencing = async () => {
  // Request location permissions
  const {status} = await Location.requestForegroundPermissionsAsync();
  if (status !== 'granted') {
    console.error('Location permission not granted');
    return;
  }

  // Define geofence parameters
  const geofence = {
    latitude: 57.547, // Latitude of Karaportti 2
    longitude: 13.438, // Longitude of Karaportti 2
    radius: 10, // Radius in meters
    notifyOnEnter: true,
    notifyOnExit: false,
  };

  // Add geofence
  const geofenceId = await Location.startGeofencingAsync('geofence', [
    geofence,
  ]);

  // Listener for geofence events
  Location.addGeofencingEventListener(async ({region, action}) => {
    if (action === 'enter') {
      // Fetch the number of free spots and handicap spots
      const spotsResponse = await fetch(
        `${process.env.REACT_SERVER_URL}/free_spots`,
      );
      const spotsData = await spotsResponse.json();
      const spots = spotsData.free_spots;

      const handicapSpotsResponse = await fetch(
        `${process.env.REACT_PARKINGSPOTS_URL}/free_handicap_spots`,
      );
      const handicapSpotsData = await handicapSpotsResponse.json();
      const handicapSpots = handicapSpotsData.free_handicap_spots;

      // Trigger push notification
      await schedulePushNotification(spots, handicapSpots, action, geofence);
    }
  });

  // Cleanup function
  return () => Location.stopGeofencingAsync(geofenceId);
};
