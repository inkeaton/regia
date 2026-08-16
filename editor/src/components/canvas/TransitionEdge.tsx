import { BaseEdge, EdgeLabelRenderer, getBezierPath, type EdgeProps } from 'reactflow';

export const TransitionEdge = ({
    sourceX,
    sourceY,
    targetX,
    targetY,
    sourcePosition,
    targetPosition,
    style = {},
    markerEnd,
    label,
    data
}: EdgeProps) => {
    const [edgePath, labelX, labelY] = getBezierPath({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
    });

    // Stagger labels vertically to prevent overlap when edges cross
    const slot = data?.slot || 0;
    
    // Slot 0 (straight line): no offset
    // Slot 1 (right arc): shift up
    // Slot 2 (left arc): shift down
    // Slot 3 (right arc 2): shift further up
    let yOffset = 0;
    if (slot % 2 === 1) {
        yOffset = -25 * Math.ceil(slot / 2);
    } else if (slot > 0) {
        yOffset = 25 * Math.ceil(slot / 2);
    }

    return (
        <>
            <BaseEdge path={edgePath} markerEnd={markerEnd} style={style} />
            {label && (
                <EdgeLabelRenderer>
                    <div
                        style={{
                            position: 'absolute',
                            transform: `translate(-50%, -50%) translate(${labelX}px, ${labelY + yOffset}px)`,
                            background: 'var(--color-edge-label-bg)',
                            color: style.stroke,
                            padding: '4px 8px',
                            borderRadius: '4px',
                            fontSize: '12px',
                            fontWeight: 700,
                            pointerEvents: 'all',
                            opacity: 0.9,
                        }}
                        className="nodrag nopan"
                    >
                        {label}
                    </div>
                </EdgeLabelRenderer>
            )}
        </>
    );
};
