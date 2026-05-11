import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import React from 'react';
import { DollarSign, TrendingUp, AlertTriangle, Briefcase, ShieldCheck } from 'lucide-react';

interface Word {
  text: string;
  start: number; // in ms
  end: number; // in ms
}

const IconMap: Record<string, React.ReactNode> = {
  'dinero': <DollarSign size={120} color="#fbbf24" />,
  'rico': <DollarSign size={120} color="#fbbf24" />,
  'pobre': <AlertTriangle size={120} color="#ef4444" />,
  'inversión': <TrendingUp size={120} color="#10b981" />,
  'negocio': <Briefcase size={120} color="#3b82f6" />,
  'seguridad': <ShieldCheck size={120} color="#8b5cf6" />,
};

export const Subtitles: React.FC<{ words: Word[] }> = ({ words }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ flex: 1, backgroundColor: 'transparent', position: 'relative' }}>
      {words.map((word, i) => {
        const startFrame = (word.start / 1000) * fps;
        const endFrame = (word.end / 1000) * fps;
        const isActive = frame >= startFrame && frame < endFrame;

        if (!isActive) return null;

        const cleanWord = word.text.toLowerCase().replace(/[.,!]/g, '');
        const icon = IconMap[cleanWord];

        const scale = spring({
          frame: frame - startFrame,
          fps,
          config: { stiffness: 200, damping: 12 },
        });

        return (
          <div key={i} style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            {icon && (
              <div style={{ marginBottom: 40, transform: `scale(${scale * 1.2})` }}>
                {icon}
              </div>
            )}
            <div
              style={{
                fontSize: 110,
                fontFamily: 'Impact, sans-serif',
                color: 'white',
                textShadow: '0 0 10px black, 0 0 20px black, 5px 5px 0px #000',
                transform: `scale(${scale})`,
                textTransform: 'uppercase',
                padding: '0 40px',
                textAlign: 'center'
              }}
            >
              {word.text}
            </div>
          </div>
        );
      })}
    </div>
  );
};
