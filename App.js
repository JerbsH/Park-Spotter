// React Native code
import React, {useState, useEffect} from 'react';
import {View, Text, StyleSheet} from 'react-native';
import {LogBox} from 'react-native';

LogBox.ignoreLogs(['Warning: ...']); // Ignore log notification by message
LogBox.ignoreAllLogs(); // Ignore all log notifications

const App = () => {
  const [spots, setSpots] = useState(0);
  const [handicapSpots, setHandicapSpots] = useState(0);
  /**
   * testausta serveriä varten
   * ....
   * ....
   * ...
   */
  useEffect(() => {
    const fetchSpots = () => {
      fetch(`${process.env.REACT_PARKINGSPOTS_URL}`)
        .then((response) => response.text()) // Get response text
        .then((text) => {
          return JSON.parse(text); // Parse the text as JSON
        })
        .then((data) => {
          console.log('Data fetched successfully', data);
          setSpots(data.free_spots);
        })
        .catch((error) => {
          console.error('Error fetching data', error);
        });

      fetch(`${process.env.REACT_HANDICAP_PARKINGSPOTS_URL}`)
        .then((response) => response.text()) // Get response text
        .then((text) => {
          console.log('Raw response:', text);
          return JSON.parse(text); // Parse the text as JSON
        })
        .then((data) => {
          console.log('Data fetched successfully', data);
          setHandicapSpots(data.free_handicap_spots);
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
