import AsyncStorage from '@react-native-async-storage/async-storage';

const useSetItem = () => {
  const setItem = async (key: string, value: string) => {
    try {
      await AsyncStorage.setItem(key, value);
      return;
    } catch (e) {
      console.error(e);
      return null;
    }
  };

  return setItem;
};

export default useSetItem;
