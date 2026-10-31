import React from 'react';
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface HeaderAjoloteProps {
  breadcrumb?: string;
  category: string;
  categoryHighlight?: string;
  bigMetric?: string;
  metricSubtitle?: string;
  badgeText?: string;
  badgeColor?: string;
}

export const HeaderAjolote: React.FC<HeaderAjoloteProps> = ({
  breadcrumb = 'ENIGMAIQ  //  BIOLOGÍA EXTRAORDINARIA',
  category,
  categoryHighlight,
  bigMetric,
  metricSubtitle,
  badgeText,
  badgeColor = '#ec4899',
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
        top: 60,
        left: 60,
        right: 60,
        zIndex: 50,
      }}
    >
      {/* Top Row: Breadcrumb & Floating Status Badge */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 8,
          paddingRight: 110, // Avoid watermark logo
        }}
      >
        <div
          style={{
            fontFamily: 'Consolas, monospace',
            fontSize: 18,
            letterSpacing: 3,
            color: '#64748b',
            textTransform: 'uppercase',
          }}
        >
          {breadcrumb}
        </div>

        {badgeText && (
          <div
            style={{
              backgroundColor: 'rgba(20, 26, 36, 0.95)',
              border: `1.5px solid ${badgeColor}`,
              borderRadius: 6,
              padding: '4px 14px',
              color: badgeColor,
              fontFamily: 'Bahnschrift, Arial, sans-serif',
              fontSize: 16,
              fontWeight: 800,
              letterSpacing: 1.5,
              boxShadow: `0 0 12px ${badgeColor}30`,
              transform: 'rotate(-2deg)',
            }}
          >
            {badgeText}
          </div>
        )}
      </div>

      {/* Main Headline */}
      <div
        style={{
          display: 'flex',
          alignItems: 'baseline',
          gap: 12,
          transform: `scale(${titleSpring})`,
          transformOrigin: 'left center',
        }}
      >
        <span
          style={{
            fontFamily: 'Bahnschrift, Arial, sans-serif',
            fontSize: 48,
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
              fontSize: 48,
              fontWeight: 900,
              color: '#ec4899',
              letterSpacing: 1,
              textTransform: 'uppercase',
            }}
          >
            {categoryHighlight}
          </span>
        )}
      </div>

      {/* High-Contrast Yellow Metric */}
      {bigMetric && (
        <div style={{ marginTop: 4 }}>
          <div
            style={{
              fontFamily: 'Bahnschrift, Arial, sans-serif',
              fontSize: 76,
              fontWeight: 900,
              color: '#fbbf24',
              lineHeight: 1.05,
              letterSpacing: -1,
            }}
          >
            {bigMetric}
          </div>
          {metricSubtitle && (
            <div
              style={{
                fontFamily: 'Consolas, monospace',
                fontSize: 21,
                color: '#94a3b8',
                letterSpacing: 1.2,
                marginTop: 4,
              }}
            >
              {metricSubtitle}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
