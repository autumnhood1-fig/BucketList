interface Props {
  label: string;
  checked: boolean;
  onChange: () => void;
  swatch?: string;
}

export function Checkbox({ label, checked, onChange, swatch }: Props) {
  return (
    <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer py-0.5">
      <input
        type="checkbox"
        checked={checked}
        onChange={onChange}
        className="h-4 w-4 shrink-0"
      />
      {swatch && (
        <span
          className="inline-block h-2.5 w-2.5 rounded-full shrink-0"
          style={{ background: swatch }}
        />
      )}
      <span>{label}</span>
    </label>
  );
}
