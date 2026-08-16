import { useState, useCallback } from "react";
import { type Connection } from "reactflow";
import { useStore } from "../store/useStore";
import { addPhase, addTransition } from "../services/codeTransformer";

export type PendingConnection = {
    source: string;
    target: string;
};

export const useGraphEditing = () => {
    const { ast, code, setCode } = useStore();
    const [pendingConnection, setPendingConnection] = useState<PendingConnection | null>(null);
    const [isAddingPhase, setIsAddingPhase] = useState<boolean>(false);

    const onConnect = useCallback((connection: Connection) => {
        if (!connection.source || !connection.target) return;
        
        // Prevent self-connections
        if (connection.source === connection.target) return;

        setPendingConnection({
            source: connection.source,
            target: connection.target,
        });
    }, []);

    const onPaneDoubleClick = useCallback(() => {
        setIsAddingPhase(true);
    }, []);

    const cancelPending = useCallback(() => {
        setPendingConnection(null);
        setIsAddingPhase(false);
    }, []);

    const confirmAddPhase = useCallback((phaseName: string) => {
        if (!ast || !code) return;
        const newCode = addPhase(code, ast, phaseName);
        setCode(newCode);
        setIsAddingPhase(false);
    }, [ast, code, setCode]);

    const confirmAddTransition = useCallback((eventName: string) => {
        if (!ast || !code || !pendingConnection) return;
        const newCode = addTransition(
            code,
            ast,
            pendingConnection.source,
            pendingConnection.target,
            eventName
        );
        setCode(newCode);
        setPendingConnection(null);
    }, [ast, code, pendingConnection, setCode]);

    return {
        onConnect,
        onPaneDoubleClick,
        pendingConnection,
        isAddingPhase,
        cancelPending,
        confirmAddPhase,
        confirmAddTransition,
    };
};
