import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';

export async function schedulePushNotification(spots, handicapSpots) {
  await Notifications.scheduleNotificationAsync({
    identifier: 'parkingSpotUpdate',
    content: {
      title: 'Karaportti 2 parkingspot update 🚗',
      body: `There are: ${spots} parkingspots free and: ${handicapSpots} handicap spots free`,
      data: {spots, handicapSpots},
    },
    trigger: null,
  });
  console.log('Push notification scheduled');
}

export async function registerForPushNotificationsAsync() {
  let token;
  if (Device.isDevice) {
    const {status: existingStatus} = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;
    if (existingStatus !== 'granted') {
      const {status} = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }
    if (finalStatus !== 'granted') {
      console.error('Failed to get push token for push notification!');
      return;
    }
    try {
      const devicePushToken = await Notifications.getDevicePushTokenAsync();
      token = devicePushToken.data;
      console.log('Device Push Token:', token);
    } catch (error) {
      console.error('Error fetching Device Push Token:', error);
    }
  } else {
    console.error('Must use physical device for Push Notifications');
  }
  if (!token) {
    console.error('Push token is undefined');
  }
  console.log('Registered for push notifications');
  return token;
}
