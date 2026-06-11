import { useCallback, useEffect, useState } from "react";

const STORAGE_KEY = "bucket-list-visited";

function loadVisited(): Record<string, boolean> {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
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
export function useVisited() {
  const [visited, setVisited] = useState<Record<string, boolean>>(() => loadVisited());

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(visited));
  }, [visited]);

  const toggleVisited = useCallback((id: string) => {
    setVisited((prev) => ({ ...prev, [id]: !prev[id] }));
  }, []);

  const isVisited = useCallback((id: string) => !!visited[id], [visited]);

  return { visited, isVisited, toggleVisited };
}
