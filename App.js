// React Native code
import React, {useState, useEffect} from 'react';
import {View, Text, StyleSheet} from 'react-native';
import {LogBox} from 'react-native';
// testikommentttia
LogBox.ignoreLogs(['Warning: ...']); // Ignore log notification by message
LogBox.ignoreAllLogs(); // Ignore all log notifications

const App = () => {
  const [spots, setSpots] = useState(0);

  useEffect(() => {
    const fetchSpots = () => {
      fetch(`${process.env.REACT_APP_API_URL}`)
        .then((response) => response.json())
        .then((data) => {
          console.log('Data fetched successfully', data);
          setSpots(data.free_spots);
        })
        .catch((error) => {
          console.error('Error fetching data', error);
        });
    };
    fetchSpots(); // Fetch immediately on component mount
    const timerId = setInterval(fetchSpots, 10000);
    return () => clearInterval(timerId); // Clean up the timer
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>
        Parking Spot Availability at Karaportti 2:
      </Text>
      <Text style={styles.spots}>{spots}</Text>
      <Text style={styles.subtitle}>Available Spots</Text>
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
