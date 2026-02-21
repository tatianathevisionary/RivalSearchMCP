import { useInView } from "../hooks/useInView";

interface Client {
  name: string;
  icon: string;
  setup: string;
  config: string;
}

const CLIENTS: Client[] = [
  {
    name: "Claude Desktop",
    icon: "C",
    setup: "Settings → MCP → Add Remote Server",
    config: `Paste URL:
https://RivalSearchMCP.fastmcp.app/mcp`,
  },
  {
    name: "Cursor",
    icon: ">_",
    setup: "One-click install or manual config",
    config: `{
  "mcpServers": {
    "RivalSearchMCP": {
      "url": "https://RivalSearchMCP.fastmcp.app/mcp"
    }
  }
}`,
  },
  {
    name: "VS Code",
    icon: "{ }",
    setup: "Add to .vscode/mcp.json",
    config: `{
  "servers": {
    "RivalSearchMCP": {
      "type": "http",
      "url": "https://RivalSearchMCP.fastmcp.app/mcp"
    }
  }
}`,
  },
  {
    name: "Claude Code",
    icon: "~$",
    setup: "Single CLI command",
    config: `claude mcp add RivalSearchMCP \\
  --url https://RivalSearchMCP.fastmcp.app/mcp`,
  },
];

function ClientCard({ client, index }: { client: Client; index: number }) {
  const { ref, isInView } = useInView();

  return (
    <div
      ref={ref}
      className={`card-hover bg-panel border border-line rounded-xl overflow-hidden transition-all duration-700 ${
        isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
      }`}
      style={{ transitionDelay: `${index * 120}ms` }}
    >
      {/* Client header */}
      <div className="flex items-center gap-3 px-5 py-4 border-b border-line">
        <div className="w-9 h-9 rounded-lg bg-surface border border-line-light flex items-center justify-center">
          <span className="font-mono font-bold text-xs text-amber">
            {client.icon}
          </span>
        </div>
        <div>
          <h3 className="font-body font-semibold text-heading text-sm">
            {client.name}
          </h3>
          <p className="text-dim font-body text-xs">{client.setup}</p>
        </div>
      </div>

      {/* Config */}
      <pre className="px-5 py-4 overflow-x-auto">
        <code className="text-body font-mono text-[11px] sm:text-xs leading-relaxed">
          {client.config}
        </code>
      </pre>
    </div>
  );
}

export function Integrations() {
  const { ref, isInView } = useInView();

  return (
    <section id="integrations" aria-label="Supported AI clients" className="relative py-24 sm:py-32">
      <div className="max-w-7xl mx-auto px-6">
        {/* Section header */}
        <div
          ref={ref}
          className={`text-center mb-16 transition-all duration-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
          }`}
        >
          <span className="font-mono text-xs text-accent tracking-widest uppercase">
            Integrations
          </span>
          <h2 className="font-display font-extrabold text-3xl sm:text-4xl md:text-5xl text-heading tracking-tight mt-3 mb-4">
            Works With Your Tools
          </h2>
          <p className="text-body font-body text-base sm:text-lg max-w-2xl mx-auto">
            Native support for every major MCP-compatible AI client.
            <br className="hidden sm:block" />
            Add one URL and unlock all 10 tools instantly.
          </p>
        </div>

        {/* Client cards grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {CLIENTS.map((client, i) => (
            <ClientCard key={client.name} client={client} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}
