import { StatusBar } from 'expo-status-bar';
import { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TextInput, Platform } from 'react-native';
import ButtonRound from '../components/ButtonRound';
import {
  NavigationProp,
  ParamListBase,
  useNavigation,
} from '@react-navigation/core';
import useGetItem from '../hooks/UseGetItem';
import useSetItem from '../hooks/UseSetItem';
import entries from '../asyncStorage';

export default function Settings() {
  const [apiUrl, setApiUrl] = useState<string>('');
  const [apiKey, setApiKey] = useState<string>('');

  const [savedApiUrl, setSavedApiUrl] = useState<string>('-');
  const [savedApiKey, setSavedApiKey] = useState<string>('-');

  const navigation = useNavigation<NavigationProp<ParamListBase>>();

  const navigateToMain = () => {
    navigation.navigate('Main');
  };

  const getItem = useGetItem();
  const setItem = useSetItem();

  // Load on mount
  useEffect(() => {
    const loadSavedValues = async () => {
      try {
        const savedUrl = await getItem(entries.URL);
        const savedKey = await getItem(entries.KEY);

        if (savedUrl) {
          setSavedApiUrl(savedUrl);
        }

        if (savedKey) {
          setSavedApiKey(savedKey);
        }
      } catch (e) {
        console.error('Error loading saved values:', e);
      }
    };

    loadSavedValues();
  }, []);

  const saveUrl = async () => {
    try {
      await setItem(entries.URL, apiUrl);
      setSavedApiUrl(apiUrl);
      setApiUrl('');
    } catch (e) {
      console.error('Error saving URL:', e);
    }
  };

  const saveApiKey = async () => {
    try {
      await setItem(entries.KEY, apiKey);
      setSavedApiKey(apiKey);
      setApiKey('');
    } catch (e) {
      console.error('Error saving key:', e);
    }
  };

  const maskApiKey = (str: string, visibleChars: number): string => {
    if (!str) return '';

    const visible = str.substring(0, visibleChars);
    const masked = '*'.repeat(
      Math.max(0, Math.min(str.length, 20) - visibleChars),
    );

    return visible + masked;
  };

  const maskApiGatewayUrl = (url: string): string => {
    if (!url) return '';

    try {
      const urlObj = new URL(url);

      const hostname = urlObj.hostname;

      const pathname = urlObj.pathname;

      const hostParts = hostname.split('.');

      const apiId = hostParts[0];
      const maskedApiId = apiId.substring(0, 6) + '*'.repeat(apiId.length - 6);
      hostParts[0] = maskedApiId;

      const maskedHostname = hostParts.join('.');

      const pathParts = pathname.split('/').filter((part) => part);
      const maskedPathParts = pathParts.map(() => '****');
      const maskedPathname =
        maskedPathParts.length > 0 ? '/' + maskedPathParts.join('/') : '';

      return `${urlObj.protocol}//${maskedHostname}${maskedPathname}`;
    } catch (error) {
      const parts = url.split('/');
      const domain = parts[2] || '';

      if (domain.includes('.execute-api.')) {
        const domainParts = domain.split('.');
        if (domainParts.length > 0) {
          const apiId = domainParts[0];
          domainParts[0] = apiId.substring(0, 6) + '*'.repeat(apiId.length - 6);
        }
        parts[2] = domainParts.join('.');
      }

      for (let i = 3; i < parts.length; i++) {
        if (parts[i]) parts[i] = '****';
      }

      return parts.join('/');
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.settings}>
        <ButtonRound iconName={'home'} onPress={navigateToMain} />
      </View>

      {/* API Url */}
      <View style={styles.section}>
        <View style={styles.header}>
          <View style={styles.headerTitleContainer}>
            <Text style={styles.headerText}>API Url</Text>
          </View>
          <ButtonRound iconName={'save-outline'} onPress={saveUrl} />
        </View>
        <Text style={styles.logLabel}>Enter your API url</Text>
        <TextInput
          value={apiUrl}
          onChangeText={setApiUrl}
          placeholder="Your API url"
          style={styles.textInput}
        />
      </View>

      {/* API Key */}
      <View style={styles.section}>
        <View style={styles.header}>
          <View style={styles.headerTitleContainer}>
            <Text style={styles.headerText}>API Key</Text>
          </View>
          <ButtonRound iconName={'save-outline'} onPress={saveApiKey} />
        </View>
        <Text style={styles.logLabel}>Enter your API key</Text>
        <TextInput
          value={apiKey}
          onChangeText={setApiKey}
          secureTextEntry
          placeholder="Your API key"
          style={styles.textInput}
        />
      </View>
      <View style={styles.section}>
        <Text style={styles.headerText}>Currently saved values:</Text>
        <Text style={styles.logLabel}>Url</Text>
        <TextInput
          multiline={true}
          editable={false}
          value={maskApiGatewayUrl(savedApiUrl)}
          style={styles.textInputDisabled}
        />
        <Text style={styles.logLabel}>Key</Text>
        <TextInput
          multiline={true}
          editable={false}
          value={maskApiKey(savedApiKey, 3)}
          style={styles.textInputDisabled}
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
  logLabel: {
    fontWeight: '600',
    marginBottom: 5,
  },
  textInput: {
    height: 50,
    borderStyle: 'dashed',
    borderColor: '#000000',
    borderWidth: 2,
    borderRadius: 10,
    width: '100%',
    backgroundColor: '#e1f9df',
    padding: 8,
  },
  textInputDisabled: {
    borderStyle: 'dashed',
    borderColor: '#000000',
    borderWidth: 2,
    borderRadius: 10,
    width: '100%',
    backgroundColor: '#e1f9df',
    padding: 8,
  },
});
