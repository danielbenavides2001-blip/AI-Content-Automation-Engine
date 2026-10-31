import React from 'react';
import { useCurrentFrame } from 'remotion';

export const DynamicHeader: React.FC<{
  category: string;
  primaryColor?: string;
  secondaryColor?: string;
}> = ({
  category = 'CIENCIA & GEOGRAFÍA',
  primaryColor = '#00f5ff',
  secondaryColor = '#38bdf8'
}) => {
  const frame = useCurrentFrame();
  const pulse = Math.sin(frame * 0.08) * 0.2 + 0.8;

  return (
    <div
      style={{
        position: 'absolute',
        top: 60,
        left: 45,
        right: 45,
        zIndex: 50,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        fontFamily: "'Bahnschrift', 'Montserrat', Arial, sans-serif",
      }}
    >
      {/* Category Pill */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 12,
          padding: '8px 18px',
          borderRadius: 24,
          backgroundColor: 'rgba(2, 9, 20, 0.75)',
          border: `1px solid ${primaryColor}40`,
          backdropFilter: 'blur(10px)',
          boxShadow: `0 0 20px ${primaryColor}20`,
        }}
      >
        <div
          style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            backgroundColor: primaryColor,
            boxShadow: `0 0 10px ${primaryColor}`,
            opacity: pulse,
          }}
        />
        <span
          style={{
            color: '#ffffff',
            fontSize: 16,
            fontWeight: 800,
            letterSpacing: 2,
            textTransform: 'uppercase',
          }}
        >
          ENIGMAIQ <span style={{ color: primaryColor, margin: '0 4px' }}>//</span> {category}
        </span>
      </div>

      {/* Official IQ Circular Badge */}
      <div
        style={{
          width: 48,
          height: 48,
          borderRadius: '50%',
          border: `2px solid ${primaryColor}90`,
          backgroundColor: '#020914',
          boxShadow: `0 0 16px ${primaryColor}40`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <span
          style={{
            color: primaryColor,
            fontSize: 16,
            fontWeight: 900,
            letterSpacing: 1,
          }}
        >
          IQ
        </span>
      </div>
    </div>
  );
};
