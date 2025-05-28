
    import React from 'react';
    import { Link, NavLink, useNavigate } from 'react-router-dom';
    import { Button } from '@/components/ui/button.jsx';
    import { CalendarDays, PlusCircle, LayoutDashboard, LogOut } from 'lucide-react';
    import { motion } from 'framer-motion';

    const Navbar = () => {
      const navigate = useNavigate();

      const handleLogout = async () => {
        try {
          // Call Django logout endpoint
          const token = localStorage.getItem('token');
          if (token) {
            await fetch('http://localhost:8000/api/auth/logout/', {
              method: 'POST',
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
              }
            });
          }
        } catch (error) {
          console.error('Logout error:', error);
        } finally {
          // Clear local storage regardless of API call result
          localStorage.removeItem('isAuthenticated');
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          navigate('/sign-in');
        }
      };

      const navLinkClasses = ({ isActive }) =>
        `flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors duration-150 ease-in-out
        ${isActive
          ? 'bg-primary/20 text-primary'
          : 'text-foreground/80 hover:bg-foreground/10 hover:text-foreground'
        }`;

      return (
        <motion.nav
          initial={{ y: -100 }}
          animate={{ y: 0 }}
          transition={{ type: 'spring', stiffness: 120, damping: 20 }}
          className="bg-background/80 backdrop-blur-md shadow-lg sticky top-0 z-50"
        >
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-20">
              <Link to="/" className="flex items-center space-x-2">
                <motion.div whileHover={{ rotate: 360, scale: 1.1 }} transition={{ duration: 0.5 }}>
                  <CalendarDays className="h-10 w-10 text-primary" />
                </motion.div>
                <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
                  EventHorizon
                </span>
              </Link>
              <div className="hidden md:flex items-center space-x-4">
                <NavLink to="/" className={navLinkClasses}>
                  <CalendarDays className="h-5 w-5 mr-2" />
                  Events
                </NavLink>
                <NavLink to="/admin" className={navLinkClasses}>
                  <LayoutDashboard className="h-5 w-5 mr-2" />
                  Admin
                </NavLink>
                <Button asChild variant="premium" size="sm">
                  <Link to="/create-event">
                    <PlusCircle className="h-5 w-5 mr-2" />
                    Create Event
                  </Link>
                </Button>
                <Button onClick={handleLogout} variant="outline" size="sm">
                  <LogOut className="h-5 w-5 mr-2" />
                  Logout
                </Button>
              </div>
              <div className="md:hidden">
                {/* Mobile menu button can be added here */}
                <Button asChild variant="ghost" size="icon">
                  <Link to="/create-event">
                    <PlusCircle className="h-6 w-6" />
                  </Link>
                </Button>
              </div>
            </div>
          </div>
        </motion.nav>
      );
    };

    export default Navbar;
