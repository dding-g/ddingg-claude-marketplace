# Modern React Patterns

> React 19+ 시대의 패턴

## 컴포넌트 구조

### 단순하게 시작

```typescript
// 대부분의 컴포넌트는 이 정도면 충분
function UserCard({ user }: { user: User }) {
  return (
    <div className="user-card">
      <img src={user.avatar} alt="" />
      <span>{user.name}</span>
    </div>
  );
}
```

### 복잡해지면 분리

```typescript
// 한 파일이 커지면 같은 폴더에 분리
// features/user/
// ├── user-card.tsx
// ├── user-avatar.tsx
// ├── user-info.tsx
// └── index.ts

function UserCard({ user }: { user: User }) {
  return (
    <div className="user-card">
      <UserAvatar src={user.avatar} />
      <UserInfo name={user.name} email={user.email} />
    </div>
  );
}
```

## 상태 관리 판단 기준

```
이 상태를 누가 알아야 하나?

├─ 이 컴포넌트만 → useState
├─ 부모-자식 몇 개 → props로 전달
├─ 멀리 떨어진 여러 컴포넌트 → Context 또는 상태 관리 라이브러리
└─ 서버 데이터 → React Query
```

### useState vs useReducer

```typescript
// 단순한 상태 → useState
const [isOpen, setIsOpen] = useState(false);

// 복잡하거나 연관된 상태 → useReducer
const [state, dispatch] = useReducer(formReducer, initialState);
```

## Compound Components

관련 컴포넌트를 하나의 API로 묶을 때:

```typescript
// 사용
<Select value={selected} onChange={setSelected}>
  <Select.Trigger>선택하세요</Select.Trigger>
  <Select.Content>
    <Select.Item value="a">옵션 A</Select.Item>
    <Select.Item value="b">옵션 B</Select.Item>
  </Select.Content>
</Select>

// 구현
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

## Render Props vs Custom Hook

```typescript
// Render Props: UI 커스터마이징이 필요할 때
<MouseTracker>
  {({ x, y }) => <Cursor x={x} y={y} />}
</MouseTracker>

// Custom Hook: 로직 재사용 (대부분의 경우 이걸 사용)
function useMousePosition() {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  // ...
  return position;
}

function Cursor() {
  const { x, y } = useMousePosition();
  return <div style={{ left: x, top: y }} />;
}
```

**대부분 Custom Hook이 더 나음**. Render Props는 라이브러리 API 설계시에만.

## Error Boundary

```typescript
// 클래스 컴포넌트로 작성 (React 요구사항)
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

// 사용 (react-error-boundary 라이브러리 추천)
<ErrorBoundary fallback={<ErrorPage />}>
  <App />
</ErrorBoundary>
```

## Suspense 패턴

```typescript
// 데이터 로딩
<Suspense fallback={<Skeleton />}>
  <UserProfile />  {/* useSuspenseQuery 사용 */}
</Suspense>

// 코드 스플리팅
const AdminPanel = lazy(() => import('./admin-panel'));

<Suspense fallback={<Loading />}>
  <AdminPanel />
</Suspense>

// 중첩 Suspense로 점진적 로딩
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

## React 19 패턴

### use() Hook

```typescript
// Promise를 직접 읽기 (Suspense 필요)
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise);
  return <div>{user.name}</div>;
}

// Context 읽기 (useContext 대체 가능)
function Button() {
  const theme = use(ThemeContext);
  return <button className={theme.button}>Click</button>;
}
```

### useActionState (폼 처리)

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
        {isPending ? '전송 중...' : '전송'}
      </button>
      {state?.success && <p>완료!</p>}
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
    addOptimistic(1);  // 즉시 UI 업데이트
    await onLike();    // 실제 요청
  };

  return <button onClick={handleClick}>❤️ {optimisticLikes}</button>;
}
```

## 피해야 할 패턴

```typescript
// ❌ useEffect로 상태 동기화
const [items, setItems] = useState([]);
const [filteredItems, setFilteredItems] = useState([]);

useEffect(() => {
  setFilteredItems(items.filter(i => i.active));
}, [items]);

// ✅ 렌더링 중에 계산
const filteredItems = useMemo(
  () => items.filter(i => i.active),
  [items]
);

// ❌ 초기화를 useEffect로
useEffect(() => {
  fetchUser().then(setUser);
}, []);

// ✅ React Query 사용
const { data: user } = useQuery({
  queryKey: ['user'],
  queryFn: fetchUser
});

// ❌ forwardRef 남용 (React 19에서는 props로 ref 전달 가능)
const Input = forwardRef((props, ref) => <input ref={ref} {...props} />);

// ✅ React 19+
function Input({ ref, ...props }) {
  return <input ref={ref} {...props} />;
}
```

**핵심**: 새 패턴을 쫓기보다, 문제를 해결하는 가장 단순한 방법을 선택하세요.
