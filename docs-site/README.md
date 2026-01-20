# RivalSearchMCP Documentation Site

A modern, production-grade React documentation site built with Vite, TypeScript, and Tailwind CSS v4.

## 🎨 Design Philosophy

**Dark Terminal Editorial** — A sophisticated dark theme merging hacker/terminal aesthetics with editorial magazine refinement. Features:

- Deep black backgrounds with subtle noise texture
- Glowing red accents (`#dc2626`) against deep blacks  
- Monospace code elements and bold Geist typography
- Dramatic gradient spotlights and layered shadows
- Staggered reveal animations on scroll
- Floating card depth with professional polish

## ⚡ Tech Stack

- **Vite** — Lightning-fast build tool with hot reload
- **React 18** — Modern UI framework with hooks
- **TypeScript** — Type-safe development
- **Tailwind CSS v4** — CSS-first configuration with `@theme`
- **Framer Motion** — Smooth, performant animations
- **React Router v7** — Client-side routing
- **Lucide React** — Beautiful icon system
- **React Syntax Highlighter** — Code block highlighting

## 🚀 Development

```bash
# Install dependencies
npm install

# Start dev server (http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
docs-site/
├── src/
│   ├── components/
│   │   ├── layout/          # Navbar, Sidebar, Footer, Layout
│   │   ├── ui/              # Reusable UI components
│   │   ├── home/            # Homepage sections
│   │   └── docs/            # Documentation components
│   ├── pages/               # Route pages
│   ├── data/                # Tool data and navigation config
│   ├── styles/              # Tailwind v4 configuration
│   └── App.tsx              # Root component
├── public/                  # Static assets
└── index.html               # Entry point
```

## 🎯 Key Features

### Typography
- **Geist** font family for clean, modern aesthetics
- **Geist Mono** for code elements
- Responsive font sizing with fluid typography
- Proper line-height and letter-spacing

### Color System (Tailwind v4)
- Brand colors: Rival Red (`#dc2626`), Rival Amber (`#f59e0b`)
- Semantic surfaces: 5-tier depth system
- Text hierarchy: Primary, Secondary, Muted, Dim
- Custom shadows with glow effects

### Components
- **Hero** — Full-height section with animated stats
- **ToolsGrid** — Category-organized tool cards with hover effects
- **BeforeAfter** — Comparison section highlighting value
- **QuickSetup** — Tabbed installation guide
- **ToolCard** — Hover-aware cards with red accent line
- **CodeBlock** — Syntax-highlighted with copy functionality
- **Callout** — Info/Success/Warning/Danger alerts

### Animations
- Page transitions with Framer Motion
- Staggered reveal on scroll (`whileInView`)
- Hover state micro-interactions
- Smooth tab switching
- Gradient borders with rotation

## 🌐 Deployment

### GitHub Pages

The site is configured for automatic deployment to GitHub Pages:

1. **Push to `main` branch** triggers the deploy workflow
2. **Build process** runs in GitHub Actions
3. **Deploy** to `https://[username].github.io/RivalSearchMCP/`

Configuration files:
- `.github/workflows/deploy.yml` — GitHub Actions workflow
- `public/.nojekyll` — Prevents Jekyll processing
- `public/404.html` — SPA redirect fallback
- `vite.config.ts` — Base path set to `/RivalSearchMCP/`

### Manual Deployment

```bash
# Build the site
npm run build

# The dist/ folder contains the static site
# Deploy dist/ to any static hosting service
```

## 🎨 Design System

### CSS Variables (Tailwind v4 @theme)

```css
--color-rival-black: #0a0a0a
--color-rival-red: #dc2626
--color-rival-amber: #f59e0b
--color-surface-0 through -4: Depth layers
--shadow-glow: Red glow effect
--shadow-card: Floating card shadow
```

### Component Patterns

**Tool Card Hover State:**
- Red accent line slides in from left
- Icon scales and adds glow
- Card lifts with enhanced shadow

**Code Block:**
- Terminal-style with macOS dots
- Copy button on hover
- Language badge in corner
- Syntax highlighting with red/amber accents

**Callout:**
- Type-specific icons and colors
- Optional title with semantic styling
- Consistent padding and borders

## 📊 Content

All tool data is centralized in `src/data/tools.ts`:

```typescript
interface Tool {
  id: string
  name: string
  displayName: string
  description: string
  icon: LucideIcon
  category: 'search' | 'content' | 'research'
  sources: string[]
  parameters: Parameter[]
  nextSteps: NextStep[]
}
```

Navigation structure defined in `src/data/navigation.ts`.

## 🔧 Customization

### Adding a New Tool

1. Add tool data to `src/data/tools.ts`
2. Tool detail page auto-generates from template
3. Updates appear in:
   - Homepage tools grid
   - Tools overview page
   - Sidebar navigation
   - Comparison table

### Modifying Colors

Edit `src/styles/app.css` in the `@theme` block:

```css
@theme {
  --color-rival-red: #your-color;
}
```

### Adding Pages

1. Create component in `src/pages/`
2. Add route in `src/App.tsx`
3. Update navigation in `src/data/navigation.ts`

## 🏆 Best Practices

- **Accessibility**: Proper semantic HTML, ARIA labels, keyboard navigation
- **Performance**: Code splitting, lazy loading, optimized images
- **SEO**: Meta tags, proper heading hierarchy, descriptive links
- **Responsiveness**: Mobile-first design, fluid typography
- **DX**: TypeScript for type safety, ESLint for code quality

## 📝 License

Part of RivalSearchMCP project. See root LICENSE for details.

---

Built with ❤️ using modern web technologies. Designed for exceptional developer experience.
