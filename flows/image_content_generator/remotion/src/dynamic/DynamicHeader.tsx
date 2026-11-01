import React from 'react';
import { useCurrentFrame } from 'remotion';

export const DynamicHeader: React.FC<{
  category: string;
  primaryColor?: string;
  secondaryColor?: string;
}> = ({
  category = 'CIENCIA & GEOGRAFÍA',
  primaryColor = '#00f5ff',
  secondaryColor = '#38bdf8',
}) => {
  const frame = useCurrentFrame();
  const pulse = Math.sin(frame * 0.08) * 0.2 + 0.8;

  return (
    <div
      style={{
        position: 'absolute',
        top: 65,
        left: 50,
        right: 50,
        zIndex: 60,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        fontFamily: "'Bahnschrift', 'Montserrat', Arial, sans-serif",
      }}
    >
      {/* Official EnigmaIQ Gold Header Pill (Exact Reference Style) */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 10,
          padding: '8px 24px',
          borderRadius: 24,
          backgroundColor: '#f59e0b',
          boxShadow: '0 0 25px rgba(245, 158, 11, 0.45)',
        }}
      >
        <span
          style={{
            color: '#020914',
            fontSize: 18,
            fontWeight: 900,
            letterSpacing: 2,
            textTransform: 'uppercase',
          }}
        >
          ENIGMAIQ
        </span>
      </div>

      {/* Secondary Category HUD Badge */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 10,
          padding: '7px 18px',
          borderRadius: 20,
          backgroundColor: 'rgba(11, 23, 42, 0.85)',
          border: '1.5px solid rgba(245, 158, 11, 0.4)',
          backdropFilter: 'blur(10px)',
          boxShadow: '0 0 15px rgba(0, 0, 0, 0.5)',
        }}
      >
        <div
          style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            backgroundColor: '#f59e0b',
            boxShadow: '0 0 10px #f59e0b',
            opacity: pulse,
          }}
        />
        <span
          style={{
            color: '#e2e8f0',
            fontSize: 14,
            fontWeight: 800,
            letterSpacing: 1.5,
            textTransform: 'uppercase',
          }}
        >
          {category}
        </span>
      </div>
    </div>
  );
};
