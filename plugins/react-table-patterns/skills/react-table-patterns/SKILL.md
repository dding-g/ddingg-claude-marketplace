---
name: react-table-patterns
description: TanStack React Table patterns. Activated when working with tables, DataGrid, column definitions, sorting, selection, or pagination.
---

# TanStack React Table Patterns

> @tanstack/react-table v8 DataGrid wrapper + column definition patterns

## File Structure

```
shared/ui/data-grid/
├── data-grid.tsx                # DataGrid wrapper (useReactTable)
├── data-grid-header.tsx         # Header group rendering
├── data-grid-body.tsx           # Body (loading/empty states)
├── data-grid-row.tsx            # Row (disabled overlay support)
├── data-grid-sortable-header.tsx
├── data-grid-loading.tsx        # Loading skeleton
├── data-grid-empty.tsx          # Empty state
└── types.ts                     # ColumnFlexBehavior type extension

features/{domain}/ui/
├── columns.tsx                  # Column definitions (ColumnDef[])
└── {domain}.table.tsx           # Table component
```

## 1. DataGrid Usage

DataGrid wraps `useReactTable`. Never call `useReactTable` directly.

```typescript
import { DataGrid, Pagination } from '@/shared/ui';
import { getApplicantsColumns } from './columns';

export function ApplicantsTable() {
  const { contents, pageable, isLoading } = useApplicantsList();
  const [rowSelection, setRowSelection] = useState<RowSelectionState>({});
  const columns = getApplicantsColumns();

  return (
    <div className='flex-1 flex flex-col'>
      <div className='flex-1 min-h-0'>
        <DataGrid
          columns={columns}
          data={contents}
          loading={isLoading}
          emptyState={
            <DataGrid.Empty
              noDataContent={EMPTY_STATE.NO_DATA}
              noSearchResultContent={EMPTY_STATE.NO_SEARCH_RESULT}
            />
          }
          enableRowSelection
          rowSelection={rowSelection}
          onRowSelectionChange={setRowSelection}
          getRowId={(row) => row.applicantUserKey}
          onRowClick={(row) => navigate({ to: '/detail/$id', params: { id: row.id } })}
        />
      </div>
      <Pagination pageable={pageable} />
    </div>
  );
}
```

## 2. Column Definition Patterns

### Factory Function (Recommended)

```typescript
import type { ColumnDef } from '@tanstack/react-table';

type ApplicantsColumn = NonNullable<
  NonNullable<GetV1ApplicantsResponse['data']>['contents']
>[number];

export function getApplicantsColumns(): ColumnDef<ApplicantsColumn>[] {
  return [
    {
      id: 'name',
      accessorKey: 'name',
      header: 'Name',
      enableSorting: false,
      meta: { flexBehavior: 'fluid' },
      cell: ({ row }) => (
        <div className='truncate'>{row.original.name}</div>
      ),
    },
    {
      id: 'phone',
      accessorKey: 'phone',
      header: 'Phone',
      enableSorting: false,
      size: 120,
      meta: { flexBehavior: 'fixed' },
      cell: ({ row }) => (
        <div className='truncate'>{row.original.phone || '-'}</div>
      ),
    },
    {
      id: 'actions',
      header: '',
      enableSorting: false,
      size: 80,
      meta: { flexBehavior: 'fixed' },
      cell: ({ row }) => <ActionMenu row={row.original} />,
    },
  ];
}
```

### Factory with Parameters

```typescript
interface GetColumnsParams {
  processOptions: { label: string; value: string }[];
}

export function getPositionColumns({
  processOptions,
}: GetColumnsParams): ColumnDef<PositionColumn>[] {
  return [
    {
      id: 'processId',
      header: 'Process',
      cell: ({ row }) => (
        <Select
          items={processOptions}
          value={row.original.processId}
          onValueChange={(value) => handleChange(row.original.id, value)}
        />
      ),
    },
  ];
}
```

## 3. Column Width: flexBehavior

```typescript
// shared/ui/data-grid/types.ts
export type ColumnFlexBehavior = 'fixed' | 'fluid';

declare module '@tanstack/react-table' {
  interface ColumnMeta<TData, TValue> {
    flexBehavior?: ColumnFlexBehavior;
  }
}
```

|Type|Usage|Examples|
|---|---|---|
|`'fixed'` + `size`|Fixed width (shrink-0)|Checkbox (48), date (100), actions (80)|
|`'fluid'`|Fills remaining space (flex-grow)|Name, description|

## 4. Cell Renderer Patterns

### Status Badge

```typescript
{
  id: 'status',
  cell: ({ row }) => {
    const colorInfo = getStatusColorInfo(row.original.status);
    return <Badge variant={colorInfo.variant} size='xsm'>{formatStatus(row.original.status)}</Badge>;
  },
}
```

### Interactive Cell with Hooks

Use **named function** for cells that need hooks:

```typescript
{
  id: 'actions',
  cell: function ActionCell({ row }) {
    const { handleArchive, isPending } = useApplicantArchive(row.original.id);
    const [isOpen, setIsOpen] = useState(false);

    return (
      <Menu open={isOpen} onOpenChange={setIsOpen}>
        <MenuTrigger onClick={(e) => e.stopPropagation()}>
          <Button size='icon' variant='primaryWhite'><EllipsisIcon /></Button>
        </MenuTrigger>
        <MenuContent align='end'>
          <MenuItem onClick={handleArchive}>
            {isPending ? <LoaderIcon className='animate-spin' /> : 'Delete'}
          </MenuItem>
        </MenuContent>
      </Menu>
    );
  },
}
```

### Cell with Select (Stop propagation)

```typescript
{
  id: 'processId',
  cell: ({ row }) => (
    <div onClick={(e) => e.stopPropagation()}>
      <Select
        items={processOptions}
        value={row.original.processId}
        onValueChange={(value) => handleChange(row.original.id, value)}
      />
    </div>
  ),
}
```

## 5. Row Selection

```typescript
function TableWithSelection() {
  const [rowSelection, setRowSelection] = useState<RowSelectionState>({});
  const selectedKeys = useMemo(() => Object.keys(rowSelection), [rowSelection]);

  return (
    <>
      <DataGrid
        columns={columns}
        data={data}
        enableRowSelection
        rowSelection={rowSelection}
        onRowSelectionChange={setRowSelection}
        getRowId={(row) => row.id}
        rowDisabled={(row) => row.status === 'LOCKED'}
      />
      <FloatingBar selectedCount={selectedKeys.length} onClear={() => setRowSelection({})} />
    </>
  );
}
```

## 6. Page Layout

```typescript
function TablePage() {
  return (
    <div className='flex-1 flex flex-col'>
      <div className='px-9 py-6 shrink-0'>
        <TableHeader totalCount={pageable?.total} />
      </div>
      <div className='flex-1 min-h-0'>
        <DataGrid columns={columns} data={data} loading={isLoading}
          emptyState={<DataGrid.Empty ... />} />
      </div>
      <div className='shrink-0 px-10 py-5 border-t'>
        <Pagination pageable={pageable} />
      </div>
      <FloatingBar selectedCount={selectedCount} onClear={clearSelection} />
    </div>
  );
}
```

## 7. Type Patterns

```typescript
// Extract row type from API response
type ApplicantsColumn = NonNullable<
  NonNullable<GetV1CompaniesApplicantsResponse['data']>['contents']
>[number];

// Required imports
import type { ColumnDef, RowSelectionState, SortingState, OnChangeFn } from '@tanstack/react-table';
import { getCoreRowModel, getSortedRowModel, flexRender, useReactTable } from '@tanstack/react-table';
```

## DO NOT

```typescript
// AVOID: direct useReactTable (use DataGrid wrapper)
const table = useReactTable({ ... });

// AVOID: inline column definitions
<DataGrid columns={[{ id: 'name', ... }]} data={data} />
// USE: separate columns file
import { getColumns } from './columns';

// AVOID: hooks in arrow function cell (Rules of Hooks violation)
cell: ({ row }) => { const { data } = useQuery(...); }
// USE: named function cell
cell: function MyCell({ row }) { const { data } = useQuery(...); }

// AVOID: size without flexBehavior
{ size: 120 }
// USE: pair with flexBehavior
{ size: 120, meta: { flexBehavior: 'fixed' } }

// AVOID: selection without getRowId
<DataGrid enableRowSelection rowSelection={rowSelection} />
// USE: always specify getRowId
<DataGrid enableRowSelection getRowId={(row) => row.uniqueKey} />

// AVOID: missing stopPropagation on interactive cells
cell: ({ row }) => (<Select onValueChange={handleChange} />)
// USE: wrap with stopPropagation
cell: ({ row }) => (
  <div onClick={(e) => e.stopPropagation()}>
    <Select onValueChange={handleChange} />
  </div>
)
```
