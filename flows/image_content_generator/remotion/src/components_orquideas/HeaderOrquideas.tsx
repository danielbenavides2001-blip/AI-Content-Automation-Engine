import React from 'react';
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface HeaderOrquideasProps {
  breadcrumb?: string;
  category: string;
  categoryHighlight?: string;
  bigMetric?: string;
  metricSubtitle?: string;
  badgeText?: string;
  badgeColor?: string;
}

export const HeaderOrquideas: React.FC<HeaderOrquideasProps> = ({
  breadcrumb = 'ENIGMAIQ  //  BOTÁNICA & ANDES',
  category,
  categoryHighlight,
  bigMetric,
  metricSubtitle,
  badgeText,
  badgeColor = '#00f5ff',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 120 },
  });

  return (
    <div
      style={{
        position: 'absolute',
        top: 65,
        left: 60,
        right: 60,
        zIndex: 50,
      }}
    >
      {/* Breadcrumb */}
      <div
        style={{
          fontFamily: 'Consolas, monospace',
          fontSize: 20,
          letterSpacing: 3,
          color: '#64748b',
          textTransform: 'uppercase',
          marginBottom: 10,
        }}
      >
        {breadcrumb}
      </div>

      {/* Main Headline */}
      <div
        style={{
          display: 'flex',
          alignItems: 'baseline',
          gap: 14,
          transform: `scale(${titleSpring})`,
          transformOrigin: 'left center',
        }}
      >
        <span
          style={{
            fontFamily: 'Bahnschrift, Arial, sans-serif',
            fontSize: 54,
            fontWeight: 900,
            color: '#ffffff',
            letterSpacing: 1,
            textTransform: 'uppercase',
          }}
        >
          {category}
        </span>
        {categoryHighlight && (
          <span
            style={{
              fontFamily: 'Bahnschrift, Arial, sans-serif',
              fontSize: 54,
              fontWeight: 900,
              color: '#d946ef',
              letterSpacing: 1,
              textTransform: 'uppercase',
            }}
          >
            {categoryHighlight}
          </span>
        )}
      </div>

      {/* Big Yellow Metric Counter */}
      {bigMetric && (
        <div style={{ marginTop: 8 }}>
          <div
            style={{
              fontFamily: 'Bahnschrift, Arial, sans-serif',
              fontSize: 92,
              fontWeight: 900,
              color: '#fbbf24',
              lineHeight: 1,
              letterSpacing: -1,
            }}
          >
            {bigMetric}
          </div>
          {metricSubtitle && (
            <div
              style={{
                fontFamily: 'Consolas, monospace',
                fontSize: 24,
                color: '#94a3b8',
                letterSpacing: 1.5,
                marginTop: 6,
              }}
            >
              {metricSubtitle}
            </div>
          )}
        </div>
      )}

      {/* Optional Badge */}
      {badgeText && (
        <div
          style={{
            position: 'absolute',
            top: 25,
            right: 80,
            transform: 'rotate(-3deg)',
            backgroundColor: 'rgba(20, 26, 36, 0.95)',
            border: `2px solid ${badgeColor}`,
            borderRadius: 8,
            padding: '6px 16px',
            color: badgeColor,
            fontFamily: 'Bahnschrift, Arial, sans-serif',
            fontSize: 20,
            fontWeight: 900,
            letterSpacing: 1.5,
            boxShadow: `0 0 15px ${badgeColor}30`,
          }}
        >
          {badgeText}
        </div>
      )}
    </div>
  );
};
