import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';

// Function to schedule a push notification with the given spots and handicapSpots
export async function schedulePushNotification(spots, handicapSpots) {
  // Scheduling a notification with Expo Notifications module
  await Notifications.scheduleNotificationAsync({
    identifier: 'parkingSpotUpdate',
    content: {
      title: 'Karaportti 2 parkingspot update 🚗',
      body: `There are: ${spots} parkingspots free and: ${handicapSpots} accessible spots free`,
      data: {spots, handicapSpots},
    },
    trigger: null, // Triggering the notification immediately
  });
}

// Function to register for push notifications asynchronously
export async function registerForPushNotificationsAsync() {
  let token;
  // Checking if the app is running on a physical device
  if (Device.isDevice) {
    // Checking the existing permission status for notifications
    const {status: existingStatus} = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;
    // Requesting permission if not granted already
    if (existingStatus !== 'granted') {
      const {status} = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }
    // Handling cases where permission is not granted
    if (finalStatus !== 'granted') {
      console.error('Failed to get push token for push notification!');
      return;
    }
    // Getting the device push token
    try {
      const devicePushToken = await Notifications.getDevicePushTokenAsync();
      token = devicePushToken.data;
    } catch (error) {
      console.error('Error fetching Device Push Token:', error);
    }
  } else {
    console.error('Must use physical device for Push Notifications');
  }
  // Handling cases where token is not received
  if (!token) {
    console.error('Push token is undefined');
  }
  return token;
}
