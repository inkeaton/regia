// src/export/toImage.ts
import { toPng, toSvg } from "html-to-image";

// ==============================================================================
// IMAGE EXPORT UTILITIES
// ==============================================================================

/**
 * Downloads a given HTML element as an image file.
 * * @param dataUrl - The base64 encoded image string.
 * @param filename - The name of the file to save.
 */
const downloadImage = (dataUrl: string, filename: string) => {
    const a = document.createElement("a");
    a.setAttribute("download", filename);
    a.setAttribute("href", dataUrl);
    a.click();
};

/**
 * Captures the React Flow canvas and exports it.
 * * @param format - 'png' or 'svg'.
 * @param plotName - Used to name the downloaded file.
 */
export const exportCanvas = async (format: "png" | "svg", plotName: string) => {
    // We target the internal div that React Flow uses to hold the nodes
    const element = document.querySelector(".react-flow__viewport") as HTMLElement;
    if (!element) return;

    // Temporarily reset transforms so the image captures the whole graph cleanly
    const oldTransform = element.style.transform;
    element.style.transform = "translate(0px, 0px) scale(1)";

    try {
        if (format === "png") {
            const dataUrl = await toPng(element, { 
                backgroundColor: "#ffffff",
                pixelRatio: 2 // High-res output
            });
            downloadImage(dataUrl, `${plotName}_plot.png`);
        } else {
            const dataUrl = await toSvg(element, { 
                backgroundColor: "#ffffff"
            });
            downloadImage(dataUrl, `${plotName}_plot.svg`);
        }
    } catch (err) {
        console.error("Failed to export image", err);
    } finally {
        // Restore the user's zoom/pan position
        element.style.transform = oldTransform;
    }
};