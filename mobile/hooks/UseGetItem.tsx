import AsyncStorage from '@react-native-async-storage/async-storage';

const useGetItem = () => {
  const getItem = async (key: string) => {
    try {
      const value = await AsyncStorage.getItem(key);
      return value !== null ? value : null;
    } catch (e) {
      console.error(e);
    }
  };

  return getItem;
};

export default useGetItem;
