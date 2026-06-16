import { useCallback, useEffect, useState } from "react";

const STORAGE_KEY = "bucket-list-visited";

function loadVisited(defaultIds: string[]): Record<string, boolean> {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    const stored: Record<string, boolean> = raw ? JSON.parse(raw) : {};
    // Seed any place marked defaultVisited that hasn't been explicitly toggled yet.
    const merged = { ...stored };
    for (const id of defaultIds) {
      if (!(id in merged)) merged[id] = true;
    }
    return merged;
  } catch {
    return {};
  }
}

/**
 * Tracks which place IDs have been visited.
 * Currently backed by localStorage (per-device). To make this sync across
 * the family, swap loadVisited/saveVisited for Supabase reads/writes -
 * the rest of the app only depends on this hook's return shape.
 */
export function useVisited(defaultIds: string[] = []) {
  const [visited, setVisited] = useState<Record<string, boolean>>(() => loadVisited(defaultIds));

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(visited));
  }, [visited]);

  const toggleVisited = useCallback((id: string) => {
    setVisited((prev) => ({ ...prev, [id]: !prev[id] }));
  }, []);

  const isVisited = useCallback((id: string) => !!visited[id], [visited]);

  return { visited, isVisited, toggleVisited };
}
