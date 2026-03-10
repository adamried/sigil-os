---
name: react-native-ui
description: Implements React Native components from design specifications. Supports React Native 0.70+, TypeScript, and Expo.
version: 1.0.0
category: ui
chainable: true
invokes: []
invoked_by: [developer]
tools: Read, Write, Edit, Bash, Glob
inputs: [component_spec, design_tokens, accessibility_requirements]
outputs: [component_files, style_files, test_files]
---

# Skill: React Native UI

## Purpose

Implement React Native components from design specifications. This skill generates production-ready React Native code optimized for iOS and Android.

## When to Invoke

- Developer receives task to implement mobile UI component
- Constitution specifies React Native as UI framework
- Target platforms include iOS and/or Android

## Inputs

**Standard Contract (same as react-ui):**
- `component_spec`: object
- `design_tokens`: object
- `accessibility_requirements`: object

**Optional:**
- `expo`: boolean — Whether using Expo (default: auto-detect)
- `platform_specific`: boolean — Need platform-specific code

## Process

### Step 1: Detect Project Setup

```bash
# Check for Expo
grep -l "expo" package.json app.json

# Check for TypeScript
ls tsconfig.json

# Check existing component patterns
ls src/components/*.tsx app/components/*.tsx
```

### Step 2: Generate Component

**React Native specifics:**
- Use View, Text, Pressable (not div, span, button)
- StyleSheet.create for styles
- Platform-specific code when needed

```typescript
import { View, Text, Pressable, StyleSheet, Platform } from 'react-native';

interface ComponentNameProps {
  variant: 'primary' | 'secondary';
  onPress?: () => void;
  children?: React.ReactNode;
}

export const ComponentName: React.FC<ComponentNameProps> = ({
  variant,
  onPress,
  children,
}) => {
  return (
    <Pressable
      style={({ pressed }) => [
        styles.container,
        styles[variant],
        pressed && styles.pressed,
      ]}
      onPress={onPress}
      accessible={true}
      accessibilityRole="button"
    >
      <Text style={[styles.text, styles[`${variant}Text`]]}>
        {children}
      </Text>
    </Pressable>
  );
};

const styles = StyleSheet.create({
  container: {
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  primary: {
    backgroundColor: '#3B82F6',
  },
  secondary: {
    backgroundColor: '#F3F4F6',
  },
  pressed: {
    opacity: 0.8,
  },
  text: {
    fontSize: 16,
    fontWeight: '600',
  },
  primaryText: {
    color: '#FFFFFF',
  },
  secondaryText: {
    color: '#111827',
  },
});
```

### Step 3: Implement Accessibility

React Native accessibility:

```typescript
<Pressable
  accessible={true}
  accessibilityRole="button"
  accessibilityLabel={label}
  accessibilityHint={hint}
  accessibilityState={{
    disabled: disabled,
    selected: selected,
  }}
>
```

### Step 4: Platform-Specific Code

When needed:

```typescript
import { Platform } from 'react-native';

const styles = StyleSheet.create({
  shadow: Platform.select({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
    },
    android: {
      elevation: 4,
    },
  }),
});
```

### Step 5: Generate Tests

```typescript
import { render, fireEvent } from '@testing-library/react-native';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('renders correctly', () => {
    const { getByText } = render(
      <ComponentName variant="primary">Press me</ComponentName>
    );
    expect(getByText('Press me')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const onPress = jest.fn();
    const { getByRole } = render(
      <ComponentName variant="primary" onPress={onPress}>Press</ComponentName>
    );
    fireEvent.press(getByRole('button'));
    expect(onPress).toHaveBeenCalled();
  });

  it('has correct accessibility role', () => {
    const { getByRole } = render(
      <ComponentName variant="primary">Press</ComponentName>
    );
    expect(getByRole('button')).toBeTruthy();
  });
});
```

## Output Format

### File Structure
```
src/components/ComponentName/
├── ComponentName.tsx
├── ComponentName.test.tsx
├── index.ts
└── styles.ts (optional, for complex styles)
```

## Handoff Data

```json
{
  "files_created": [
    "src/components/ComponentName/ComponentName.tsx",
    "src/components/ComponentName/ComponentName.test.tsx",
    "src/components/ComponentName/index.ts"
  ],
  "expo": true,
  "platform_specific": false,
  "accessibility_implemented": true,
  "typescript": true
}
```

## React Native Patterns

### Layout
- Flexbox by default (flexDirection: 'column')
- Dimensions API for responsive
- SafeAreaView for notches

### Touch
- Pressable (preferred) over TouchableOpacity
- Proper hit slop for touch targets (min 44pt)
- Visual feedback on press

### Platform
- Platform.OS for conditionals
- Platform.select for style objects
- .ios.tsx / .android.tsx for file-level splits

### Navigation
- React Navigation integration
- Screen-level components
- Deep linking support

### Performance
- FlatList for long lists
- Image caching
- Avoid inline functions in renders

## Human Checkpoint

**Tier:** Auto

## Error Handling

| Error | Resolution |
|-------|------------|
| Expo-specific API needed | Check for Expo, suggest expo install |
| Platform conflict | Create platform-specific files |
| Touch target too small | Enforce 44pt minimum |
| Missing native module | Document dependency requirement |
