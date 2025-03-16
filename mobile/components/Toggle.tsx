import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

interface ToggleProps {
  value: boolean;
  onToggle: (args?: unknown) => void;
  label?: string;
  disabled?: boolean;
}

const Toggle: React.FC<ToggleProps> = ({
  value,
  onToggle,
  label,
  disabled = false,
}) => {
  const handleToggle = () => {
    if (!disabled) {
      onToggle(!value);
    }
  };

  return (
    <View style={styles.container}>
      {label && <Text style={styles.label}>{label}</Text>}
      <TouchableOpacity
        activeOpacity={0.8}
        style={[
          styles.toggleContainer,
          { backgroundColor: value ? '#4da944' : '#e1f9df' },
          disabled && styles.disabled,
        ]}
        onPress={handleToggle}
        disabled={disabled}
      >
        <View
          style={[
            styles.toggleCircle,
            value ? styles.toggleCircleOn : styles.toggleCircleOff,
          ]}
        />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  label: {
    marginRight: 8,
    fontSize: 16,
    color: '#333',
  },
  toggleContainer: {
    width: 52,
    height: 30,
    borderRadius: 15,
    paddingHorizontal: 2,
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 2,
  },
  toggleCircle: {
    width: 26,
    height: 26,
    borderRadius: 13,
    backgroundColor: 'white',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 1,
    elevation: 1,
  },
  toggleCircleOff: {
    alignSelf: 'flex-start',
  },
  toggleCircleOn: {
    alignSelf: 'flex-end',
  },
  disabled: {
    opacity: 0.5,
  },
});

export default Toggle;
