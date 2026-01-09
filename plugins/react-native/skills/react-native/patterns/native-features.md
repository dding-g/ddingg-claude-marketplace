# React Native Native Features

## Camera & Media

### expo-camera

```typescript
// features/camera/ui/camera-screen.tsx
import { CameraView, useCameraPermissions } from 'expo-camera';
import { useState, useRef } from 'react';

export function CameraScreen() {
  const [permission, requestPermission] = useCameraPermissions();
  const [facing, setFacing] = useState<'front' | 'back'>('back');
  const cameraRef = useRef<CameraView>(null);

  if (!permission) {
    return <View />;
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text>카메라 권한이 필요합니다</Text>
        <Button onPress={requestPermission} title="권한 요청" />
      </View>
    );
  }

  const takePicture = async () => {
    if (cameraRef.current) {
      const photo = await cameraRef.current.takePictureAsync();
      console.log(photo.uri);
    }
  };

  return (
    <View style={styles.container}>
      <CameraView
        ref={cameraRef}
        style={styles.camera}
        facing={facing}
      >
        <View style={styles.controls}>
          <Button
            title="촬영"
            onPress={takePicture}
          />
          <Button
            title="전환"
            onPress={() => setFacing(f => f === 'back' ? 'front' : 'back')}
          />
        </View>
      </CameraView>
    </View>
  );
}
```

### expo-image-picker

```typescript
// features/upload/lib/image-picker.ts
import * as ImagePicker from 'expo-image-picker';

export async function pickImage() {
  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.Images,
    allowsEditing: true,
    aspect: [1, 1],
    quality: 0.8,
  });

  if (!result.canceled) {
    return result.assets[0].uri;
  }

  return null;
}

export async function takePhoto() {
  const permission = await ImagePicker.requestCameraPermissionsAsync();

  if (!permission.granted) {
    throw new Error('Camera permission required');
  }

  const result = await ImagePicker.launchCameraAsync({
    allowsEditing: true,
    aspect: [1, 1],
    quality: 0.8,
  });

  if (!result.canceled) {
    return result.assets[0].uri;
  }

  return null;
}
```

## Location

### expo-location

```typescript
// features/location/lib/location.ts
import * as Location from 'expo-location';

export async function getCurrentLocation() {
  const { status } = await Location.requestForegroundPermissionsAsync();

  if (status !== 'granted') {
    throw new Error('Location permission required');
  }

  const location = await Location.getCurrentPositionAsync({
    accuracy: Location.Accuracy.Balanced,
  });

  return {
    latitude: location.coords.latitude,
    longitude: location.coords.longitude,
  };
}

// 실시간 위치 추적
export function watchLocation(
  callback: (location: Location.LocationObject) => void
) {
  return Location.watchPositionAsync(
    {
      accuracy: Location.Accuracy.Balanced,
      timeInterval: 5000,
      distanceInterval: 10,
    },
    callback
  );
}

// 주소 변환
export async function reverseGeocode(latitude: number, longitude: number) {
  const [address] = await Location.reverseGeocodeAsync({
    latitude,
    longitude,
  });

  return address;
}
```

```typescript
// features/location/ui/location-button.tsx
import { useState } from 'react';
import { getCurrentLocation, reverseGeocode } from '../lib/location';

export function LocationButton({ onLocation }: Props) {
  const [isLoading, setIsLoading] = useState(false);

  const handlePress = async () => {
    try {
      setIsLoading(true);
      const coords = await getCurrentLocation();
      const address = await reverseGeocode(coords.latitude, coords.longitude);
      onLocation({ coords, address });
    } catch (error) {
      Alert.alert('오류', '위치를 가져올 수 없습니다');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Pressable onPress={handlePress} disabled={isLoading}>
      <Text>{isLoading ? '위치 확인 중...' : '현재 위치'}</Text>
    </Pressable>
  );
}
```

## Biometrics

### expo-local-authentication

```typescript
// features/auth/lib/biometrics.ts
import * as LocalAuthentication from 'expo-local-authentication';

export async function checkBiometricSupport() {
  const hasHardware = await LocalAuthentication.hasHardwareAsync();
  const isEnrolled = await LocalAuthentication.isEnrolledAsync();
  const supportedTypes = await LocalAuthentication.supportedAuthenticationTypesAsync();

  return {
    isSupported: hasHardware && isEnrolled,
    types: supportedTypes.map((type) => {
      switch (type) {
        case LocalAuthentication.AuthenticationType.FINGERPRINT:
          return 'fingerprint';
        case LocalAuthentication.AuthenticationType.FACIAL_RECOGNITION:
          return 'face';
        case LocalAuthentication.AuthenticationType.IRIS:
          return 'iris';
        default:
          return 'unknown';
      }
    }),
  };
}

export async function authenticateWithBiometrics() {
  const result = await LocalAuthentication.authenticateAsync({
    promptMessage: '생체 인증으로 로그인',
    cancelLabel: '취소',
    disableDeviceFallback: false,
    fallbackLabel: '비밀번호 사용',
  });

  return result.success;
}
```

## Haptics

### expo-haptics

```typescript
// shared/lib/haptics.ts
import * as Haptics from 'expo-haptics';

export const haptics = {
  light: () => Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light),
  medium: () => Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium),
  heavy: () => Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy),
  success: () => Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success),
  warning: () => Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning),
  error: () => Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error),
  selection: () => Haptics.selectionAsync(),
};

// 사용 예시
function LikeButton() {
  const handlePress = async () => {
    await haptics.success();
    // 좋아요 로직
  };

  return <Pressable onPress={handlePress}>❤️</Pressable>;
}
```

## Share & Clipboard

### expo-sharing & expo-clipboard

```typescript
// shared/lib/share.ts
import * as Sharing from 'expo-sharing';
import * as Clipboard from 'expo-clipboard';
import { Share as RNShare, Platform } from 'react-native';

// 텍스트 공유
export async function shareText(message: string, title?: string) {
  try {
    await RNShare.share({
      message,
      title,
    });
  } catch (error) {
    console.error('Share failed:', error);
  }
}

// 파일 공유
export async function shareFile(fileUri: string) {
  const isAvailable = await Sharing.isAvailableAsync();

  if (!isAvailable) {
    throw new Error('Sharing is not available');
  }

  await Sharing.shareAsync(fileUri);
}

// 클립보드
export async function copyToClipboard(text: string) {
  await Clipboard.setStringAsync(text);
}

export async function getFromClipboard() {
  return Clipboard.getStringAsync();
}
```

## App Linking

### expo-linking

```typescript
// shared/lib/linking.ts
import * as Linking from 'expo-linking';
import { Platform } from 'react-native';

// URL 열기
export async function openUrl(url: string) {
  const canOpen = await Linking.canOpenURL(url);

  if (canOpen) {
    await Linking.openURL(url);
  } else {
    throw new Error(`Cannot open URL: ${url}`);
  }
}

// 전화 걸기
export function makeCall(phoneNumber: string) {
  const url = Platform.select({
    ios: `telprompt:${phoneNumber}`,
    android: `tel:${phoneNumber}`,
  });

  if (url) Linking.openURL(url);
}

// 이메일 보내기
export function sendEmail(email: string, subject?: string, body?: string) {
  const url = `mailto:${email}?subject=${encodeURIComponent(subject ?? '')}&body=${encodeURIComponent(body ?? '')}`;
  Linking.openURL(url);
}

// 지도 열기
export function openMaps(latitude: number, longitude: number, label?: string) {
  const url = Platform.select({
    ios: `maps:0,0?q=${label ?? 'Location'}@${latitude},${longitude}`,
    android: `geo:${latitude},${longitude}?q=${latitude},${longitude}(${label ?? 'Location'})`,
  });

  if (url) Linking.openURL(url);
}

// 앱 설정 열기
export function openSettings() {
  Linking.openSettings();
}
```

## Background Tasks

### expo-task-manager & expo-background-fetch

```typescript
// features/sync/lib/background-sync.ts
import * as TaskManager from 'expo-task-manager';
import * as BackgroundFetch from 'expo-background-fetch';

const BACKGROUND_SYNC_TASK = 'background-sync';

// 태스크 정의
TaskManager.defineTask(BACKGROUND_SYNC_TASK, async () => {
  try {
    // 백그라운드에서 실행할 작업
    await syncData();
    return BackgroundFetch.BackgroundFetchResult.NewData;
  } catch (error) {
    return BackgroundFetch.BackgroundFetchResult.Failed;
  }
});

// 태스크 등록
export async function registerBackgroundSync() {
  const status = await BackgroundFetch.getStatusAsync();

  if (status === BackgroundFetch.BackgroundFetchStatus.Available) {
    await BackgroundFetch.registerTaskAsync(BACKGROUND_SYNC_TASK, {
      minimumInterval: 15 * 60, // 15분
      stopOnTerminate: false,
      startOnBoot: true,
    });
  }
}

// 태스크 해제
export async function unregisterBackgroundSync() {
  await BackgroundFetch.unregisterTaskAsync(BACKGROUND_SYNC_TASK);
}
```

## Device Info

### expo-device & expo-constants

```typescript
// shared/lib/device.ts
import * as Device from 'expo-device';
import Constants from 'expo-constants';

export const deviceInfo = {
  brand: Device.brand,
  manufacturer: Device.manufacturer,
  modelName: Device.modelName,
  osName: Device.osName,
  osVersion: Device.osVersion,
  deviceType: Device.deviceType,
  isDevice: Device.isDevice, // true if physical device

  // App info
  appVersion: Constants.expoConfig?.version,
  buildNumber: Constants.expoConfig?.ios?.buildNumber ||
               Constants.expoConfig?.android?.versionCode,
  bundleId: Constants.expoConfig?.ios?.bundleIdentifier ||
            Constants.expoConfig?.android?.package,
};

// 디바이스 타입 확인
export function getDeviceType() {
  switch (Device.deviceType) {
    case Device.DeviceType.PHONE:
      return 'phone';
    case Device.DeviceType.TABLET:
      return 'tablet';
    case Device.DeviceType.DESKTOP:
      return 'desktop';
    case Device.DeviceType.TV:
      return 'tv';
    default:
      return 'unknown';
  }
}
```

## Permission Pattern

```typescript
// shared/lib/permissions.ts
import * as ImagePicker from 'expo-image-picker';
import * as Location from 'expo-location';
import * as Notifications from 'expo-notifications';
import { Alert, Linking } from 'react-native';

type PermissionType = 'camera' | 'photos' | 'location' | 'notifications';

export async function requestPermission(type: PermissionType): Promise<boolean> {
  let status: string;

  switch (type) {
    case 'camera':
      ({ status } = await ImagePicker.requestCameraPermissionsAsync());
      break;
    case 'photos':
      ({ status } = await ImagePicker.requestMediaLibraryPermissionsAsync());
      break;
    case 'location':
      ({ status } = await Location.requestForegroundPermissionsAsync());
      break;
    case 'notifications':
      ({ status } = await Notifications.requestPermissionsAsync());
      break;
  }

  if (status !== 'granted') {
    Alert.alert(
      '권한 필요',
      `이 기능을 사용하려면 ${type} 권한이 필요합니다.`,
      [
        { text: '취소', style: 'cancel' },
        { text: '설정으로 이동', onPress: () => Linking.openSettings() },
      ]
    );
    return false;
  }

  return true;
}
```
