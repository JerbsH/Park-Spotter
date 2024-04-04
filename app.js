import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';

const App = () => {
  const [spots, setSpots] = useState(0);

  useEffect(() => {
    fetch('http://localhost:8000/free_spots')
      .then(response => response.json())
      .then(data => setSpots(data.free_spots))
      .catch(error => console.error(error));
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Parking Spot Availability</Text>
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