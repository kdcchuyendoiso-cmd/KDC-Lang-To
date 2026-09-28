import { getAll } from "@/lib/db";
import { TABLES } from "@/lib/schema";
import { deleteRowAction, saveRowAction } from "@/app/quan-tri/actions";

function Field({ col, value }) {
  const name = `col__${col.key}`;
  if (col.type === "select") {
    const extra = value && !col.options.includes(value) ? [value] : [];
    return (
      <select name={name} defaultValue={value || col.options[0]}>
        {[...col.options, ...extra].map((o) => (
          <option key={o} value={o}>
            {o}
          </option>
        ))}
      </select>
    );
  }
  if (col.type === "textarea") {
    return <textarea name={name} defaultValue={value} rows={3} />;
  }
  return <input name={name} defaultValue={value} disabled={Boolean(col.readOnlyInAdmin)} />;
}

function RowForm({ table, columns, row }) {
  return (
    <form className="form-card" action={saveRowAction}>
      <input type="hidden" name="table" value={table} />
      {row ? <input type="hidden" name="id" value={row.id} /> : null}
      {columns.map((col) => (
        <div className="field" key={col.key}>
          <label>{col.label}</label>
          <Field col={col} value={row ? row[col.key] : ""} />
        </div>
      ))}
      <div style={{ display: "flex", gap: 8 }}>
        <button className="btn-primary" type="submit">
          {row ? "💾 Lưu" : "➕ Thêm dòng mới"}
        </button>
        {row ? (
          <button
            className="btn-secondary"
            type="submit"
            formAction={deleteRowAction}
            style={{ color: "var(--bad)" }}
          >
            🗑️ Xóa
          </button>
        ) : null}
      </div>
    </form>
  );
}

export default async function AdminSheetEditor({ table }) {
  const config = TABLES[table];
  const rows = await getAll(table, { orderBy: "id", desc: true });

  return (
    <>
      <div className="sec">
        <b>
          {config.icon} {config.label} ({rows.length})
        </b>
      </div>
      {rows.map((row) => (
        <RowForm key={row.id} table={table} columns={config.columns} row={row} />
      ))}
      <div className="sec">
        <b>Thêm dòng mới</b>
      </div>
      <RowForm table={table} columns={config.columns} row={null} />
    </>
  );
}
