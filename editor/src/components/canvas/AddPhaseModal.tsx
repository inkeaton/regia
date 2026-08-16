import { useState } from "react";
import styles from "./AddPhaseModal.module.css";

type Props = {
    onConfirm: (name: string) => void;
    onCancel: () => void;
};

export const AddPhaseModal = ({ onConfirm, onCancel }: Props) => {
    const [name, setName] = useState("");

    const handleConfirm = () => {
        if (!name.trim()) return;
        onConfirm(name);
    };

    return (
        <div className={styles.modalOverlay}>
            <div className={styles.modalContent}>
                <h3 className={styles.modalTitle}>Add New Phase</h3>
                
                <div className={styles.inputGroup}>
                    <label className={styles.inputLabel}>Phase Name</label>
                    <input
                        autoFocus
                        className={styles.textInput}
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="e.g. performing"
                        onKeyDown={(e) => {
                            if (e.key === "Enter") handleConfirm();
                            if (e.key === "Escape") onCancel();
                        }}
                    />
                    <span className={styles.helpText}>
                        Will be automatically converted to snake_case.
                    </span>
                </div>

                <div className={styles.buttonRow}>
                    <button className={styles.cancelButton} onClick={onCancel}>
                        Cancel
                    </button>
                    <button 
                        className={styles.confirmButton} 
                        onClick={handleConfirm}
                        disabled={!name.trim()}
                    >
                        Create
                    </button>
                </div>
            </div>
        </div>
    );
};
