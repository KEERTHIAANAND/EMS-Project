
import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button.jsx';
import { motion } from 'framer-motion';
import { AlertTriangle } from 'lucide-react';

const NotFoundPage = () => {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col items-center justify-center min-h-[calc(100vh-200px)] text-center px-4"
    >
      <AlertTriangle className="h-24 w-24 text-destructive mb-8 animate-pulse" />
      <h1 className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-orange-500 mb-4">
        404
      </h1>
      <h2 className="text-3xl font-semibold text-foreground mb-3">Oops! Page Not Found</h2>
      <p className="text-lg text-muted-foreground mb-8 max-w-md">
        The page you're looking for doesn't exist or has been moved. Let's get you back on track.
      </p>
      <img alt="Confused robot looking at a map" className="w-full max-w-xs h-auto mb-8 rounded-lg shadow-xl" src="https://images.unsplash.com/photo-1672789210128-c9ac59de248f" />
      <Button asChild variant="premium" size="lg">
        <Link to="/">Go Back to Homepage</Link>
      </Button>
    </motion.div>
  );
};

export default NotFoundPage;
