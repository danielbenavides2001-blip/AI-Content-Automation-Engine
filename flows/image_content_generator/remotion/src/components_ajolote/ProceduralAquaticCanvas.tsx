import React, { useEffect, useRef } from 'react';
import { useCurrentFrame } from 'remotion';

export const ProceduralAquaticCanvas: React.FC<{ accentColor?: string }> = ({
  accentColor = '#ec4899',
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

    // Dark aquatic radial gradient
    const grad = ctx.createRadialGradient(w / 2, h / 2, 200, w / 2, h / 2, 1100);
    grad.addColorStop(0, '#0c1524');
    grad.addColorStop(1, '#05080f');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);

    // Subtle biological coordinate grid
    const spacing = 80;
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.035)';
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

    // Grid crosshairs
    ctx.strokeStyle = 'rgba(236, 72, 153, 0.25)';
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

    // Water caustics wave lines
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.04)';
    ctx.lineWidth = 3;
    for (let j = 0; j < 6; j++) {
      ctx.beginPath();
      const waveY = (j * 320 + frame * 0.8) % (h + 200) - 100;
      for (let x = 0; x <= w; x += 30) {
        const offset = Math.sin((x * 0.015) + (frame * 0.04) + j) * 25;
        if (x === 0) ctx.moveTo(x, waveY + offset);
        else ctx.lineTo(x, waveY + offset);
      }
      ctx.stroke();
    }

    // Floating bio-luminescent plankton / micro-bubbles
    for (let i = 0; i < 40; i++) {
      const px = (i * 127 + frame * 0.45) % w;
      const py = (h - ((i * 163 + frame * 1.2) % (h + 100))) % h;
      const r = (i % 3) + 1.2;
      const alpha = 0.25 + 0.35 * Math.sin(frame * 0.05 + i);

      ctx.fillStyle = i % 2 === 0 ? `rgba(236, 72, 153, ${alpha})` : `rgba(56, 189, 248, ${alpha})`;
      ctx.beginPath();
      ctx.arc(px, py, r, 0, Math.PI * 2);
      ctx.fill();
    }
  }, [frame]);

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
        zIndex: 1,
      }}
    />
  );
};
