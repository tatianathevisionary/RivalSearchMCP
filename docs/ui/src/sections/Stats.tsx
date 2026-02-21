import { useInView } from "../hooks/useInView";

const STATS = [
  { value: "10", label: "Research Tools", accent: "text-accent" },
  { value: "20+", label: "Data Sources", accent: "text-amber" },
  { value: "0", label: "API Keys Required", accent: "text-emerald-400" },
  { value: "MIT", label: "Licensed", accent: "text-heading" },
];

export function Stats() {
  const { ref, isInView } = useInView();

  return (
    <section ref={ref} aria-label="Key statistics" className="relative py-6 border-y border-line">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-0 md:divide-x md:divide-line">
          {STATS.map((stat, i) => (
            <div
              key={stat.label}
              className={`text-center py-4 transition-all duration-700 ${
                isInView
                  ? "opacity-100 translate-y-0"
                  : "opacity-0 translate-y-4"
              }`}
              style={{ transitionDelay: `${i * 100}ms` }}
            >
              <div
                className={`font-display font-extrabold text-3xl sm:text-4xl tracking-tight ${stat.accent}`}
              >
                {stat.value}
              </div>
              <div className="text-dim font-body text-xs tracking-wider uppercase mt-1">
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
