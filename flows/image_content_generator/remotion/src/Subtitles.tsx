import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import React from 'react';
import { DollarSign, TrendingUp, AlertTriangle, Briefcase, ShieldCheck } from 'lucide-react';

interface Word {
  text: string;
  start: number; // in ms
  end: number; // in ms
}

const IconMap: Record<string, React.ReactNode> = {
  'dinero': <DollarSign size={140} color="#fbbf24" />,
  'rico': <DollarSign size={140} color="#fbbf24" />,
  'pobre': <AlertTriangle size={140} color="#ef4444" />,
  'inversión': <TrendingUp size={140} color="#10b981" />,
  'negocio': <Briefcase size={140} color="#3b82f6" />,
  'seguridad': <ShieldCheck size={140} color="#8b5cf6" />,
};

// Money Chart Animation Component
const MoneyChart: React.FC<{ progress: number }> = ({ progress }) => {
  return (
    <div style={{ width: 400, height: 200, backgroundColor: 'rgba(0,0,0,0.5)', borderRadius: 20, padding: 20, display: 'flex', alignItems: 'flex-end', gap: 10 }}>
      {[0.2, 0.4, 0.3, 0.6, 0.8, 1.0].map((h, i) => {
        const currentH = Math.min(h, progress * (i + 1) / 6) * 100;
        return (
          <div key={i} style={{ flex: 1, height: `${currentH}%`, backgroundColor: '#10b981', borderRadius: 5, transition: 'height 0.1s' }} />
        );
      })}
    </div>
  );
};

export const Subtitles: React.FC<{ words: Word[] }> = ({ words }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Group words into phrases of 4 words (2 lines of 2 words)
  const phrases: { words: Word[], start: number, end: number }[] = [];
  for (let i = 0; i < words.length; i += 4) {
    const chunk = words.slice(i, i + 4);
    phrases.push({
      words: chunk,
      start: chunk[0].start,
      end: chunk[chunk.length - 1].end
    });
  }

  return (
    <div style={{ flex: 1, backgroundColor: 'transparent', position: 'relative', overflow: 'hidden' }}>
      {phrases.map((phrase, pi) => {
        const startFrame = (phrase.start / 1000) * fps;
        const endFrame = (phrase.end / 1000) * fps;
        const isActivePhrase = frame >= startFrame && frame < endFrame;

        if (!isActivePhrase) return null;

        return (
          <div key={pi} style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            
            {/* Money Chart Animation */}
            <div style={{ marginBottom: 40 }}>
              {phrase.words.map((w, wi) => {
                const clean = w.text.toLowerCase().replace(/[.,!]/g, '');
                const isShowing = frame >= (w.start / 1000) * fps && frame < (w.end / 1000) * fps;
                if (!isShowing) return null;
                const scale = spring({ frame: frame - (w.start / 1000) * fps, fps, config: { stiffness: 200 } });
                if (clean === 'dinero' || clean === 'rico' || clean === 'inversión' || clean === 'crecimiento') {
                    return <MoneyChart key={wi} progress={scale} />;
                }
                return null;
              })}
            </div>

            {/* Subtitle Block (Semi-transparent black box) */}
            <div style={{ 
                backgroundColor: 'rgba(0, 0, 0, 0.65)', 
                padding: '15px 40px', 
                borderRadius: '8px', 
                display: 'flex', 
                flexDirection: 'column',
                alignItems: 'center',
                maxWidth: '85%',
                boxShadow: '0 5px 20px rgba(0,0,0,0.4)',
                border: '1px solid rgba(255,255,255,0.1)'
            }}>
              <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '15px 30px' }}>
                {phrase.words.map((word, wi) => {
                  const wStart = (word.start / 1000) * fps;
                  const wEnd = (word.end / 1000) * fps;
                  const isCurrentWord = frame >= wStart && frame < wEnd;

                  return (
                    <span
                      key={wi}
                      style={{
                        fontSize: 95,
                        fontFamily: 'Impact, sans-serif',
                        fontWeight: 'bold',
                        color: isCurrentWord ? '#FFFF00' : '#FFFFFF',
                        textTransform: 'uppercase',
                        display: 'inline-block',
                        lineHeight: 1.1,
                        textShadow: '2px 2px 4px rgba(0,0,0,0.5)'
                      }}
                    >
                      {word.text}
                    </span>
                  );
                })}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
