
    import React from 'react';
    import { Outlet } from 'react-router-dom';
    import Navbar from '@/components/Navbar.jsx';
    import Footer from '@/components/Footer.jsx';
    import { Toaster } from '@/components/ui/toaster.jsx';
    import { motion, AnimatePresence } from 'framer-motion';
    import { useLocation } from 'react-router-dom';

    const pageVariants = {
      initial: {
        opacity: 0,
        y: 20,
      },
      in: {
        opacity: 1,
        y: 0,
      },
      out: {
        opacity: 0,
        y: -20,
      },
    };

    const pageTransition = {
      type: 'tween',
      ease: 'anticipate',
      duration: 0.4,
    };

    const Layout = () => {
      const location = useLocation();
      return (
        <div className="flex flex-col min-h-screen bg-gradient-to-br from-background to-slate-900">
          <Navbar />
          <main className="flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <AnimatePresence mode="wait">
              <motion.div
                key={location.pathname}
                initial="initial"
                animate="in"
                exit="out"
                variants={pageVariants}
                transition={pageTransition}
              >
                <Outlet />
              </motion.div>
            </AnimatePresence>
          </main>
          <Footer />
          <Toaster />
        </div>
      );
    };

    export default Layout;
  