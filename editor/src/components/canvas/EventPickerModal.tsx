import { useState, useMemo } from "react";
import type { Program } from "../../types/ast";
import type { PendingConnection } from "../../hooks/useGraphEditing";
import styles from "./EventPickerModal.module.css";

type Props = {
    ast: Program;
    connection: PendingConnection;
    onConfirm: (eventName: string) => void;
    onCancel: () => void;
};

export const EventPickerModal = ({ ast, connection, onConfirm, onCancel }: Props) => {
    const [mode, setMode] = useState<"select" | "create">("select");
    const [selectedEvent, setSelectedEvent] = useState<string>("");
    const [newEventName, setNewEventName] = useState<string>("");

    // Extract existing events from AST
    const existingEvents = useMemo(() => {
        if (!ast?.items) return [];
        return ast.items
            .filter((item) => item.type === "EventDecl")
            // @ts-ignore
            .map((item) => item.name as string);
    }, [ast]);

    // Auto-select first event if available
    useMemo(() => {
        if (existingEvents.length > 0 && !selectedEvent && mode === "select") {
            setSelectedEvent(existingEvents[0]);
        } else if (existingEvents.length === 0 && mode === "select") {
            setMode("create");
        }
    }, [existingEvents, selectedEvent, mode]);

    const handleConfirm = () => {
        if (mode === "select") {
            if (selectedEvent) onConfirm(selectedEvent);
        } else {
            if (newEventName.trim()) onConfirm(newEventName.trim());
        }
    };

    return (
        <div className={styles.modalOverlay}>
            <div className={styles.modalContent}>
                <h3 className={styles.modalTitle}>Add Transition</h3>
                <p className={styles.subtitle}>
                    {connection.source} → {connection.target}
                </p>
                
                <div className={styles.tabs}>
                    <button 
                        className={`${styles.tab} ${mode === "select" ? styles.tabActive : ""}`}
                        onClick={() => setMode("select")}
                        disabled={existingEvents.length === 0}
                    >
                        Existing Event
                    </button>
                    <button 
                        className={`${styles.tab} ${mode === "create" ? styles.tabActive : ""}`}
                        onClick={() => setMode("create")}
                    >
                        New Event
                    </button>
                </div>

                <div className={styles.inputGroup}>
                    {mode === "select" ? (
                        <select 
                            className={styles.selectInput}
                            value={selectedEvent}
                            onChange={(e) => setSelectedEvent(e.target.value)}
                        >
                            {existingEvents.map(evt => (
                                <option key={evt} value={evt}>{evt}</option>
                            ))}
                        </select>
                    ) : (
                        <>
                            <input
                                autoFocus
                                className={styles.textInput}
                                value={newEventName}
                                onChange={(e) => setNewEventName(e.target.value)}
                                placeholder="e.g. key_found"
                                onKeyDown={(e) => {
                                    if (e.key === "Enter") handleConfirm();
                                    if (e.key === "Escape") onCancel();
                                }}
                            />
                            <span className={styles.helpText}>
                                Will be automatically converted to snake_case and added to top-level declarations.
                            </span>
                        </>
                    )}
                </div>

                <div className={styles.buttonRow}>
                    <button className={styles.cancelButton} onClick={onCancel}>
                        Cancel
                    </button>
                    <button 
                        className={styles.confirmButton} 
                        onClick={handleConfirm}
                        disabled={mode === "select" ? !selectedEvent : !newEventName.trim()}
                    >
                        Confirm
                    </button>
                </div>
            </div>
        </div>
    );
};
