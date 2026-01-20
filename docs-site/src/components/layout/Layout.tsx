import { Outlet, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import Navbar from './Navbar'
import Sidebar from './Sidebar'
import Footer from './Footer'

export default function Layout() {
  const location = useLocation()
  const isHomePage = location.pathname === '/'

  return (
    <div className="min-h-screen flex flex-col gradient-mesh">
      <Navbar />
      
      <div className="flex-1">
        {isHomePage ? (
          // Homepage - full width, no sidebar
          <motion.main
            key={location.pathname}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
            className="pt-20"
          >
            <Outlet />
          </motion.main>
        ) : (
          // Documentation pages - with sidebar
          <div className="mx-auto max-w-7xl px-6 sm:px-8 lg:px-12 pt-28 pb-16">
            <div className="flex gap-12">
              <Sidebar />
              
              <motion.main
                key={location.pathname}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.5 }}
                className="flex-1 min-w-0"
              >
                <Outlet />
              </motion.main>
            </div>
          </div>
        )}
      </div>

      <Footer />
    </div>
  )
}
