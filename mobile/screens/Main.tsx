import { StatusBar } from 'expo-status-bar';
import { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TextInput, Platform } from 'react-native';
import ButtonRound from '../components/ButtonRound';
import {
  NavigationProp,
  ParamListBase,
  useNavigation,
} from '@react-navigation/native';
import useGetItem from '../hooks/UseGetItem';
import entries from '../asyncStorage';

export default function Main() {
  const [statusLogs, setStatusLogs] = useState<string>('');
  const [controllerLogs, setControllerLogs] = useState<string>('');
  const [isStatus, setIsStatus] = useState<boolean>(false);
  const [isStartStop, setIsStartStop] = useState<boolean>(false);
  const [lastChecked, setLastChecked] = useState<string>('');

  const navigation = useNavigation<NavigationProp<ParamListBase>>();
  const getItem = useGetItem();

  const fetchStatus = async () => {
    const timestamp = new Date().toLocaleTimeString();

    setLastChecked(timestamp);

    try {
      const url = await getItem(entries.URL);
      if (!url) return;
      const key = await getItem(entries.KEY);
      if (!key) return;

      const resp = await fetch(`${url}/status`, {
        headers: {
          'x-api-key': key,
        },
        method: 'GET',
      });

      const jsonData = await resp.json();
      if ('Container is not running' === jsonData.body) {
        setIsStatus(false);
      } else if (
        (jsonData.body as string).startsWith('Container is running using ip:')
      ) {
        setIsStatus(true);
      } else {
        setIsStatus(false);
      }

      setStatusLogs(JSON.stringify(jsonData));
    } catch (e) {
      console.error(e);
      if (e instanceof Error) {
        setStatusLogs(e.message);
      } else {
        setStatusLogs('An unknown error occurred');
      }
    }
  };

  const fetchStartStop = async (isStart: boolean = false) => {
    try {
      const url = await getItem(entries.URL);
      if (!url) return;
      const key = await getItem(entries.KEY);
      if (!key) return;

      const resp = await fetch(`${url}/container`, {
        headers: {
          'x-api-key': key,
          'Content-Type': 'application/json',
        },
        method: 'POST',
        body: JSON.stringify({
          Command: isStart ? 'Start' : 'Stop',
        }),
      });

      const jsonData = await resp.json();
      if ('Container stopped.' === jsonData.body) {
        setIsStartStop(false);
      } else if ('Container started.' === jsonData.body) {
        setIsStartStop(true);
      } else {
        setIsStartStop(false);
      }

      setControllerLogs(JSON.stringify(jsonData));
    } catch (e) {
      console.error(e);
      if (e instanceof Error) {
        setControllerLogs(e.message);
      } else {
        setControllerLogs('An unknown error occurred');
      }
    }
  };

  useEffect(() => {
    setLastChecked('Not checked yet');
  }, []);

  const navigateToSettings = () => {
    navigation.navigate('Settings');
  };

  return (
    <View style={styles.container}>
      <View style={styles.settings}>
        <ButtonRound
          iconName={'settings-outline'}
          onPress={navigateToSettings}
        />
      </View>

      {/* Controller Section */}
      <View style={styles.section}>
        <View style={styles.header}>
          <View style={styles.headerTitleContainer}>
            <Text style={styles.headerText}>API Controller</Text>
            <Text style={styles.subHeaderText}>
              {isStartStop
                ? 'Last used command is "Start"'
                : 'Last used command is "Stop"'}
            </Text>
          </View>
          <ButtonRound
            iconName={'flash-outline'}
            onPress={() => {
              fetchStartStop(true);
            }}
          />
          <ButtonRound
            iconName={'flash-off-outline'}
            onPress={() => {
              fetchStartStop(false);
            }}
          />
        </View>
        <Text style={styles.logLabel}>API Response Data</Text>
        <TextInput
          value={controllerLogs}
          multiline={true}
          style={styles.textInput}
          showSoftInputOnFocus={false}
        />
      </View>

      {/* Status Section */}
      <View style={styles.section}>
        <View style={styles.header}>
          <View style={styles.statusContainer}>
            <View style={styles.headerTitleContainer}>
              <Text style={styles.headerText}>Server Status</Text>
              <Text style={styles.subHeaderText}>
                Last checked: {lastChecked}
              </Text>
            </View>
            <View style={styles.statusIndicatorContainer}>
              <Text style={styles.statusText}>
                {isStatus ? 'ONLINE' : 'OFFLINE'}
              </Text>
              <View
                style={{
                  ...styles.indicator,
                  backgroundColor: isStatus ? '#66b266' : '#ff6666',
                  borderColor: isStatus ? '#004c00' : '#990000',
                }}
              />
            </View>
          </View>
          <ButtonRound iconName={'refresh'} onPress={fetchStatus} />
        </View>

        <Text style={styles.logLabel}>API Response Data</Text>
        <TextInput
          value={statusLogs}
          multiline={true}
          style={styles.textInput}
          showSoftInputOnFocus={false}
        />
      </View>

      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    paddingTop: Platform.OS === 'android' ? 25 : 0,
  },
  settings: {
    marginTop: 30,
    paddingRight: 10,
    marginBottom: 5,
    flexDirection: 'row',
    justifyContent: 'flex-end',
    alignItems: 'center',
    width: '95%',
  },
  headerText: {
    fontSize: 18,
    fontWeight: 'bold',
    fontFamily: 'Arial',
  },
  subHeaderText: {
    fontSize: 12,
    color: '#555',
    marginTop: 2,
  },
  headerTitleContainer: {
    flexDirection: 'column',
  },
  section: {
    width: '95%',
    padding: 10,
    marginTop: 5,
    marginBottom: 5,
    backgroundColor: '#b4f7ae',
    borderRadius: 20,
  },
  header: {
    width: '100%',
    marginTop: 5,
    marginBottom: 10,
    backgroundColor: '#b4f7ae',
    borderRadius: 10,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  statusContainer: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  statusIndicatorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusText: {
    fontSize: 14,
    fontWeight: 'bold',
    marginRight: 6,
  },
  indicator: {
    marginRight: 5,
    width: 14,
    height: 14,
    borderRadius: 7,
    borderWidth: 2,
  },
  logLabel: {
    fontWeight: '600',
    marginBottom: 5,
  },
  textInput: {
    height: 100,
    borderStyle: 'dashed',
    borderColor: '#000000',
    borderWidth: 2,
    borderRadius: 10,
    width: '100%',
    backgroundColor: '#e1f9df',
    padding: 8,
  },
});
