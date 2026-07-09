// src/hooks/useDebounce.ts
import { useEffect, useState } from "react";

// ==============================================================================
// HOOK IMPLEMENTATION
// ==============================================================================

/**
 * Custom hook to delay the update of a value until a specified time has passed.
 * Used to prevent excessive API calls while typing.
 * * @param value - The value to debounce.
 * @param delay - The delay in milliseconds.
 * @returns The debounced value.
 */
export const useDebounce = <T>(value: T, delay: number): T => {
    const [debouncedValue, setDebouncedValue] = useState<T>(value);

    useEffect(() => {
        const timer = setTimeout(() => setDebouncedValue(value), delay);
        
        return () => {
            clearTimeout(timer);
        };
    }, [value, delay]);

    return debouncedValue;
};