---
name: react-patterns
description: Modern React 19+ patterns. Activated when working with state management, Suspense, Compound Components, or React hooks.
---

# Modern React Patterns

> React 19+ era patterns

## Component Structure

```typescript
function UserCard({ user }: { user: User }) {
  return (
    <div className="user-card">
      <img src={user.avatar} alt="" />
      <span>{user.name}</span>
    </div>
  );
}
```

When it grows, split into same-folder modules:

```typescript
// features/user/
// ├── user-card.tsx
// ├── user-avatar.tsx
// ├── user-info.tsx
// └── index.ts
```

## State Management Decision

```
Who needs this state?

├─ This component only       → useState
├─ Parent-child few levels   → props
├─ Distant multiple components → Context or state library
└─ Server data               → React Query
```

```typescript
// Simple state → useState
const [isOpen, setIsOpen] = useState(false);

// Complex/related state → useReducer
const [state, dispatch] = useReducer(formReducer, initialState);
```

## Compound Components

```typescript
<Select value={selected} onChange={setSelected}>
  <Select.Trigger>Choose</Select.Trigger>
  <Select.Content>
    <Select.Item value="a">Option A</Select.Item>
    <Select.Item value="b">Option B</Select.Item>
  </Select.Content>
</Select>

// Implementation
const SelectContext = createContext<SelectContextValue | null>(null);

function Select({ value, onChange, children }) {
  return (
    <SelectContext.Provider value={{ value, onChange }}>
      {children}
    </SelectContext.Provider>
  );
}

Select.Trigger = function Trigger({ children }) { ... };
Select.Content = function Content({ children }) { ... };
Select.Item = function Item({ value, children }) { ... };
```

## Custom Hook vs Render Props

|Pattern|Use When|
|---|---|
|Custom Hook|Logic reuse (most cases)|
|Render Props|Library API design, UI customization needed|

```typescript
// Custom Hook (preferred)
function useMousePosition() {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  // ...
  return position;
}
```

## Error Boundary

```typescript
class ErrorBoundary extends React.Component<Props, State> {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? <DefaultError error={this.state.error} />;
    }
    return this.props.children;
  }
}

// Recommend: react-error-boundary library
<ErrorBoundary fallback={<ErrorPage />}>
  <App />
</ErrorBoundary>
```

## Suspense

```typescript
// Data loading
<Suspense fallback={<Skeleton />}>
  <UserProfile />  {/* uses useSuspenseQuery */}
</Suspense>

// Code splitting
const AdminPanel = lazy(() => import('./admin-panel'));

<Suspense fallback={<Loading />}>
  <AdminPanel />
</Suspense>

// Nested Suspense for progressive loading
<Suspense fallback={<PageSkeleton />}>
  <Header />
  <Suspense fallback={<ContentSkeleton />}>
    <Content />
  </Suspense>
  <Suspense fallback={<SidebarSkeleton />}>
    <Sidebar />
  </Suspense>
</Suspense>
```

## React 19 Patterns

### use() Hook

```typescript
// Read Promise directly (requires Suspense)
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise);
  return <div>{user.name}</div>;
}

// Read Context (replaces useContext)
function Button() {
  const theme = use(ThemeContext);
  return <button className={theme.button}>Click</button>;
}
```

### useActionState (Form handling)

```typescript
async function submitForm(prevState: State, formData: FormData) {
  const result = await api.post('/submit', Object.fromEntries(formData));
  return { success: true, data: result };
}

function Form() {
  const [state, formAction, isPending] = useActionState(submitForm, null);

  return (
    <form action={formAction}>
      <input name="email" />
      <button disabled={isPending}>
        {isPending ? 'Submitting...' : 'Submit'}
      </button>
      {state?.success && <p>Done!</p>}
    </form>
  );
}
```

### useOptimistic

```typescript
function LikeButton({ likes, onLike }: Props) {
  const [optimisticLikes, addOptimistic] = useOptimistic(
    likes,
    (current, added: number) => current + added
  );

  const handleClick = async () => {
    addOptimistic(1);
    await onLike();
  };

  return <button onClick={handleClick}>{optimisticLikes}</button>;
}
```

## DO NOT

```typescript
// AVOID: useEffect for state sync
const [filteredItems, setFilteredItems] = useState([]);
useEffect(() => {
  setFilteredItems(items.filter(i => i.active));
}, [items]);
// USE: compute during render
const filteredItems = useMemo(() => items.filter(i => i.active), [items]);

// AVOID: useEffect for data fetching
useEffect(() => { fetchUser().then(setUser); }, []);
// USE: React Query
const { data: user } = useQuery({ queryKey: ['user'], queryFn: fetchUser });

// AVOID: forwardRef (React 19 passes ref as prop)
const Input = forwardRef((props, ref) => <input ref={ref} {...props} />);
// USE: React 19+
function Input({ ref, ...props }) {
  return <input ref={ref} {...props} />;
}
```

|Principle|Description|
|---|---|
|Start simple|Choose the simplest solution that solves the problem|
|Derive, don't sync|Compute values instead of syncing with useEffect|
|Hooks for logic|Extract logic into custom hooks, keep components UI-only|
