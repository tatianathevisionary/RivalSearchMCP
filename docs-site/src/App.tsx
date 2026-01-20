import { Routes, Route } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import Layout from './components/layout/Layout'
import Home from './pages/Home'
import Tools from './pages/Tools'
import ToolDetail from './pages/ToolDetail'
import GettingStarted from './pages/GettingStarted'
import UserGuide from './pages/UserGuide'
import Examples from './pages/Examples'

function App() {
  return (
    <>
      <div className="noise-overlay" />
      <AnimatePresence mode="wait">
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="tools" element={<Tools />} />
            <Route path="tools/:toolId" element={<ToolDetail />} />
            <Route path="getting-started" element={<GettingStarted />} />
            <Route path="guide" element={<UserGuide />} />
            <Route path="examples" element={<Examples />} />
          </Route>
        </Routes>
      </AnimatePresence>
    </>
  )
}

export default App
