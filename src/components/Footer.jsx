
    import React from 'react';
    import { motion } from 'framer-motion';

    const Footer = () => {
      return (
        <motion.footer 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="bg-background/50 border-t border-border mt-12 py-8 text-center"
        >
          <p className="text-sm text-muted-foreground">
            &copy; {new Date().getFullYear()} EventHorizon. All rights reserved.
          </p>
          <p className="text-xs text-muted-foreground/70 mt-1">
            Powered by Hostinger Horizons
          </p>
        </motion.footer>
      );
    };

    export default Footer;
  