<script lang="ts">
  export let segmentProportions: Record<string, number> = {};

  // Generate colors for each segment
  const colors = [
    "#4F46E5",
    "#F59E42",
    "#10B981",
    "#F43F5E",
    "#6366F1",
    "#FBBF24",
    "#22D3EE",
    "#A78BFA",
    "#F472B6",
    "#34D399",
  ];
  const keys = Object.keys(segmentProportions);
  const values = Object.values(segmentProportions);

  // Calculate start/end angles for each segment
  let angles = [];
  let acc = 0;
  for (let i = 0; i < values.length; i++) {
    const start = acc;
    const end = acc + values[i] * 360;
    angles.push({ start, end });
    acc = end;
  }

  function describeArc(
    cx: number,
    cy: number,
    r: number,
    startAngle: number,
    endAngle: number
  ) {
    const start = polarToCartesian(cx, cy, r, endAngle);
    const end = polarToCartesian(cx, cy, r, startAngle);
    const largeArcFlag = endAngle - startAngle > 180 ? 1 : 0;
    return [
      "M",
      start.x,
      start.y,
      "A",
      r,
      r,
      0,
      largeArcFlag,
      0,
      end.x,
      end.y,
      "L",
      cx,
      cy,
      "Z",
    ].join(" ");
  }

  function polarToCartesian(cx: number, cy: number, r: number, angle: number) {
    const rad = ((angle - 90) * Math.PI) / 180.0;
    return {
      x: cx + r * Math.cos(rad),
      y: cy + r * Math.sin(rad),
    };
  }
</script>

<svg width="300" height="300" viewBox="0 0 300 300">
  {#each angles as a, i}
    <path
      d={describeArc(150, 150, 120, a.start, a.end)}
      fill={colors[i % colors.length]}
      stroke="#fff"
      stroke-width="2"
    />
  {/each}
  {#each keys as key, i}
    <rect
      x="220"
      y={30 + i * 30}
      width="20"
      height="20"
      fill={colors[i % colors.length]}
    />
    <text x="250" y={45 + i * 30} font-size="16">{key}</text>
  {/each}
</svg>
