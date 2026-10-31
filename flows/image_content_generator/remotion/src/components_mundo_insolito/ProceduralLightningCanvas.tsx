import React, { useEffect, useRef } from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';

interface LightningProps {
  intensity?: number;
  strikeProbability?: number;
}

export const ProceduralLightningCanvas: React.FC<LightningProps> = ({
  intensity = 1.0,
  strikeProbability = 0.15,
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, width, height);

    // 1. Draw base technical grid
    ctx.fillStyle = '#0d0f12';
    ctx.fillRect(0, 0, width, height);

    const gridSpacing = 80;
    ctx.strokeStyle = 'rgba(28, 35, 48, 0.45)';
    ctx.lineWidth = 1;

    for (let x = 0; x < width; x += gridSpacing) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    for (let y = 0; y < height; y += gridSpacing) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    // Grid crosshairs
    const crossLen = 6;
    ctx.strokeStyle = 'rgba(0, 245, 255, 0.3)';
    for (let x = 0; x < width; x += gridSpacing * 2) {
      for (let y = 0; y < height; y += gridSpacing * 2) {
        ctx.beginPath();
        ctx.moveTo(x - crossLen, y);
        ctx.lineTo(x + crossLen, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x, y - crossLen);
        ctx.lineTo(x, y + crossLen);
        ctx.stroke();
      }
    }

    // 2. Determine if lightning strikes on this frame
    // Pseudo-random deterministic noise based on frame
    const hash = Math.sin(frame * 12.9898 + 78.233) * 43758.5453;
    const pseudoRand = hash - Math.floor(hash);

    const isStrike = pseudoRand < strikeProbability;
    const isAfterglow = Math.sin((frame - 1) * 12.9898 + 78.233) % 1 < strikeProbability;

    if (isStrike || isAfterglow) {
      const flashAlpha = isStrike ? 0.35 * intensity : 0.12 * intensity;

      // Ambient sky flash
      const skyGradient = ctx.createRadialGradient(
        width * 0.5,
        height * 0.3,
        50,
        width * 0.5,
        height * 0.5,
        width * 0.8
      );
      skyGradient.addColorStop(0, `rgba(168, 85, 247, ${flashAlpha})`);
      skyGradient.addColorStop(0.5, `rgba(0, 245, 255, ${flashAlpha * 0.6})`);
      skyGradient.addColorStop(1, 'rgba(0, 0, 0, 0)');

      ctx.fillStyle = skyGradient;
      ctx.fillRect(0, 0, width, height);

      // Recursive Midpoint Displacement Lightning
      const drawBolt = (
        x1: number,
        y1: number,
        x2: number,
        y2: number,
        displace: number,
        branchDepth: number
      ) => {
        if (displace < 5 || branchDepth <= 0) {
          ctx.beginPath();
          ctx.moveTo(x1, y1);
          ctx.lineTo(x2, y2);
          ctx.stroke();
          return;
        }

        const midX = (x1 + x2) / 2 + (Math.sin(frame * 7 + x1 + y1) * displace);
        const midY = (y1 + y2) / 2 + (Math.cos(frame * 5 + x2 + y2) * displace * 0.5);

        drawBolt(x1, y1, midX, midY, displace / 1.8, branchDepth - 1);
        drawBolt(midX, midY, x2, y2, displace / 1.8, branchDepth - 1);

        // Branching forks
        if (branchDepth > 2 && Math.sin(x1 * 0.1 + frame) > 0.1) {
          const forkAngle = Math.PI / 4 + (Math.sin(frame + y1) * 0.3);
          const forkLen = 120 * (branchDepth / 4);
          const forkX = midX + Math.cos(forkAngle) * forkLen;
          const forkY = midY + Math.sin(forkAngle) * forkLen;
          drawBolt(midX, midY, forkX, forkY, displace / 2.2, branchDepth - 2);
        }
      };

      // Draw primary bolt
      ctx.save();
      ctx.shadowBlur = 25;
      ctx.shadowColor = '#00f5ff';
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 3.5;

      const startX = width * (0.35 + (Math.sin(frame * 3) * 0.3));
      const startY = height * 0.12;
      const endX = width * (0.45 + (Math.cos(frame * 2) * 0.25));
      const endY = height * 0.72;

      drawBolt(startX, startY, endX, endY, 90, 5);

      // Core electric cyan pass
      ctx.strokeStyle = 'rgba(0, 245, 255, 0.85)';
      ctx.lineWidth = 2;
      ctx.shadowBlur = 10;
      ctx.shadowColor = '#a855f7';
      drawBolt(startX, startY, endX, endY, 90, 5);

      ctx.restore();
    }

    // 3. Ambient atmospheric particles (water vapor and charged ions)
    const particleCount = 45;
    ctx.fillStyle = 'rgba(0, 245, 255, 0.4)';
    for (let i = 0; i < particleCount; i++) {
      const px = ((i * 137.5 + frame * 0.8) % width);
      const py = ((i * 91.3 + Math.sin(frame * 0.03 + i) * 30 + frame * 0.5) % height);
      const pr = 1 + (i % 3);
      ctx.beginPath();
      ctx.arc(px, py, pr, 0, Math.PI * 2);
      ctx.fill();
    }
  }, [frame, width, height, intensity, strikeProbability]);

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: 0,
      }}
    />
  );
};
