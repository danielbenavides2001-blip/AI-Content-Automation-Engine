import React, { useEffect, useRef } from 'react';
import { useCurrentFrame } from 'remotion';

export const ProceduralGridCanvas: React.FC<{ accentColor?: string }> = ({
  accentColor = '#00f5ff',
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const frame = useCurrentFrame();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const w = canvas.width;
    const h = canvas.height;

    // Dark background
    ctx.fillStyle = '#0a0d14';
    ctx.fillRect(0, 0, w, h);

    // Grid spacing
    const spacing = 80;
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
    ctx.lineWidth = 1;

    for (let x = 0; x <= w; x += spacing) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
      ctx.stroke();
    }

    for (let y = 0; y <= h; y += spacing) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }

    // Crosshairs
    ctx.strokeStyle = 'rgba(0, 245, 255, 0.25)';
    ctx.lineWidth = 1.2;
    const cLen = 6;
    for (let x = spacing; x < w; x += spacing * 2) {
      for (let y = spacing; y < h; y += spacing * 2) {
        ctx.beginPath();
        ctx.moveTo(x - cLen, y);
        ctx.lineTo(x + cLen, y);
        ctx.moveTo(x, y - cLen);
        ctx.lineTo(x, y + cLen);
        ctx.stroke();
      }
    }

    // Floating particles
    for (let i = 0; i < 35; i++) {
      const px = ((i * 137 + frame * 0.4) % w);
      const py = ((i * 193 + Math.sin(frame * 0.02 + i) * 40) % h);
      const alpha = 0.2 + 0.3 * Math.sin(frame * 0.05 + i);

      ctx.fillStyle = i % 2 === 0 ? accentColor : '#fbbf24';
      ctx.globalAlpha = Math.max(0, Math.min(1, alpha));
      ctx.beginPath();
      ctx.arc(px, py, 2.5, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1.0;
  }, [frame, accentColor]);

  return (
    <canvas
      ref={canvasRef}
      width={1080}
      height={1920}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: 1080,
        height: 1920,
        zIndex: 0,
      }}
    />
  );
};
