import * as Location from 'expo-location';
import * as TaskManager from 'expo-task-manager';

const GEOFENCE_TASK_NAME = 'GEOFENCE_TASK';

// Define the geofence coordinates and radius
const geofence = {
    latitude: 60.2135,
    longitude: 24.8842,
    radius: 1000, // 1km
};

TaskManager.defineTask(GEOFENCE_TASK_NAME, async ({ data, error }) => {
    if (error) {
        console.error('Background location task error:', error.message);
        return;
    }

    if (data) {
        console.log(data);
        const { locations } = data;
        for (const location of locations) {
            const { coords } = location;
            // Check if the user's location is inside the geofence
            if (isInsideGeofence(coords, geofence)) {
                // Trigger your functionality here
                console.log('User is inside the specific area');
                // Call your specific function here
            } else {
                console.log('User is outside the specific area');
            }
        }
    }
    console.log("LOCATION");
});

// Function to check if the user's location is inside the geofence
const isInsideGeofence = (userCoords, geofence) => {
    const distance = calculateDistance(userCoords.latitude, userCoords.longitude, geofence.latitude, geofence.longitude);
    return distance <= geofence.radius;
};

const calculateDistance = (lat1, lon1, lat2, lon2) => {
    // Convert from degrees to radean
    const lat1Rad = lat1 * Math.PI / 180;
    const lon1Rad = lon1 * Math.PI / 180;
    const lat2Rad = lat2 * Math.PI / 180;
    const lon2Rad = lon2 * Math.PI / 180;

    // Calculate differences in coordinates
    const deltaX = lon2Rad - lon1Rad;
    const deltaY = lat2Rad - lat1Rad;

    // Calculate distance using Pythagorean theorem
    const distance = Math.sqrt(deltaX ** 2 + deltaY ** 2) * 6371e3; // Earth's radius in meters

    return distance;
};

const requestBackgroundLocationPermissionsWithTimeout = async (timeout) => {
    let timerId;
    const timeoutPromise = new Promise((resolve, reject) => {
        timerId = setTimeout(() => {
            clearTimeout(timerId);
            reject(new Error("Permission request timed out"));
        }, timeout);
    });

    const permissionsPromise = Location.requestBackgroundPermissionsAsync();

    try {
        await Promise.race([permissionsPromise, timeoutPromise]);
        clearTimeout(timerId);
        const { status } = await permissionsPromise;
        return status;
    } catch (error) {
        console.error("Error requesting background location permissions:", error);
        return null;
    }
}

// Function to start background location tracking
export async function startBackgroundLocationTracking() {
    const { status: foregroundStatus } = await Location.requestForegroundPermissionsAsync();
    if (foregroundStatus === 'granted') {
        console.log("[GEO] Foreground location permissions granted.");
        const { status: backgroundStatus } = await requestBackgroundLocationPermissionsWithTimeout(5000);
        if (backgroundStatus === 'granted') {
            console.log("[GEO] Background location permissions granted.");
            await Location.startLocationUpdatesAsync(GEOFENCE_TASK_NAME, {
                accuracy: Location.Accuracy.Balanced,
            });
        } else {
            console.log("[GEO] Background location permissions denied.");
        }
    } else {
        console.log("[GEO] Foreground location permissions denied.");
    }
};

// Function to stop background location tracking
export const stopBackgroundLocationTracking = async () => {
    await Location.stopLocationUpdatesAsync(GEOFENCE_TASK_NAME);
    console.log('Background location tracking stopped');
};
