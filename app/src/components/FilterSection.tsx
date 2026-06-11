import { useState, type ReactNode } from "react";

interface Props {
  title: string;
  children: ReactNode;
  defaultOpen?: boolean;
}

export function FilterSection({ title, children, defaultOpen = true }: Props) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="border-b border-gray-200 py-3">
      <button
        className="flex w-full items-center justify-between text-left font-semibold text-sm text-gray-800"
        onClick={() => setOpen((o) => !o)}
      >
        {title}
        <span className="text-gray-400">{open ? "−" : "+"}</span>
      </button>
      {open && <div className="mt-2 space-y-1">{children}</div>}
    </div>
  );
}
