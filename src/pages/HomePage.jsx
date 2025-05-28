
    import React from 'react';
    import { useEvents } from '@/contexts/EventContext.jsx';
    import EventCard from '@/components/EventCard.jsx';
    import { Button } from '@/components/ui/button.jsx';
    import { Link } from 'react-router-dom';
    import { motion } from 'framer-motion';
    import { PlusCircle, Info } from 'lucide-react';

    const HomePage = () => {
      const { events } = useEvents();

      return (
        <div className="space-y-8">
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="flex flex-col sm:flex-row justify-between items-center gap-4 p-6 rounded-lg glassmorphic"
          >
            <div>
              <h1 className="text-4xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
                Upcoming Events
              </h1>
              <p className="text-muted-foreground mt-2">
                Discover amazing events happening around you.
              </p>
            </div>
            <Button asChild variant="premium">
              <Link to="/create-event">
                <PlusCircle className="mr-2 h-5 w-5" /> Create Your Event
              </Link>
            </Button>
          </motion.div>

          {events.length === 0 ? (
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="text-center py-12"
            >
              <Info className="h-16 w-16 mx-auto text-primary mb-4" />
              <h2 className="text-2xl font-semibold text-foreground mb-2">No Events Yet!</h2>
              <p className="text-muted-foreground mb-6">
                Be the first to create an event and get the party started.
              </p>
              <img  alt="Empty stage with confetti" class="mx-auto rounded-lg shadow-xl w-full max-w-md h-auto" src="https://images.unsplash.com/photo-1694030954886-74c7a4e9f4e5" />
            </motion.div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {events.map((event, index) => (
                <motion.div
                  key={event.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <EventCard event={event} />
                </motion.div>
              ))}
            </div>
          )}
        </div>
      );
    };

    export default HomePage;
  