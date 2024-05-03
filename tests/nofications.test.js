import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import {
  schedulePushNotification,
  registerForPushNotificationsAsync,
} from '../frontend/notifications.js';

// Mock Notifications module
jest.mock('expo-notifications', () => ({
  scheduleNotificationAsync: jest.fn(),
  getPermissionsAsync: jest.fn(),
  requestPermissionsAsync: jest.fn(),
  getDevicePushTokenAsync: jest.fn(),
}));

// Mock Device module
jest.mock('expo-device', () => ({
  isDevice: true,
}));

describe('schedulePushNotification', () => {
  it('should schedule a push notification with correct content', async () => {
    const spots = 5;
    const handicapSpots = 3;

    await schedulePushNotification(spots, handicapSpots);

    expect(Notifications.scheduleNotificationAsync).toHaveBeenCalledWith({
      identifier: 'parkingSpotUpdate',
      content: {
        title: 'Karaportti 2 parkingspot update 🚗',
        body: `There are: ${spots} parkingspots free and: ${handicapSpots} handicap spots free`,
        data: {spots, handicapSpots},
      },
      trigger: null,
    });
    expect(console.log).toHaveBeenCalledWith('Push notification scheduled');
  });
});

describe('registerForPushNotificationsAsync', () => {
  it('should register for push notifications and return a token', async () => {
    Notifications.getPermissionsAsync.mockResolvedValueOnce({
      status: 'granted',
    });
    Notifications.getDevicePushTokenAsync.mockResolvedValueOnce({
      data: 'token123',
    });

    const token = await registerForPushNotificationsAsync();

    expect(token).toBe('token123');
    expect(console.log).toHaveBeenCalledWith(
      'Registered for push notifications',
    );
  });

  it('should handle the case when permissions are not granted', async () => {
    Notifications.getPermissionsAsync.mockResolvedValueOnce({status: 'denied'});

    const token = await registerForPushNotificationsAsync();

    expect(token).toBeUndefined();
    expect(console.error).toHaveBeenCalledWith(
      'Failed to get push token for push notification!',
    );
  });

  it('should handle the case when device is not available', async () => {
    Device.isDevice = false;

    await registerForPushNotificationsAsync();

    expect(console.error).toHaveBeenCalledWith(
      'Must use physical device for Push Notifications',
    );
  });

  it('should handle errors while fetching push token', async () => {
    Notifications.getPermissionsAsync.mockResolvedValueOnce({
      status: 'granted',
    });
    Notifications.getDevicePushTokenAsync.mockRejectedValueOnce(
      'Error fetching token',
    );

    await registerForPushNotificationsAsync();

    expect(console.error).toHaveBeenCalledWith(
      'Error fetching Device Push Token:',
      'Error fetching token',
    );
  });

  it('should handle undefined token', async () => {
    Notifications.getPermissionsAsync.mockResolvedValueOnce({
      status: 'granted',
    });
    Notifications.getDevicePushTokenAsync.mockResolvedValueOnce({});

    await registerForPushNotificationsAsync();

    expect(console.error).toHaveBeenCalledWith('Push token is undefined');
  });
});
