import * as Location from 'expo-location'; // Import Location module
import {schedulePushNotification} from './notifications';

export const setupGeofencing = async () => {
  try {
    // Request foreground location permissions
    const {status: foregroundStatus} =
      await Location.requestForegroundPermissionsAsync();
    if (foregroundStatus !== 'granted') {
      console.error('Foreground location permission not granted');
      return;
    }

    // Request background location permissions
    const {status: backgroundStatus} =
      await Location.requestBackgroundPermissionsAsync();
    if (backgroundStatus !== 'granted') {
      console.error('Background location permission not granted');
      return;
    }

    // Get user's location
    const location = await Location.getCurrentPositionAsync({});
    console.log(location);

    // Define geofence parameters
    const geofence = {
      latitude: location.coords.latitude, // User's latitude
      longitude: location.coords.longitude, // User's longitude
      radius: 10, // Radius in meters
      notifyOnEnter: true,
      notifyOnExit: false,
    };

    // Start geofencing
    await Location.startGeofencingAsync('geofence', [geofence]);

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

    // Return a cleanup function
    return () => Location.stopGeofencingAsync('geofence');
  } catch (error) {
    console.error('Error setting up geofencing:', error);
  }
};
