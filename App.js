import {useState, useEffect} from 'react';
import {View, Text, StyleSheet} from 'react-native';
import {LogBox} from 'react-native';
import * as Notifications from 'expo-notifications';
import {initializeApp} from 'firebase/app';
import * as BackgroundFetch from 'expo-background-fetch';
import * as TaskManager from 'expo-task-manager';
import {firebaseConfig} from './frontend/config';
import {
  schedulePushNotification,
  registerForPushNotificationsAsync,
} from './frontend/notifications';
import {
  startBackgroundLocationTracking,
  stopBackgroundLocationTracking,
} from './frontend/locationservice';

LogBox.ignoreLogs(['Warning: ...']); // Ignore log notification by message
LogBox.ignoreAllLogs(); // Ignore all log notifications

initializeApp(firebaseConfig);

const App = () => {
  const [spots, setSpots] = useState(0);
  const [handicapSpots, setHandicapSpots] = useState(0);
  const [isInside, setIsInside] = useState(false);

  useEffect(() => {
    const registerToken = async () => {
      const expoPushToken = await registerForPushNotificationsAsync();

      fetch(`${process.env.REACT_SERVER_URL}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token: expoPushToken,
        }),
      });
    };

    registerToken();
  }, []);

  useEffect(() => {
    const onFirstVisit = async () => {
      console.log('Trigger push notification');
      await fetchSpots();
    };
    startBackgroundLocationTracking(onFirstVisit);

    return () => {
      stopBackgroundLocationTracking();
    };
  }, []);

  const fetchSpots = async () => {
    let spots = 0;
    let handicapSpots = 0;

    await fetch(`${process.env.REACT_PARKINGSPOTS_URL}`)
      .then((response) => response.text()) // Get response text
      .then((text) => {
        return JSON.parse(text); // Parse the text as JSON
      })
      .then((data) => {
        console.log('Data fetched successfully', data);
        spots = data.free_spots;
      })
      .catch((error) => {
        console.error('Error fetching data', error);
      });

    await fetch(`${process.env.REACT_HANDICAP_PARKINGSPOTS_URL}`)
      .then((response) => response.text()) // Get response text
      .then((text) => {
        return JSON.parse(text); // Parse the text as JSON
      })
      .then((data) => {
        console.log('Data fetched successfully', data);
        handicapSpots = data.free_handicap_spots;
      })
      .catch((error) => {
        console.error('Error fetching data', error);
      });

    setSpots(spots);
    setHandicapSpots(handicapSpots);

    if (isInside) {
      await schedulePushNotification(spots, handicapSpots);
    }
  };

  useEffect(() => {
    fetchSpots();
    // Register the background fetch task on component mount
    BackgroundFetch.registerTaskAsync(BACKGROUND_FETCH_TASK, {
      minimumInterval: 1, // 1 seconds
    });
    console.log('Background fetch task registered');
    // Fetch every 10 seconds
    const intervalId = setInterval(fetchSpots, 10000);

    // Clear interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  useEffect(() => {
    const onFirstVisit = () => {
      fetchSpots();
    };

    const onLocationChange = (isInsideGeofence) => {
      setIsInside(isInsideGeofence);
    };

    startBackgroundLocationTracking(onFirstVisit, onLocationChange);

    return () => {
      stopBackgroundLocationTracking();
    };
  }, []);

  useEffect(() => {
    const subscription = Notifications.addNotificationReceivedListener(
      (notification) => {
        console.log(notification);
      },
    );
    return () => subscription.remove();
  }, []);

  const BACKGROUND_FETCH_TASK = 'background-fetch';

  TaskManager.defineTask(BACKGROUND_FETCH_TASK, async () => {
    const now = Date.now();
    console.log(
      `Got background fetch call at date: ${new Date(now).toISOString()}`,
    );
    try {
      await fetchSpots();

      console.log('Background fetch task completed successfully');
      return BackgroundFetch.BackgroundFetchResult.NewData;
    } catch (err) {
      console.error('Background fetch task failed:', err);
      return BackgroundFetch.BackgroundFetchResult.Failed;
    }
  });

  return (
    <View style={styles.container}>
      <Text style={styles.title}>
        Parking Spot Availability at Karaportti 2:
      </Text>
      <Text style={styles.spots}>{spots}</Text>
      <Text style={styles.subtitle}>Available Spots</Text>
      <Text style={styles.spots}>{handicapSpots}</Text>
      <Text style={styles.subtitle}>Available Handicap Spots</Text>
    </View>
  );
};
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5FCFF',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 30,
    textAlign: 'center',
    margin: 10,
  },
  spots: {
    fontSize: 80,
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 20,
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
});

export default App;
