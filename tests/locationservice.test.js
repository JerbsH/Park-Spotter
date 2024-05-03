import {
  calculateDistance,
  isInsideGeofence,
  handleUserLocation,
  handleUserLocationTask,
  geofence,
} from './locationservice';

// Mock the schedulePushNotification function
jest.mock('../frontend/notifications.js', () => ({
  schedulePushNotification: jest.fn(),
}));

describe('Location Service', () => {
  describe('calculateDistance', () => {
    it('should correctly calculate the distance between two points', () => {
      const lat1 = 60.224185;
      const lon1 = 24.758153;
      const lat2 = 60.224185;
      const lon2 = 24.758153;
      const distance = calculateDistance(lat1, lon1, lat2, lon2);
      expect(distance).toBe(0);
    });
  });

  describe('isInsideGeofence', () => {
    it('should return true if the user is inside the geofence', () => {
      const userCoords = {
        latitude: 60.224185,
        longitude: 24.758153,
      };
      const isInside = isInsideGeofence(userCoords, geofence);
      expect(isInside).toBe(true);
    });

    it('should return false if the user is outside the geofence', () => {
      const userCoords = {
        latitude: 60.224186,
        longitude: 24.758154,
      };
      const isInside = isInsideGeofence(userCoords, geofence);
      expect(isInside).toBe(false);
    });
  });

  describe('handleUserLocation', () => {
    it('should handle user location inside the geofence', async () => {
      const coords = {
        latitude: 60.224185,
        longitude: 24.758153,
      };
      const onFirstVisit = jest.fn();
      const setIsInside = jest.fn();
      await handleUserLocation(coords, onFirstVisit, setIsInside);
      expect(setIsInside).toHaveBeenCalledWith(true);
      expect(onFirstVisit).toHaveBeenCalled();
      expect(
        require('../frontend/notifications.js').schedulePushNotification,
      ).toHaveBeenCalled();
    });

    it('should handle user location outside the geofence', async () => {
      const coords = {
        latitude: 60.224186,
        longitude: 24.758154,
      };
      const onFirstVisit = jest.fn();
      const setIsInside = jest.fn();
      await handleUserLocation(coords, onFirstVisit, setIsInside);
      expect(setIsInside).toHaveBeenCalledWith(false);
      expect(
        require('../frontend/notifications.js').schedulePushNotification,
      ).toHaveBeenCalled();
    });
  });

  describe('handleUserLocationTask', () => {
    it('should handle user location task inside the geofence', async () => {
      const data = {
        locations: [
          {
            coords: {
              latitude: 60.224185,
              longitude: 24.758153,
            },
          },
        ],
      };
      const onFirstVisit = jest.fn();
      const setIsInside = jest.fn();
      await handleUserLocationTask(data, onFirstVisit, setIsInside);
      expect(setIsInside).toHaveBeenCalledWith(true);
      expect(onFirstVisit).toHaveBeenCalled();
      expect(
        require('../frontend/notifications.js').schedulePushNotification,
      ).toHaveBeenCalled();
    });

    it('should handle user location task outside the geofence', async () => {
      const data = {
        locations: [
          {
            coords: {
              latitude: 60.224186,
              longitude: 24.758154,
            },
          },
        ],
      };
      const onFirstVisit = jest.fn();
      const setIsInside = jest.fn();
      await handleUserLocationTask(data, onFirstVisit, setIsInside);
      expect(setIsInside).toHaveBeenCalledWith(false);
      expect(
        require('../frontend/notifications.js').schedulePushNotification,
      ).toHaveBeenCalled();
    });
  });
});
