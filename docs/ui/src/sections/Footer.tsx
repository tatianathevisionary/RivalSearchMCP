export function Footer() {
  return (
    <footer className="border-t border-line py-10">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-6">
          {/* Logo */}
          <div className="flex items-center gap-1.5">
            <span className="font-display font-extrabold text-sm text-accent">
              RIVAL
            </span>
            <span className="font-display font-extrabold text-sm text-heading">
              SEARCH
            </span>
            <span className="ml-1 text-[9px] font-mono font-semibold text-amber/70 tracking-widest">
              MCP
            </span>
          </div>

          {/* Links */}
          <div className="flex items-center gap-6">
            <a
              href="https://github.com/damionrashford/RivalSearchMCP"
              target="_blank"
              rel="noopener noreferrer"
              className="text-dim hover:text-heading transition-colors font-body text-xs"
            >
              GitHub
            </a>
            <a
              href="https://github.com/damionrashford/RivalSearchMCP/blob/main/LICENSE"
              target="_blank"
              rel="noopener noreferrer"
              className="text-dim hover:text-heading transition-colors font-body text-xs"
            >
              MIT License
            </a>
            <a
              href="https://linkedin.com/in/damion-rashford"
              target="_blank"
              rel="noopener noreferrer"
              className="text-dim hover:text-heading transition-colors font-body text-xs"
            >
              LinkedIn
            </a>
          </div>

          {/* Copyright */}
          <p className="text-faint font-body text-xs">
            Built by{" "}
            <a
              href="https://github.com/damionrashford"
              target="_blank"
              rel="noopener noreferrer"
              className="text-dim hover:text-heading transition-colors"
            >
              Damion Rashford
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
}
