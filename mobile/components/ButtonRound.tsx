import React from 'react';
import { Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface ButtonRoundProps {
  text?: string;
  iconName?: any;
  onPress: (args?: unknown) => void;
}

const ButtonRound: React.FC<ButtonRoundProps> = ({
  text,
  iconName,
  onPress,
}) => {
  return (
    <TouchableOpacity style={styles.touchableOpacity} onPress={onPress}>
      {text && <Text style={styles.text}>{text}</Text>}
      {iconName && <Ionicons name={iconName} size={24} color="white" />}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  touchableOpacity: {
    width: 42,
    height: 42,
    borderRadius: 21,
    backgroundColor: '#4da944',
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    color: 'white',
  },
});

export default ButtonRound;
