import { StatusBar } from 'expo-status-bar';
import { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  Platform,
  TouchableOpacity,
} from 'react-native';
import ButtonRound from './components/ButtonRound';
import Toggle from './components/Toggle';

export default function App() {
  const [statusLogs, setStatusLogs] = useState<string>('');
  const [controllerLogs, setControllerLogs] = useState<string>('');
  const [isStatus, setIsStatus] = useState<boolean>(false);
  const [isStartServer, setIsStartServer] = useState<boolean>(false);
  const [lastChecked, setLastChecked] = useState<string>('');
  const [serverIP, setServerIP] = useState<string>('');

  const fetchStatus = async () => {
    const timestamp = new Date().toLocaleTimeString();
    setLastChecked(timestamp);
  };

  useEffect(() => {
    setLastChecked('Not checked yet');
  }, []);

  return (
    <View style={styles.container}>
      <View style={styles.settings}>
        <ButtonRound iconName={'settings-outline'} onPress={() => {}} />
      </View>

      {/* Controller Section */}
      <View style={styles.section}>
        <View style={styles.header}>
          <View style={styles.headerTitleContainer}>
            <Text style={styles.headerText}>API Controller</Text>
            <Text style={styles.subHeaderText}>
              {isStartServer
                ? 'Server is set to running'
                : 'Server is set to stop'}
            </Text>
          </View>
          <Toggle
            value={isStartServer}
            onToggle={() => {
              setIsStartServer(!isStartServer);
            }}
          />
        </View>
        <Text style={styles.logLabel}>API Response Data</Text>
        <TextInput
          value={controllerLogs}
          multiline={true}
          editable={false}
          style={styles.textInput}
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

        {isStatus && (
          <View style={styles.ipContainer}>
            <Text style={styles.ipLabel}>Server IP:</Text>
            <TouchableOpacity>
              <Text style={styles.ipAddress}>{serverIP}</Text>
            </TouchableOpacity>
          </View>
        )}

        <Text style={styles.logLabel}>API Response Data</Text>
        <TextInput
          value={statusLogs}
          multiline={true}
          editable={false}
          style={styles.textInput}
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
  ipContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#e1f9df',
    padding: 6,
    borderRadius: 8,
    marginBottom: 8,
  },
  ipLabel: {
    fontWeight: 'bold',
    marginRight: 5,
  },
  ipAddress: {
    color: '#0066cc',
    textDecorationLine: 'underline',
  },
});
