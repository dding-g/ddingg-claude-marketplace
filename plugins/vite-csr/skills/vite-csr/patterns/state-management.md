# Vite CSR State Management Patterns

## State 분류

| 상태 유형 | 도구 | 예시 |
|----------|------|------|
| Server State | React Query | API 데이터, 캐시 |
| Client State (Global) | Zustand | 인증, 테마, 사이드바 |
| Client State (Local) | useState/useReducer | 폼 입력, 모달 열림 |
| URL State | React Router | 필터, 페이지네이션 |

## Zustand Patterns

### Basic Store

```typescript
// features/auth/model/store.ts
import { create } from 'zustand';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
}

interface AuthActions {
  login: (user: User) => void;
  logout: () => void;
  updateUser: (updates: Partial<User>) => void;
}

type AuthStore = AuthState & AuthActions;

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  isAuthenticated: false,

  login: (user) => set({ user, isAuthenticated: true }),
  logout: () => set({ user: null, isAuthenticated: false }),
  updateUser: (updates) =>
    set((state) => ({
      user: state.user ? { ...state.user, ...updates } : null,
    })),
}));
```

### Persist Middleware

```typescript
// features/settings/model/store.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

interface SettingsState {
  theme: 'light' | 'dark' | 'system';
  language: string;
  notifications: boolean;
}

interface SettingsActions {
  setTheme: (theme: SettingsState['theme']) => void;
  setLanguage: (language: string) => void;
  toggleNotifications: () => void;
}

export const useSettingsStore = create<SettingsState & SettingsActions>()(
  persist(
    (set) => ({
      theme: 'system',
      language: 'ko',
      notifications: true,

      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
      toggleNotifications: () =>
        set((state) => ({ notifications: !state.notifications })),
    }),
    {
      name: 'settings-storage',
      storage: createJSONStorage(() => localStorage),
    }
  )
);
```

### Computed Values with Selectors

```typescript
// entities/cart/model/store.ts
import { create } from 'zustand';

interface CartState {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  clearCart: () => void;
}

export const useCartStore = create<CartState>((set) => ({
  items: [],

  addItem: (item) =>
    set((state) => {
      const existing = state.items.find((i) => i.id === item.id);
      if (existing) {
        return {
          items: state.items.map((i) =>
            i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
          ),
        };
      }
      return { items: [...state.items, { ...item, quantity: 1 }] };
    }),

  removeItem: (id) =>
    set((state) => ({
      items: state.items.filter((i) => i.id !== id),
    })),

  clearCart: () => set({ items: [] }),
}));

// Selectors (별도 파일 또는 같은 파일)
export const selectCartTotal = (state: CartState) =>
  state.items.reduce((sum, item) => sum + item.price * item.quantity, 0);

export const selectCartItemCount = (state: CartState) =>
  state.items.reduce((sum, item) => sum + item.quantity, 0);

// 사용
function CartSummary() {
  const total = useCartStore(selectCartTotal);
  const itemCount = useCartStore(selectCartItemCount);

  return (
    <div>
      <span>{itemCount} items</span>
      <span>${total}</span>
    </div>
  );
}
```

### Slices Pattern

```typescript
// app/store/index.ts
import { create } from 'zustand';

// Auth Slice
interface AuthSlice {
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
}

const createAuthSlice = (set: any): AuthSlice => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null }),
});

// UI Slice
interface UISlice {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
}

const createUISlice = (set: any): UISlice => ({
  sidebarOpen: true,
  toggleSidebar: () => set((state: UISlice) => ({ sidebarOpen: !state.sidebarOpen })),
});

// Combined Store
type AppStore = AuthSlice & UISlice;

export const useAppStore = create<AppStore>()((...args) => ({
  ...createAuthSlice(...args),
  ...createUISlice(...args),
}));
```

## React Query + Zustand Integration

```typescript
// features/user/api/mutations.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuthStore } from '@/features/auth';

export const useUpdateProfileMutation = () => {
  const queryClient = useQueryClient();
  const updateUser = useAuthStore((s) => s.updateUser);

  return useMutation({
    mutationFn: updateProfile,
    onSuccess: (data) => {
      // React Query 캐시 업데이트
      queryClient.setQueryData(['user', 'me'], data);
      // Zustand 스토어 업데이트
      updateUser(data);
    },
  });
};
```

## Context for Scoped State

```typescript
// features/form/model/context.tsx
import { createContext, useContext, useReducer } from 'react';

interface FormState {
  values: Record<string, any>;
  errors: Record<string, string>;
  touched: Record<string, boolean>;
}

type FormAction =
  | { type: 'SET_VALUE'; field: string; value: any }
  | { type: 'SET_ERROR'; field: string; error: string }
  | { type: 'SET_TOUCHED'; field: string }
  | { type: 'RESET' };

const FormContext = createContext<{
  state: FormState;
  dispatch: React.Dispatch<FormAction>;
} | null>(null);

function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case 'SET_VALUE':
      return {
        ...state,
        values: { ...state.values, [action.field]: action.value },
      };
    case 'SET_ERROR':
      return {
        ...state,
        errors: { ...state.errors, [action.field]: action.error },
      };
    case 'SET_TOUCHED':
      return {
        ...state,
        touched: { ...state.touched, [action.field]: true },
      };
    case 'RESET':
      return { values: {}, errors: {}, touched: {} };
    default:
      return state;
  }
}

export function FormProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(formReducer, {
    values: {},
    errors: {},
    touched: {},
  });

  return (
    <FormContext.Provider value={{ state, dispatch }}>
      {children}
    </FormContext.Provider>
  );
}

export function useForm() {
  const context = useContext(FormContext);
  if (!context) throw new Error('useForm must be used within FormProvider');
  return context;
}
```

## URL State Management

```typescript
// shared/lib/hooks/use-url-state.ts
import { useSearchParams } from 'react-router-dom';
import { useCallback, useMemo } from 'react';

export function useUrlState<T extends Record<string, string>>(
  defaultValues: T
) {
  const [searchParams, setSearchParams] = useSearchParams();

  const state = useMemo(() => {
    const result = { ...defaultValues };
    Object.keys(defaultValues).forEach((key) => {
      const value = searchParams.get(key);
      if (value !== null) {
        result[key as keyof T] = value as T[keyof T];
      }
    });
    return result;
  }, [searchParams, defaultValues]);

  const setState = useCallback(
    (updates: Partial<T>) => {
      setSearchParams((prev) => {
        Object.entries(updates).forEach(([key, value]) => {
          if (value === undefined || value === defaultValues[key]) {
            prev.delete(key);
          } else {
            prev.set(key, value as string);
          }
        });
        return prev;
      });
    },
    [setSearchParams, defaultValues]
  );

  return [state, setState] as const;
}

// 사용 예시
function ProductList() {
  const [filters, setFilters] = useUrlState({
    category: '',
    sort: 'newest',
    page: '1',
  });

  return (
    <div>
      <select
        value={filters.sort}
        onChange={(e) => setFilters({ sort: e.target.value })}
      >
        <option value="newest">Newest</option>
        <option value="popular">Popular</option>
      </select>
    </div>
  );
}
```

## Best Practices

1. **Server State는 React Query**: API 데이터는 React Query로 관리
2. **Global Client State는 Zustand**: 인증, 설정 등 앱 전역 상태
3. **Scoped State는 Context**: 특정 트리 내에서만 필요한 상태
4. **URL State 활용**: 필터, 정렬, 페이지는 URL로 관리
5. **Selector 사용**: 불필요한 리렌더링 방지
