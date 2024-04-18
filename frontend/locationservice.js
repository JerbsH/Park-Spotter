import * as Location from 'expo-location';
import * as TaskManager from 'expo-task-manager';

const GEOFENCE_TASK_NAME = 'GEOFENCE_TASK';
let firstVisit = false;

// Define the geofence coordinates and radius
// Karaportti 2: 60.224185, 24.758153
const geofence = {
    latitude: 60.224185,
    longitude: 24.758153,
    radius: 250, // 250m
};

// Check user's location, compare to geofence
const handleUserLocation = async (coords, onFirstVisit) => {
    // Check if the user's location is inside the geofence
    if (isInsideGeofence(coords, geofence) && firstVisit) {
        console.log("User is inside the specific area for the first time");
        firstVisit = false;
        onFirstVisit();
    } else if (isInsideGeofence(coords, geofence)) {
        console.log("User is inside the specific area")
    }
    else {
        console.log("User is outside the specific area");
        firstVisit = true;
    }
}

const handleUserLocationTask = async ({ data: { locations } }) => {
    locations.forEach((location) => {
        const isInsideGeofence = isInsideGeofence(location.coords, geofence);
        if (isInsideGeofence && firstVisit) {
            console.log("User is inside the specific area for the first time");
            firstVisit = false;
            onFirstVisit();
        }
        else if (isInsideGeofence) {
            console.log("User is inside the specific area");
        }
        else {
            console.log("User is outside the specific area");
            firstVisit = true;
        }
    });
}

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
    console.log("DISTANCE: " + distance);
    return distance;
};

const requestBackgroundLocationPermissionsWithTimeout = async (timeout) => {
    let timerId;
    const timeoutPromise = new Promise((resolve, reject) => {
        timerId = setTimeout(() => {
            clearTimeout(timerId);
            reject(new Error("Permission request timed out."));
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
        return "error";
    }
}

// Function to start background location tracking
export const startBackgroundLocationTracking = async (onFirstVisit) => {
    const { status: foregroundStatus } = await Location.requestForegroundPermissionsAsync();
    if (foregroundStatus === "granted") {

        // Request background permissions, timed for compability between all platforms
        const { status: backgroundStatus } = await requestBackgroundLocationPermissionsWithTimeout(10000);

        if (backgroundStatus === "granted") {
            // Background task
            TaskManager.defineTask(GEOFENCE_TASK_NAME, handleUserLocationTask);
            await Location.startLocationUpdatesAsync(GEOFENCE_TASK_NAME, {
                accuracy: Location.Accuracy.Balanced,
                onFirstVisit,
            });
        }

        // Foreground location tracker
        const locationSubscription = await Location.watchPositionAsync({
            accuracy: Location.Accuracy.Balanced,
            distanceInterval: 10,
            timeInterval: 1500,
        }, location => {
            handleUserLocation(location.coords, onFirstVisit);
        });
    }
};

// Function to stop background location tracking
export const stopBackgroundLocationTracking = async () => {
    await Location.stopLocationUpdatesAsync(GEOFENCE_TASK_NAME);
};
